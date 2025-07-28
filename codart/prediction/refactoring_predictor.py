#!/usr/bin/env python3
"""
Enhanced Refactoring Sequence Predictor for CodART.
Provides high-level interface for using trained models to predict optimal refactoring sequences.
"""

import os
import sys
import torch
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import pandas as pd

# Add CodART modules to path
sys.path.append('/app')

from codart.learner.tests.test_reinforcement.environment import RefactoringSequenceEnvironment
from codart.learner.tests.test_reinforcement.model import create_policy_module, create_value_module
from codart.utility.directory_utils import update_understand_database
from codart.metrics.qmood import DesignQualityAttributes


@dataclass
class RefactoringRecommendation:
    """Data class for a single refactoring recommendation."""
    step: int
    refactoring_type: str
    confidence: float
    target_class: str
    target_method: Optional[str]
    parameters: Dict[str, Any]
    expected_improvement: Dict[str, float]
    rationale: str


@dataclass
class PredictionResult:
    """Data class for prediction results."""
    project_name: str
    model_used: str
    recommendations: List[RefactoringRecommendation]
    total_expected_improvement: Dict[str, float]
    execution_time: float
    timestamp: str
    confidence_score: float


class RefactoringSequencePredictor:
    """
    High-level interface for predicting refactoring sequences using trained models.
    """

    def __init__(self, 
                 project_name: str,
                 udb_path: str,
                 project_path: str,
                 model_checkpoint: Optional[str] = None,
                 device: str = "auto"):
        """
        Initialize the predictor.

        Args:
            project_name: Name of the project
            udb_path: Path to Understand database file
            project_path: Path to project source code
            model_checkpoint: Specific model checkpoint path (uses latest if None)
            device: Device to run inference on
        """
        self.project_name = project_name
        self.udb_path = udb_path
        self.project_path = project_path
        self.model_checkpoint = model_checkpoint
        
        # Set device
        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        
        # Model components (loaded lazily)
        self._environment = None
        self._policy_module = None
        self._value_module = None
        self._model_loaded = False

    def load_model(self, checkpoint_path: Optional[str] = None) -> bool:
        """
        Load the trained model for inference.

        Args:
            checkpoint_path: Path to model checkpoint

        Returns:
            True if model loaded successfully
        """
        try:
            # Initialize environment
            self._environment = RefactoringSequenceEnvironment(
                udb_path=self.udb_path,
                project_name=self.project_name,
                project_path=self.project_path,
                device=self.device
            )

            # Create model architecture
            self._policy_module = create_policy_module(self._environment)
            self._value_module = create_value_module(self._environment)

            # Load checkpoint if provided
            if checkpoint_path and os.path.exists(checkpoint_path):
                checkpoint = torch.load(checkpoint_path, map_location=self.device)
                
                if 'policy_state_dict' in checkpoint:
                    self._policy_module.load_state_dict(checkpoint['policy_state_dict'])
                if 'value_state_dict' in checkpoint:
                    self._value_module.load_state_dict(checkpoint['value_state_dict'])
                    
                self.model_checkpoint = checkpoint_path
                self.logger.info(f"Loaded model from {checkpoint_path}")
            else:
                self.logger.warning("No checkpoint provided or found, using untrained model")

            # Set to evaluation mode
            self._policy_module.eval()
            self._value_module.eval()
            
            self._model_loaded = True
            return True

        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            return False

    def predict_sequence(self, 
                        max_steps: int = 10,
                        temperature: float = 1.0,
                        confidence_threshold: float = 0.3) -> PredictionResult:
        """
        Predict an optimal refactoring sequence.

        Args:
            max_steps: Maximum number of refactoring steps
            temperature: Sampling temperature for predictions
            confidence_threshold: Minimum confidence for recommendations

        Returns:
            PredictionResult with recommendations
        """
        if not self._model_loaded:
            raise ValueError("Model not loaded. Call load_model() first.")

        start_time = datetime.now()
        recommendations = []
        
        try:
            # Get initial state
            current_observation = self._environment.reset()
            
            # Generate baseline metrics
            baseline_metrics = self._get_current_metrics()
            
            for step in range(max_steps):
                with torch.no_grad():
                    # Get policy prediction
                    policy_output = self._policy_module(current_observation)
                    
                    # Get refactoring type prediction
                    refactoring_type, confidence = self._predict_refactoring_type(
                        policy_output, temperature
                    )
                    
                    # Skip low-confidence predictions
                    if confidence < confidence_threshold:
                        self.logger.info(f"Step {step + 1}: Skipping low confidence prediction ({confidence:.3f})")
                        continue
                    
                    # Get value estimation
                    expected_improvement = self._get_expected_improvement(current_observation)
                    
                    # Generate refactoring action
                    action = self._generate_refactoring_action(policy_output, refactoring_type)
                    
                    # Extract refactoring details
                    refactoring_details = self._extract_refactoring_details(action)
                    
                    # Create recommendation
                    recommendation = RefactoringRecommendation(
                        step=step + 1,
                        refactoring_type=refactoring_type,
                        confidence=confidence,
                        target_class=refactoring_details.get('target_class', 'Unknown'),
                        target_method=refactoring_details.get('target_method'),
                        parameters=refactoring_details.get('parameters', {}),
                        expected_improvement=expected_improvement,
                        rationale=self._generate_rationale(refactoring_type, expected_improvement)
                    )
                    
                    recommendations.append(recommendation)
                    
                    # Update environment
                    current_observation = self._environment.step(action)
                    
                    # Check if done
                    if current_observation.get('done', torch.tensor([False])).item():
                        break

            # Calculate metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            total_improvement = self._calculate_total_improvement(recommendations)
            avg_confidence = sum(r.confidence for r in recommendations) / len(recommendations) if recommendations else 0.0

            return PredictionResult(
                project_name=self.project_name,
                model_used=self.model_checkpoint or "untrained",
                recommendations=recommendations,
                total_expected_improvement=total_improvement,
                execution_time=execution_time,
                timestamp=datetime.now().isoformat(),
                confidence_score=avg_confidence
            )

        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            raise

    def _predict_refactoring_type(self, policy_output: Dict, temperature: float) -> Tuple[str, float]:
        """Predict refactoring type from policy output."""
        refactoring_types = [
            "Move Method", "Extract Class", "Extract Method",
            "Pull Up Method", "Push Down Method", "Move Class"
        ]
        
        if 'refactoring_logits' in policy_output:
            logits = policy_output['refactoring_logits'] / temperature
            probs = torch.softmax(logits, dim=-1)
            type_idx = torch.multinomial(probs, 1).item()
            confidence = probs[type_idx].item()
            return refactoring_types[type_idx], confidence
        
        return refactoring_types[0], 0.5

    def _get_expected_improvement(self, observation: torch.Tensor) -> Dict[str, float]:
        """Get expected improvement from value network."""
        with torch.no_grad():
            state_value = self._value_module(observation)
            if torch.is_tensor(state_value):
                improvements = state_value.cpu().numpy().flatten()
                return {f'objective_{i}': float(improvements[i]) 
                       for i in range(len(improvements))}
        return {}

    def _generate_refactoring_action(self, policy_output: Dict, refactoring_type: str):
        """Generate a refactoring action."""
        try:
            # Use environment's action generator as fallback
            return self._environment.generator.generate_an_action()
        except Exception as e:
            self.logger.warning(f"Failed to generate action: {e}")
            return None

    def _extract_refactoring_details(self, action) -> Dict[str, Any]:
        """Extract details from refactoring action."""
        details = {}
        
        try:
            if hasattr(action, 'get_refactoring'):
                refactoring = action.get_refactoring()
                if hasattr(refactoring, 'params'):
                    details['parameters'] = refactoring.params
                if hasattr(refactoring, 'class_name'):
                    details['target_class'] = refactoring.class_name
                if hasattr(refactoring, 'method_name'):
                    details['target_method'] = refactoring.method_name
        except Exception as e:
            self.logger.warning(f"Could not extract refactoring details: {e}")
            
        return details

    def _generate_rationale(self, refactoring_type: str, expected_improvement: Dict[str, float]) -> str:
        """Generate human-readable rationale for the refactoring."""
        top_objective = max(expected_improvement, key=expected_improvement.get) if expected_improvement else "unknown"
        improvement_value = expected_improvement.get(top_objective, 0.0)
        
        rationales = {
            "Move Method": f"Moving method will improve {top_objective} by {improvement_value:.3f}",
            "Extract Class": f"Extracting class will enhance cohesion and improve {top_objective}",
            "Extract Method": f"Extracting method will reduce complexity and improve {top_objective}",
            "Pull Up Method": f"Pulling up method will improve inheritance hierarchy",
            "Push Down Method": f"Pushing down method will improve specialization",
            "Move Class": f"Moving class will improve package structure"
        }
        
        return rationales.get(refactoring_type, f"This refactoring will improve {top_objective}")

    def _calculate_total_improvement(self, recommendations: List[RefactoringRecommendation]) -> Dict[str, float]:
        """Calculate total expected improvement."""
        total = {}
        for rec in recommendations:
            for key, value in rec.expected_improvement.items():
                total[key] = total.get(key, 0.0) + value
        return total

    def _get_current_metrics(self) -> Dict[str, float]:
        """Get current code quality metrics."""
        try:
            metrics_calculator = DesignQualityAttributes(self.udb_path)
            return metrics_calculator.get_metrics()
        except Exception as e:
            self.logger.warning(f"Could not calculate current metrics: {e}")
            return {}

    def save_predictions(self, result: PredictionResult, output_path: str) -> bool:
        """Save predictions to file."""
        try:
            # Convert to serializable format
            output_data = {
                'project_name': result.project_name,
                'model_used': result.model_used,
                'timestamp': result.timestamp,
                'execution_time': result.execution_time,
                'confidence_score': result.confidence_score,
                'total_expected_improvement': result.total_expected_improvement,
                'recommendations': [
                    {
                        'step': rec.step,
                        'refactoring_type': rec.refactoring_type,
                        'confidence': rec.confidence,
                        'target_class': rec.target_class,
                        'target_method': rec.target_method,
                        'parameters': rec.parameters,
                        'expected_improvement': rec.expected_improvement,
                        'rationale': rec.rationale
                    }
                    for rec in result.recommendations
                ]
            }
            
            with open(output_path, 'w') as f:
                json.dump(output_data, f, indent=2)
                
            self.logger.info(f"Predictions saved to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save predictions: {e}")
            return False


# Convenience functions for easy usage

def predict_for_project(project_name: str,
                       udb_path: str,
                       project_path: str,
                       model_checkpoint: Optional[str] = None,
                       max_steps: int = 10,
                       temperature: float = 1.0,
                       output_file: Optional[str] = None) -> PredictionResult:
    """
    Convenience function to predict refactoring sequence for a project.

    Args:
        project_name: Name of the project
        udb_path: Path to Understand database
        project_path: Path to project source code
        model_checkpoint: Model checkpoint path
        max_steps: Maximum refactoring steps
        temperature: Sampling temperature
        output_file: Optional output file path

    Returns:
        PredictionResult
    """
    predictor = RefactoringSequencePredictor(
        project_name=project_name,
        udb_path=udb_path,
        project_path=project_path,
        model_checkpoint=model_checkpoint
    )
    
    if not predictor.load_model(model_checkpoint):
        raise RuntimeError("Failed to load model")
    
    result = predictor.predict_sequence(
        max_steps=max_steps,
        temperature=temperature
    )
    
    if output_file:
        predictor.save_predictions(result, output_file)
    
    return result


def batch_predict_projects(projects: List[Dict[str, str]], 
                          model_checkpoint: Optional[str] = None,
                          max_steps: int = 10) -> Dict[str, PredictionResult]:
    """
    Predict refactoring sequences for multiple projects.

    Args:
        projects: List of project configurations
        model_checkpoint: Model checkpoint path
        max_steps: Maximum refactoring steps

    Returns:
        Dictionary mapping project names to results
    """
    results = {}
    
    for project_config in projects:
        project_name = project_config['project_name']
        try:
            result = predict_for_project(
                project_name=project_name,
                udb_path=project_config['udb_path'],
                project_path=project_config['project_path'],
                model_checkpoint=model_checkpoint,
                max_steps=max_steps
            )
            results[project_name] = result
        except Exception as e:
            logging.error(f"Prediction failed for {project_name}: {e}")
            
    return results