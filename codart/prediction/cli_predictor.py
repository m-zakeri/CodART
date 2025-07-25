#!/usr/bin/env python3
"""
Command-line interface for refactoring sequence prediction using trained models.
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add CodART to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from codart.prediction.refactoring_predictor import predict_for_project, batch_predict_projects


def print_prediction_summary(result):
    """Print a summary of prediction results."""
    print(f"\n{'='*60}")
    print(f"REFACTORING SEQUENCE PREDICTION RESULTS")
    print(f"{'='*60}")
    print(f"Project: {result.project_name}")
    print(f"Model: {result.model_used}")
    print(f"Execution Time: {result.execution_time:.2f}s")
    print(f"Average Confidence: {result.confidence_score:.3f}")
    print(f"Total Recommendations: {len(result.recommendations)}")
    
    print(f"\n{'RECOMMENDATIONS':-^60}")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"\n{i}. {rec.refactoring_type}")
        print(f"   Target: {rec.target_class}")
        if rec.target_method:
            print(f"   Method: {rec.target_method}")
        print(f"   Confidence: {rec.confidence:.3f}")
        print(f"   Rationale: {rec.rationale}")
        
        # Show top expected improvements
        if rec.expected_improvement:
            top_improvements = sorted(
                rec.expected_improvement.items(), 
                key=lambda x: abs(x[1]), 
                reverse=True
            )[:3]
            print(f"   Expected Improvements:")
            for obj, value in top_improvements:
                print(f"     {obj}: {value:+.4f}")
    
    print(f"\n{'TOTAL EXPECTED IMPROVEMENT':-^60}")
    if result.total_expected_improvement:
        for obj, value in result.total_expected_improvement.items():
            print(f"{obj}: {value:+.4f}")


def main():
    parser = argparse.ArgumentParser(
        description="Predict optimal refactoring sequences using trained CodART models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic prediction for a project
  python cli_predictor.py --project myproject --udb /path/to/project.udb --source /path/to/source

  # Use specific model checkpoint
  python cli_predictor.py --project myproject --udb /path/to/project.udb --source /path/to/source \\
                         --model /path/to/checkpoint.pth

  # Save results to file
  python cli_predictor.py --project myproject --udb /path/to/project.udb --source /path/to/source \\
                         --output predictions.json

  # Batch prediction from config file
  python cli_predictor.py --batch projects.json --output batch_results.json
        """
    )
    
    # Project configuration
    parser.add_argument('--project', '-p', type=str,
                       help='Project name')
    parser.add_argument('--udb', '-u', type=str,
                       help='Path to Understand database file (.udb)')
    parser.add_argument('--source', '-s', type=str,
                       help='Path to project source code')
    
    # Model configuration
    parser.add_argument('--model', '-m', type=str,
                       help='Path to model checkpoint file (uses latest if not specified)')
    parser.add_argument('--max-steps', type=int, default=10,
                       help='Maximum number of refactoring steps to predict (default: 10)')
    parser.add_argument('--temperature', type=float, default=1.0,
                       help='Sampling temperature for predictions (default: 1.0)')
    parser.add_argument('--confidence', type=float, default=0.3,
                       help='Minimum confidence threshold for recommendations (default: 0.3)')
    
    # Batch processing
    parser.add_argument('--batch', '-b', type=str,
                       help='JSON file with multiple project configurations')
    
    # Output options
    parser.add_argument('--output', '-o', type=str,
                       help='Output file path for saving results (JSON format)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress console output (useful with --output)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Configure logging
    import logging
    if args.verbose:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    elif args.quiet:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.WARNING)
    
    try:
        # Batch processing
        if args.batch:
            if not os.path.exists(args.batch):
                print(f"Error: Batch configuration file not found: {args.batch}")
                sys.exit(1)
            
            with open(args.batch, 'r') as f:
                projects_config = json.load(f)
            
            if not args.quiet:
                print(f"Starting batch prediction for {len(projects_config)} projects...")
            
            results = batch_predict_projects(
                projects=projects_config,
                model_checkpoint=args.model,
                max_steps=args.max_steps
            )
            
            # Save results
            if args.output:
                output_data = {}
                for project_name, result in results.items():
                    # Convert to dict for JSON serialization
                    output_data[project_name] = {
                        'project_name': result.project_name,
                        'model_used': result.model_used,
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
                
                with open(args.output, 'w') as f:
                    json.dump(output_data, f, indent=2)
                
                if not args.quiet:
                    print(f"Batch results saved to {args.output}")
            
            # Print summary
            if not args.quiet:
                print(f"\nBatch prediction completed:")
                for project_name, result in results.items():
                    print(f"  {project_name}: {len(result.recommendations)} recommendations")
        
        # Single project processing
        else:
            if not all([args.project, args.udb, args.source]):
                print("Error: --project, --udb, and --source are required for single project prediction")
                print("Use --batch for batch processing or --help for more information")
                sys.exit(1)
            
            if not os.path.exists(args.udb):
                print(f"Error: UDB file not found: {args.udb}")
                sys.exit(1)
            
            if not os.path.exists(args.source):
                print(f"Error: Source directory not found: {args.source}")
                sys.exit(1)
            
            if not args.quiet:
                print(f"Starting prediction for project: {args.project}")
                if args.model:
                    print(f"Using model: {args.model}")
                else:
                    print("Using latest available model")
            
            # Run prediction
            result = predict_for_project(
                project_name=args.project,
                udb_path=args.udb,
                project_path=args.source,
                model_checkpoint=args.model,
                max_steps=args.max_steps,
                temperature=args.temperature,
                output_file=args.output
            )
            
            # Print results
            if not args.quiet:
                print_prediction_summary(result)
            
            if args.output and not args.quiet:
                print(f"\nResults saved to: {args.output}")
        
    except KeyboardInterrupt:
        print("\nPrediction interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()