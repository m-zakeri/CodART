import React, { useState, useEffect, useCallback } from 'react';
import { Upload, Download, Play, Pause, Trash2, FileText, Activity, Package, AlertCircle, CheckCircle, Clock, X, RefreshCw, Moon, Sun, Save, Database, Brain, TrendingUp, BarChart3, Settings, Target, GitBranch, RotateCcw, Square, PlayCircle, History, Archive, Zap, Sparkles, ChevronRight, Info } from 'lucide-react';

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Local Storage Keys
const STORAGE_KEYS = {
  THEME: 'codart-theme',
  TASK_HISTORY: 'codart-task-history',
  PROJECT_CONFIGS: 'codart-project-configs',
  ML_MODELS: 'codart-ml-models',
};

// Storage Manager
class StorageManager {
  static save(key, data) {
    try {
      localStorage.setItem(key, JSON.stringify(data));
    } catch (e) {
      console.error('Failed to save to localStorage:', e);
    }
  }

  static load(key, defaultValue = null) {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (e) {
      console.error('Failed to load from localStorage:', e);
      return defaultValue;
    }
  }

  static addToList(key, item, maxItems = 20) {
    const list = this.load(key, []);
    const filtered = list.filter(i => i.task_id !== item.task_id);
    const updated = [item, ...filtered].slice(0, maxItems);
    this.save(key, updated);
    return updated;
  }
}

// API Client
class ApiClient {
  static async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    console.log(`Making request to: ${url}`);
    
    // Don't set Content-Type for FormData - let browser handle it
    const headers = { ...options.headers };
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
    }
    
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    if (options.responseType === 'blob') {
      return response.blob();
    }

    return response.json();
  }
}

// Components
const ProgressBar = ({ progress, label, color = 'blue', darkMode }) => (
  <div className="w-full">
    {label && <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} mb-1`}>{label}</p>}
    <div className={`w-full ${darkMode ? 'bg-gray-700' : 'bg-gray-200'} rounded-full h-2.5 overflow-hidden`}>
      <div
        className={`bg-${color}-600 h-2.5 rounded-full transition-all duration-300 ease-out`}
        style={{ width: `${Math.min(progress || 0, 100)}%` }}
      />
    </div>
    <p className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-500'} mt-1`}>{Math.round(progress || 0)}%</p>
  </div>
);

const StatusBadge = ({ status, darkMode }) => {
  const statusConfig = {
    'PENDING': { color: darkMode ? 'bg-yellow-900 text-yellow-200' : 'bg-yellow-100 text-yellow-800', icon: Clock },
    'PROGRESS': { color: darkMode ? 'bg-blue-900 text-blue-200' : 'bg-blue-100 text-blue-800', icon: Activity },
    'SUCCESS': { color: darkMode ? 'bg-green-900 text-green-200' : 'bg-green-100 text-green-800', icon: CheckCircle },
    'FAILURE': { color: darkMode ? 'bg-red-900 text-red-200' : 'bg-red-100 text-red-800', icon: AlertCircle },
    'CANCELLED': { color: darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-800', icon: X },
  };

  const config = statusConfig[status] || statusConfig['PENDING'];
  const Icon = config.icon;

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
      <Icon className="w-3 h-3 mr-1" />
      {status}
    </span>
  );
};

// Main App Component
const App = () => {
  const [darkMode, setDarkMode] = useState(() => StorageManager.load(STORAGE_KEYS.THEME, false));
  const [activeTab, setActiveTab] = useState('projects');
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [notification, setNotification] = useState(null);
  const [selectedProject, setSelectedProject] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [taskHistory, setTaskHistory] = useState(() => StorageManager.load(STORAGE_KEYS.TASK_HISTORY, []));
  const [mlModels, setMlModels] = useState(() => StorageManager.load(STORAGE_KEYS.ML_MODELS, []));
  const [predictionResults, setPredictionResults] = useState([]);
  const [predictionHistory, setPredictionHistory] = useState(() => StorageManager.load('prediction-history', []));
  const [testabilityTasks, setTestabilityTasks] = useState([]);
  const [availableMetrics, setAvailableMetrics] = useState([]);

  // Toggle dark mode
  useEffect(() => {
    StorageManager.save(STORAGE_KEYS.THEME, darkMode);
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  // Show notification
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  };

  // Fetch projects
  const fetchProjects = useCallback(async () => {
    try {
      const data = await ApiClient.request('/api/v1/projects/projects');
      setProjects(Array.isArray(data) ? data : data.projects || []);
    } catch (error) {
      showNotification('Failed to fetch projects: ' + error.message, 'error');
      setProjects([]);
    }
  }, []);

  // Fetch available projects for ML training
  const fetchAvailableProjects = useCallback(async () => {
    try {
      const data = await ApiClient.request('/api/v1/rl-handler/api/v1/ml-training/config/projects');
      return data.projects || [];
    } catch (error) {
      console.error('Failed to fetch available projects:', error);
      return [];
    }
  }, []);

  // Initial data fetch
  useEffect(() => {
    fetchProjects();
    fetchAvailableMetrics();
    setTestabilityTasks(StorageManager.load('testability-tasks', []));
  }, [fetchProjects]);

  // Upload project
  const handleProjectUpload = async (file, projectName, description, gitUrl, gitBranch, gitCommit) => {
    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('project_name', projectName);
    if (description) formData.append('description', description);
    if (gitUrl) formData.append('git_url', gitUrl);
    if (gitBranch) formData.append('git_branch', gitBranch);
    if (gitCommit) formData.append('git_commit', gitCommit);

    try {
      await ApiClient.request('/api/v1/projects/projects/upload', {
        method: 'POST',
        body: formData,
      });

      showNotification(`Project ${projectName} uploaded successfully!`, 'success');
      fetchProjects();
    } catch (error) {
      showNotification('Upload failed: ' + error.message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  // Analyze project
  const analyzeProject = async (projectName, versionId) => {
    try {
      setIsLoading(true);
      const formData = new FormData();
      formData.append('project_name', projectName);
      formData.append('version_id', versionId);

      await ApiClient.request('/api/v1/projects/projects/analyze', {
        method: 'POST',
        body: formData,
      });

      showNotification(`Analysis started for ${projectName}`, 'success');
    } catch (error) {
      showNotification('Analysis failed: ' + error.message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  // Start RL Training
  const startRLTraining = async (trainingConfig) => {
    try {
      setIsLoading(true);
      const response = await ApiClient.request('/api/v1/rl-handler/api/v1/ml-training/train', {
        method: 'POST',
        body: JSON.stringify(trainingConfig),
      });

      const taskData = {
        task_id: response.task_id,
        project_name: trainingConfig.env_config.project_name,
        status: response.status,
        type: 'RL_TRAINING',
        timestamp: response.timestamp,
        config: trainingConfig
      };

      // Save to history and update UI
      const updatedHistory = StorageManager.addToList(STORAGE_KEYS.TASK_HISTORY, taskData);
      setTaskHistory(updatedHistory);

      showNotification(`RL Training started! Task ID: ${response.task_id}`, 'success');
      return response;
    } catch (error) {
      showNotification('Training failed to start: ' + error.message, 'error');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Get task status
  const getTaskStatus = async (taskId) => {
    try {
      const response = await ApiClient.request(`/api/v1/rl-handler/api/v1/ml-training/status/${taskId}`);
      
      // Update task in history
      const updatedHistory = taskHistory.map(task => 
        task.task_id === taskId ? { ...task, ...response } : task
      );
      setTaskHistory(updatedHistory);
      StorageManager.save(STORAGE_KEYS.TASK_HISTORY, updatedHistory);
      
      return response;
    } catch (error) {
      console.error('Failed to fetch task status:', error);
      return null;
    }
  };

  // Cancel training
  const cancelTraining = async (taskId) => {
    try {
      await ApiClient.request(`/api/v1/rl-handler/api/v1/ml-training/cancel/${taskId}`, {
        method: 'DELETE',
      });
      showNotification(`Task ${taskId} cancelled`, 'info');
      getTaskStatus(taskId);
    } catch (error) {
      showNotification('Failed to cancel task: ' + error.message, 'error');
    }
  };

  // Stop training gracefully
  const stopTraining = async (taskId, saveCheckpoint = true) => {
    try {
      await ApiClient.request(`/api/v1/rl-handler/api/v1/ml-training/stop/${taskId}?save_checkpoint=${saveCheckpoint}`, {
        method: 'POST',
      });
      showNotification(`Task ${taskId} stopped ${saveCheckpoint ? 'with checkpoint saved' : 'immediately'}`, 'info');
      getTaskStatus(taskId);
    } catch (error) {
      showNotification('Failed to stop task: ' + error.message, 'error');
    }
  };

  // Resume/Fine-tune training
  const resumeTraining = async (resumeConfig) => {
    try {
      setIsLoading(true);
      const response = await ApiClient.request('/api/v1/rl-handler/api/v1/ml-training/resume', {
        method: 'POST',
        body: JSON.stringify(resumeConfig),
      });

      const taskData = {
        task_id: response.task_id,
        project_name: resumeConfig.project_name,
        status: response.status,
        type: resumeConfig.fine_tune ? 'RL_FINE_TUNE' : 'RL_RESUME',
        timestamp: response.timestamp,
        config: resumeConfig
      };

      // Save to history and update UI
      const updatedHistory = StorageManager.addToList(STORAGE_KEYS.TASK_HISTORY, taskData);
      setTaskHistory(updatedHistory);

      showNotification(response.message, 'success');
      return response;
    } catch (error) {
      showNotification('Failed to resume/fine-tune training: ' + error.message, 'error');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Get available checkpoints
  const getAvailableCheckpoints = async (projectName) => {
    try {
      const response = await ApiClient.request(`/api/v1/rl-handler/api/v1/ml-training/checkpoints/${projectName}`);
      return response;
    } catch (error) {
      console.error('Failed to fetch checkpoints:', error);
      return { available_checkpoints: [], total_checkpoints: 0 };
    }
  };

  // Cleanup old checkpoints
  const cleanupCheckpoints = async (projectName, keepLatest = 5) => {
    try {
      const response = await ApiClient.request(`/api/v1/rl-handler/api/v1/ml-training/checkpoints/${projectName}/cleanup?keep_latest=${keepLatest}`, {
        method: 'POST',
      });
      showNotification(`Cleanup completed: ${response.deleted_checkpoints} checkpoints removed`, 'success');
      return response;
    } catch (error) {
      showNotification('Failed to cleanup checkpoints: ' + error.message, 'error');
      throw error;
    }
  };

  // Testability ML Training Functions
  const startTestabilityTraining = async (trainingConfig) => {
    try {
      setIsLoading(true);
      const response = await ApiClient.request('/api/v1/tasks/ml-training-tasks/start-training', {
        method: 'POST',
        body: JSON.stringify(trainingConfig),
      });

      const taskData = {
        task_id: response.task_id,
        project_name: trainingConfig.project_name || 'N/A',
        status: response.status || 'PENDING',
        type: 'TESTABILITY_TRAINING',
        timestamp: new Date().toISOString(),
        config: trainingConfig
      };

      const updatedTasks = [...testabilityTasks, taskData];
      setTestabilityTasks(updatedTasks);
      StorageManager.save('testability-tasks', updatedTasks);

      showNotification(`Testability training started! Task ID: ${response.task_id}`, 'success');
      return response;
    } catch (error) {
      showNotification('Testability training failed to start: ' + error.message, 'error');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const getTestabilityTaskStatus = async (taskId) => {
    try {
      const response = await ApiClient.request(`/api/v1/tasks/ml-training-tasks/task-status/${taskId}`);
      
      const updatedTasks = testabilityTasks.map(task => 
        task.task_id === taskId ? { ...task, ...response } : task
      );
      setTestabilityTasks(updatedTasks);
      StorageManager.save('testability-tasks', updatedTasks);
      
      return response;
    } catch (error) {
      console.error('Failed to fetch testability task status:', error);
      return null;
    }
  };

  const cancelTestabilityTraining = async (taskId) => {
    try {
      await ApiClient.request(`/api/v1/tasks/ml-training-tasks/cancel-task/${taskId}`, {
        method: 'POST',
      });
      showNotification(`Testability task ${taskId} cancelled`, 'info');
      getTestabilityTaskStatus(taskId);
    } catch (error) {
      showNotification('Failed to cancel testability task: ' + error.message, 'error');
    }
  };

  // Fetch available metrics
  const fetchAvailableMetrics = async () => {
    try {
      const response = await ApiClient.request('/api/v1/learning/metrics/api/v1/metrics');
      setAvailableMetrics(Array.isArray(response) ? response : []);
    } catch (error) {
      console.error('Failed to fetch available metrics:', error);
      setAvailableMetrics([]);
    }
  };

  // Fetch available datasets for testability training
  const fetchAvailableDatasets = async () => {
    try {
      const allDatasets = [];
      
      // Fetch datasets for each project
      for (const project of projects) {
        try {
          const projectName = project.name || project.project_name;
          const response = await ApiClient.request(`/api/v1/exporter/metrics/${projectName}`);
          
          if (response && response.metrics) {
            // Add project-specific datasets to the list
            allDatasets.push(...response.metrics.map(metric => ({
              ...metric,
              display_name: `${metric.project_name} - ${metric.metric_type} (${metric.version_id})`
            })));
          }
        } catch (error) {
          console.error(`Failed to fetch datasets for project ${project.name}:`, error);
        }
      }
      
      return allDatasets;
    } catch (error) {
      console.error('Failed to fetch available datasets:', error);
      return [];
    }
  };

  // Export metrics
  const exportMetrics = async (exportConfig) => {
    try {
      setIsLoading(true);
      const response = await ApiClient.request('/api/v1/exporter/metrics/export', {
        method: 'POST',
        body: JSON.stringify(exportConfig),
      });
      showNotification('Metrics exported successfully!', 'success');
      fetchAvailableMetrics(); // Refresh metrics list
      return response;
    } catch (error) {
      showNotification('Failed to export metrics: ' + error.message, 'error');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Download file
  const downloadFile = async (endpoint, filename) => {
    try {
      const response = await ApiClient.request(endpoint, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(response);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      showNotification(`${filename} downloaded successfully!`, 'success');
    } catch (error) {
      showNotification(`Failed to download ${filename}: ` + error.message, 'error');
    }
  };

  // Delete project
  const deleteProject = async (projectName, versionId) => {
    if (window.confirm(`Are you sure you want to delete project "${projectName}"?`)) {
      try {
        const params = versionId ? `?version_id=${versionId}` : '';
        await ApiClient.request(`/api/v1/projects/projects/${projectName}${params}`, {
          method: 'DELETE',
        });
        showNotification('Project deleted successfully', 'success');
        fetchProjects();
      } catch (error) {
        showNotification('Failed to delete project: ' + error.message, 'error');
      }
    }
  };

  // Prediction Functions
  const predictRefactoringSequence = async (predictionRequest) => {
    try {
      setIsLoading(true);
      const response = await ApiClient.request('/api/v1/rl-handler/api/v1/ml-training/predict', {
        method: 'POST',
        body: JSON.stringify(predictionRequest),
      });

      const predictionData = {
        ...response,
        prediction_id: `pred_${Date.now()}`,
        timestamp: new Date().toISOString(),
        request_params: predictionRequest
      };

      // Save to history
      const updatedHistory = StorageManager.addToList('prediction-history', predictionData, 50);
      setPredictionHistory(updatedHistory);
      setPredictionResults([predictionData]);

      showNotification(`Prediction generated! Found ${response.predictions.length} recommendations`, 'success');
      return response;
    } catch (error) {
      showNotification('Prediction failed: ' + error.message, 'error');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const getAvailableModels = async (projectName) => {
    try {
      const response = await ApiClient.request(`/api/v1/rl-handler/api/v1/ml-training/models/${projectName}`);
      return response.available_models || [];
    } catch (error) {
      console.error('Failed to fetch available models:', error);
      return [];
    }
  };

  const loadModelForInference = async (projectName, checkpointPath) => {
    try {
      const response = await ApiClient.request(`/api/v1/rl-handler/api/v1/ml-training/models/${projectName}/load`, {
        method: 'POST',
        body: JSON.stringify({ checkpoint_path: checkpointPath }),
      });
      showNotification(`Model loaded successfully for ${projectName}`, 'success');
      return response;
    } catch (error) {
      showNotification('Failed to load model: ' + error.message, 'error');
      throw error;
    }
  };

  // Render Projects Tab
  const renderProjects = () => (
    <div className="space-y-6">
      {/* Upload Section */}
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
        <h3 className={`text-lg font-semibold mb-4 flex items-center ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          <Upload className="w-5 h-5 mr-2 text-blue-600" />
          Upload New Project
        </h3>
        <ProjectUploadForm onUpload={handleProjectUpload} isLoading={isLoading} darkMode={darkMode} />
      </div>

      {/* Projects List */}
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg`}>
        <div className={`px-6 py-4 border-b ${darkMode ? 'bg-gray-900 border-gray-700' : 'bg-gray-50 border-gray-200'}`}>
          <div className="flex items-center justify-between">
            <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Projects</h3>
            <button
              onClick={fetchProjects}
              className={`p-2 ${darkMode ? 'text-gray-400 hover:text-blue-400 hover:bg-gray-700' : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'} rounded transition`}
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <div className={`divide-y ${darkMode ? 'divide-gray-700' : 'divide-gray-200'}`}>
          {projects.length === 0 ? (
            <div className="p-12 text-center">
              <Package className={`w-16 h-16 mx-auto ${darkMode ? 'text-gray-600' : 'text-gray-300'} mb-4`} />
              <p className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>No projects uploaded yet. Upload your first project above!</p>
            </div>
          ) : (
            projects.map((project, index) => (
              <ProjectCard 
                key={index}
                project={project}
                darkMode={darkMode}
                onAnalyze={analyzeProject}
                onDelete={deleteProject}
                onSelectForML={(proj) => {
                  setSelectedProject(proj);
                  setActiveTab('training');
                }}
                isLoading={isLoading}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );

  // Render ML Training Tab
  const renderTraining = () => (
    <div className="space-y-6">
      <MLTrainingForm 
        onSubmit={startRLTraining}
        projects={projects}
        selectedProject={selectedProject}
        darkMode={darkMode}
        isLoading={isLoading}
      />
      
      <RLCheckpointManager 
        projects={projects}
        darkMode={darkMode}
        getAvailableCheckpoints={getAvailableCheckpoints}
        cleanupCheckpoints={cleanupCheckpoints}
        resumeTraining={resumeTraining}
        isLoading={isLoading}
      />
    </div>
  );

  // Render Task Monitoring Tab
  const renderTasks = () => (
    <div className="space-y-6">
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg`}>
        <div className={`px-6 py-4 border-b ${darkMode ? 'bg-gray-900 border-gray-700' : 'bg-gray-50 border-gray-200'}`}>
          <div className="flex items-center justify-between">
            <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>RL Training Tasks</h3>
            <button
              onClick={() => {
                taskHistory.forEach(task => {
                  if (task.status === 'PROGRESS' || task.status === 'PENDING') {
                    getTaskStatus(task.task_id);
                  }
                });
              }}
              className={`p-2 ${darkMode ? 'text-gray-400 hover:text-blue-400 hover:bg-gray-700' : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'} rounded transition`}
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <div className={`divide-y ${darkMode ? 'divide-gray-700' : 'divide-gray-200'}`}>
          {taskHistory.length === 0 ? (
            <div className="p-12 text-center">
              <Activity className={`w-16 h-16 mx-auto ${darkMode ? 'text-gray-600' : 'text-gray-300'} mb-4`} />
              <p className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>No RL training tasks yet. Start a training from the ML Training tab!</p>
            </div>
          ) : (
            taskHistory.map((task) => (
              <EnhancedTaskCard
                key={task.task_id}
                task={task}
                darkMode={darkMode}
                onCancel={cancelTraining}
                onRefresh={() => getTaskStatus(task.task_id)}
                stopTraining={stopTraining}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );

  // Render Testability Training Tab
  const renderTestabilityTraining = () => (
    <div className="space-y-6">
      <TestabilityTrainingForm 
        onSubmit={startTestabilityTraining}
        projects={projects}
        fetchAvailableDatasets={fetchAvailableDatasets}
        darkMode={darkMode}
        isLoading={isLoading}
      />
      
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg`}>
        <div className={`px-6 py-4 border-b ${darkMode ? 'bg-gray-900 border-gray-700' : 'bg-gray-50 border-gray-200'}`}>
          <div className="flex items-center justify-between">
            <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Testability Training Tasks</h3>
            <button
              onClick={() => {
                testabilityTasks.forEach(task => {
                  if (task.status === 'PROGRESS' || task.status === 'PENDING') {
                    getTestabilityTaskStatus(task.task_id);
                  }
                });
              }}
              className={`p-2 ${darkMode ? 'text-gray-400 hover:text-blue-400 hover:bg-gray-700' : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'} rounded transition`}
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <div className={`divide-y ${darkMode ? 'divide-gray-700' : 'divide-gray-200'}`}>
          {testabilityTasks.length === 0 ? (
            <div className="p-12 text-center">
              <Target className={`w-16 h-16 mx-auto ${darkMode ? 'text-gray-600' : 'text-gray-300'} mb-4`} />
              <p className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>No testability training tasks yet. Start a training above!</p>
            </div>
          ) : (
            testabilityTasks.map((task) => (
              <TaskCard
                key={task.task_id}
                task={task}
                darkMode={darkMode}
                onCancel={cancelTestabilityTraining}
                onRefresh={() => getTestabilityTaskStatus(task.task_id)}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );

  // Render Predictions Tab
  const renderPredictions = () => (
    <div className="space-y-6">
      <RefactoringPredictionForm
        onSubmit={predictRefactoringSequence}
        projects={projects}
        darkMode={darkMode}
        isLoading={isLoading}
        getAvailableModels={getAvailableModels}
        loadModelForInference={loadModelForInference}
      />
      
      <PredictionResultsSection
        predictionResults={predictionResults}
        predictionHistory={predictionHistory}
        darkMode={darkMode}
        onClearHistory={() => {
          setPredictionHistory([]);
          StorageManager.save('prediction-history', []);
        }}
        setPredictionResults={setPredictionResults}
      />
    </div>
  );

  // Render Metrics and Downloads Tab
  const renderMetricsAndDownloads = () => (
    <div className="space-y-6">
      <MetricsExportForm
        onSubmit={exportMetrics}
        projects={projects}
        darkMode={darkMode}
        isLoading={isLoading}
      />
      
      <MetricsDownloadSection
        availableMetrics={availableMetrics}
        projects={projects}
        darkMode={darkMode}
        onDownload={downloadFile}
        onRefresh={fetchAvailableMetrics}
      />
    </div>
  );

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      {/* Header */}
      <header className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} shadow-sm border-b`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Brain className="w-8 h-8 text-blue-600 mr-3" />
              <h1 className={`text-xl font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                CodART - ML Code Refactoring Platform
              </h1>
            </div>
            <div className="flex items-center gap-4">
              <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                Tasks: {taskHistory.length}
              </span>
              <button
                onClick={() => setDarkMode(!darkMode)}
                className={`p-2 rounded-md ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'} transition`}
              >
                {darkMode ? <Sun className="w-5 h-5 text-yellow-400" /> : <Moon className="w-5 h-5 text-gray-600" />}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-b sticky top-0 z-10`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { id: 'projects', label: 'Projects', icon: Package },
              { id: 'training', label: 'ML Training', icon: Brain },
              { id: 'predictions', label: 'Refactoring Predictions', icon: Sparkles },
              { id: 'tasks', label: 'Task Monitor', icon: Activity },
              { id: 'testability', label: 'Testability Training', icon: Target },
              { id: 'metrics', label: 'Metrics & Downloads', icon: BarChart3 },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-3 border-b-2 font-medium text-sm transition flex items-center ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : darkMode 
                      ? 'border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-600' 
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4 mr-2" />
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'projects' && renderProjects()}
        {activeTab === 'training' && renderTraining()}
        {activeTab === 'predictions' && renderPredictions()}
        {activeTab === 'tasks' && renderTasks()}
        {activeTab === 'testability' && renderTestabilityTraining()}
        {activeTab === 'metrics' && renderMetricsAndDownloads()}
      </main>

      {/* Notification */}
      {notification && (
        <div className={`fixed bottom-4 right-4 p-4 rounded-lg shadow-lg transition-all transform ${
          notification.type === 'error' 
            ? darkMode ? 'bg-red-900 text-red-200 border border-red-700' : 'bg-red-100 text-red-800 border border-red-200'
            : notification.type === 'success' 
            ? darkMode ? 'bg-green-900 text-green-200 border border-green-700' : 'bg-green-100 text-green-800 border border-green-200'
            : darkMode ? 'bg-blue-900 text-blue-200 border border-blue-700' : 'bg-blue-100 text-blue-800 border border-blue-200'
        }`}>
          <div className="flex items-center">
            {notification.type === 'error' && <AlertCircle className="w-5 h-5 mr-2" />}
            {notification.type === 'success' && <CheckCircle className="w-5 h-5 mr-2" />}
            {notification.type === 'info' && <AlertCircle className="w-5 h-5 mr-2" />}
            <span className="font-medium">{notification.message}</span>
          </div>
        </div>
      )}
    </div>
  );
};

// Project Upload Form Component
const ProjectUploadForm = ({ onUpload, isLoading, darkMode }) => {
  const [formData, setFormData] = useState({
    file: null,
    project_name: '',
    description: '',
    git_url: '',
    git_branch: '',
    git_commit: ''
  });

  const handleSubmit = () => {
    if (formData.file && formData.project_name) {
      onUpload(
        formData.file,
        formData.project_name,
        formData.description,
        formData.git_url,
        formData.git_branch,
        formData.git_commit
      );
      setFormData({
        file: null,
        project_name: '',
        description: '',
        git_url: '',
        git_branch: '',
        git_commit: ''
      });
    }
  };

  const inputClass = `w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
    darkMode 
      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
      : 'bg-white border-gray-300 text-gray-900'
  }`;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Project Name *
          </label>
          <input
            type="text"
            value={formData.project_name}
            onChange={(e) => setFormData({...formData, project_name: e.target.value})}
            className={inputClass}
            placeholder="my-java-project"
          />
        </div>
        <div>
          <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Project File (.zip) *
          </label>
          <input
            type="file"
            accept=".zip"
            onChange={(e) => setFormData({...formData, file: e.target.files[0]})}
            className={inputClass}
          />
        </div>
      </div>
      
      <div>
        <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
          Description
        </label>
        <textarea
          value={formData.description}
          onChange={(e) => setFormData({...formData, description: e.target.value})}
          className={inputClass}
          rows="3"
          placeholder="Brief description of your project..."
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Git URL
          </label>
          <input
            type="text"
            value={formData.git_url}
            onChange={(e) => setFormData({...formData, git_url: e.target.value})}
            className={inputClass}
            placeholder="https://github.com/..."
          />
        </div>
        <div>
          <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Git Branch
          </label>
          <input
            type="text"
            value={formData.git_branch}
            onChange={(e) => setFormData({...formData, git_branch: e.target.value})}
            className={inputClass}
            placeholder="main"
          />
        </div>
        <div>
          <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Git Commit
          </label>
          <input
            type="text"
            value={formData.git_commit}
            onChange={(e) => setFormData({...formData, git_commit: e.target.value})}
            className={inputClass}
            placeholder="abc123..."
          />
        </div>
      </div>

      <button
        onClick={handleSubmit}
        disabled={!formData.file || !formData.project_name || isLoading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 transition duration-200 flex items-center justify-center"
      >
        {isLoading ? (
          <>
            <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            Uploading...
          </>
        ) : (
          <>
            <Upload className="w-4 h-4 mr-2" />
            Upload Project
          </>
        )}
      </button>
    </div>
  );
};

// Project Card Component  
const ProjectCard = ({ project, darkMode, onAnalyze, onDelete, onSelectForML, isLoading }) => {
  // Handle both single project and project with versions structure
  const projectName = project.project_name || project.name;
  const versions = project.versions || [project];
  const latestVersion = project.latest_version;
  
  return (
    <div className={`p-6 ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50'} transition`}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h4 className={`font-medium text-lg ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            {projectName}
          </h4>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} mt-1`}>
            {project.description || versions[0]?.description || 'No description provided'}
          </p>
          <div className="flex items-center gap-4 mt-3">
            <span className={`inline-flex items-center px-2 py-1 rounded-md ${darkMode ? 'bg-blue-700 text-blue-200' : 'bg-blue-100 text-blue-700'} text-xs`}>
              {versions.length} version{versions.length > 1 ? 's' : ''}
            </span>
            {latestVersion && (
              <span className={`inline-flex items-center px-2 py-1 rounded-md ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'} text-xs`}>
                Latest: {latestVersion}
              </span>
            )}
            {(project.git_url || versions[0]?.git_url) && (
              <a href={project.git_url || versions[0]?.git_url} target="_blank" rel="noopener noreferrer"
                 className="text-xs text-blue-600 hover:underline">
                Git Repository
              </a>
            )}
          </div>
          
          {/* Version Details */}
          {versions.length > 0 && (
            <div className="mt-3">
              <details className={`${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                <summary className="text-xs cursor-pointer hover:underline">
                  View all versions ({versions.length})
                </summary>
                <div className="mt-2 space-y-1">
                  {versions.map((version, idx) => (
                    <div key={idx} className={`text-xs p-2 rounded ${darkMode ? 'bg-gray-800' : 'bg-gray-50'}`}>
                      <span className="font-mono">{version.version_id}</span>
                      {version.upload_date && (
                        <span className={`ml-2 ${darkMode ? 'text-gray-500' : 'text-gray-500'}`}>
                          {new Date(version.upload_date).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </details>
            </div>
          )}
        </div>
        <div className="flex items-center gap-2 ml-4">
          <button
            onClick={() => onAnalyze(projectName, latestVersion || versions[0]?.version_id || 'v1.0')}
            className={`p-2 ${darkMode ? 'text-purple-400 hover:bg-purple-900' : 'text-purple-600 hover:bg-purple-50'} rounded transition`}
            title="Analyze Project"
            disabled={isLoading}
          >
            <Activity className="w-4 h-4" />
          </button>
          <button
            onClick={() => onSelectForML(project)}
            className={`p-2 ${darkMode ? 'text-green-400 hover:bg-green-900' : 'text-green-600 hover:bg-green-50'} rounded transition`}
            title="Start ML Training"
          >
            <Brain className="w-4 h-4" />
          </button>
          <button
            onClick={() => onDelete(projectName, latestVersion || versions[0]?.version_id)}
            className={`p-2 ${darkMode ? 'text-red-400 hover:bg-red-900' : 'text-red-600 hover:bg-red-50'} rounded transition`}
            title="Delete Project"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

// ML Training Form Component
const MLTrainingForm = ({ onSubmit, projects, selectedProject, darkMode, isLoading }) => {
  const [trainingConfig, setTrainingConfig] = useState({
    env_config: {
      project_name: '',
      udb_path: '',
      n_obj: 8,
      lower_band: 1,
      upper_bound: 50,
      population_size: 100,
      version_id: '',
      project_path: '',
      evaluate_in_parallel: true,
      verbose_design_metrics: true
    },
    minio_config: {
      endpoint: 'minio:9000',
      access_key: 'minioadmin',
      secret_key: 'minioadmin',
      secure: false,
      results_bucket: 'ml-models'
    },
    training_options: {
      frames_per_batch: 6000,
      n_iters: 10,
      num_epochs: 30,
      minibatch_size: 400,
      learning_rate: 0.0003,
      max_grad_norm: 1.0,
      max_steps: 100,
      save_interval: 100,
      evaluation_interval: 50,
      use_normalization: true
    }
  });
  
  const [availableVersions, setAvailableVersions] = useState([]);

  // Get available versions for selected project
  const getProjectVersions = (projectName) => {
    const project = projects.find(p => (p.project_name || p.name) === projectName);
    if (project && project.versions) {
      return project.versions;
    } else if (project && project.version_id) {
      return [{ version_id: project.version_id }];
    }
    return [];
  };
  
  // Update available versions when project changes
  useEffect(() => {
    if (trainingConfig.env_config.project_name) {
      const versions = getProjectVersions(trainingConfig.env_config.project_name);
      setAvailableVersions(versions);
      
      // Auto-select latest version if available
      if (versions.length > 0 && !trainingConfig.env_config.version_id) {
        const project = projects.find(p => (p.project_name || p.name) === trainingConfig.env_config.project_name);
        const latestVersion = project?.latest_version || versions[0]?.version_id;
        if (latestVersion) {
          setTrainingConfig(prev => ({
            ...prev,
            env_config: { ...prev.env_config, version_id: latestVersion }
          }));
        }
      }
    } else {
      setAvailableVersions([]);
    }
  }, [trainingConfig.env_config.project_name, projects]);
  
  // Update config when selected project changes from parent
  useEffect(() => {
    if (selectedProject) {
      const projectName = selectedProject.project_name || selectedProject.name;
      const versions = selectedProject.versions || [selectedProject];
      const latestVersion = selectedProject.latest_version || versions[0]?.version_id;
      
      setTrainingConfig(prev => ({
        ...prev,
        env_config: {
          ...prev.env_config,
          project_name: projectName,
          version_id: latestVersion || ''
        }
      }));
    }
  }, [selectedProject]);

  const handleSubmit = async () => {
    if (!trainingConfig.env_config.project_name) {
      alert('Please select a project');
      return;
    }
    
    // Auto-generate paths based on project selection
    const finalConfig = {
      ...trainingConfig,
      env_config: {
        ...trainingConfig.env_config,
        udb_path: `/opt/understand_dbs/${trainingConfig.env_config.project_name}/${trainingConfig.env_config.version_id}/${trainingConfig.env_config.version_id}.und`,
        project_path: `/opt/projects/${trainingConfig.env_config.project_name}/${trainingConfig.env_config.version_id}`
      }
    };

    await onSubmit(finalConfig);
  };

  const inputClass = `w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
    darkMode 
      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
      : 'bg-white border-gray-300 text-gray-900'
  }`;

  return (
    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
      <h3 className={`text-lg font-semibold mb-6 flex items-center ${darkMode ? 'text-white' : 'text-gray-900'}`}>
        <Brain className="w-5 h-5 mr-2 text-green-600" />
        Start Reinforcement Learning Training
      </h3>

      <div className="space-y-6">
        {/* Project and Version Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Select Project *
            </label>
            <select
              value={trainingConfig.env_config.project_name}
              onChange={(e) => {
                setTrainingConfig(prev => ({
                  ...prev,
                  env_config: { 
                    ...prev.env_config, 
                    project_name: e.target.value,
                    version_id: '' // Reset version when project changes
                  }
                }));
              }}
              className={inputClass}
            >
              <option value="">Choose a project...</option>
              {projects.map((project, index) => {
                const projectName = project.project_name || project.name;
                const versionCount = project.versions ? project.versions.length : 1;
                return (
                  <option key={index} value={projectName}>
                    {projectName} ({versionCount} version{versionCount > 1 ? 's' : ''})
                  </option>
                );
              })}
            </select>
          </div>
          
          <div>
            <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Select Version *
            </label>
            <select
              value={trainingConfig.env_config.version_id}
              onChange={(e) => setTrainingConfig(prev => ({
                ...prev,
                env_config: { ...prev.env_config, version_id: e.target.value }
              }))}
              className={inputClass}
              disabled={!trainingConfig.env_config.project_name}
            >
              <option value="">Choose a version...</option>
              {availableVersions.map((version, index) => (
                <option key={index} value={version.version_id}>
                  {version.version_id} {version.upload_date && `(${new Date(version.upload_date).toLocaleDateString()})`}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Environment Configuration */}
        <div className={`border rounded-lg p-4 ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
          <h4 className={`text-md font-semibold mb-3 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Environment Configuration</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Objectives
              </label>
              <input
                type="number"
                value={trainingConfig.env_config.n_obj}
                onChange={(e) => setTrainingConfig(prev => ({
                  ...prev,
                  env_config: { ...prev.env_config, n_obj: parseInt(e.target.value) }
                }))}
                className={inputClass}
              />
            </div>
            <div>
              <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Population Size
              </label>
              <input
                type="number"
                value={trainingConfig.env_config.population_size}
                onChange={(e) => setTrainingConfig(prev => ({
                  ...prev,
                  env_config: { ...prev.env_config, population_size: parseInt(e.target.value) }
                }))}
                className={inputClass}
              />
            </div>
            <div>
              <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Lower Band
              </label>
              <input
                type="number"
                value={trainingConfig.env_config.lower_band}
                onChange={(e) => setTrainingConfig(prev => ({
                  ...prev,
                  env_config: { ...prev.env_config, lower_band: parseInt(e.target.value) }
                }))}
                className={inputClass}
              />
            </div>
          </div>
        </div>

        {/* Training Options */}
        <div className={`border rounded-lg p-4 ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
          <h4 className={`text-md font-semibold mb-3 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Training Options</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Frames per Batch
              </label>
              <input
                type="number"
                value={trainingConfig.training_options.frames_per_batch}
                onChange={(e) => setTrainingConfig(prev => ({
                  ...prev,
                  training_options: { ...prev.training_options, frames_per_batch: parseInt(e.target.value) }
                }))}
                className={inputClass}
              />
            </div>
            <div>
              <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Iterations
              </label>
              <input
                type="number"
                value={trainingConfig.training_options.n_iters}
                onChange={(e) => setTrainingConfig(prev => ({
                  ...prev,
                  training_options: { ...prev.training_options, n_iters: parseInt(e.target.value) }
                }))}
                className={inputClass}
              />
            </div>
            <div>
              <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Learning Rate
              </label>
              <input
                type="number"
                step="0.0001"
                value={trainingConfig.training_options.learning_rate}
                onChange={(e) => setTrainingConfig(prev => ({
                  ...prev,
                  training_options: { ...prev.training_options, learning_rate: parseFloat(e.target.value) }
                }))}
                className={inputClass}
              />
            </div>
          </div>
        </div>

        <button
          onClick={handleSubmit}
          disabled={!trainingConfig.env_config.project_name || !trainingConfig.env_config.version_id || isLoading}
          className="w-full bg-green-600 text-white py-3 px-4 rounded-md hover:bg-green-700 disabled:bg-gray-400 transition duration-200 flex items-center justify-center text-lg font-medium"
        >
          {isLoading ? (
            <>
              <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
              Starting Training...
            </>
          ) : (
            <>
              <Brain className="w-5 h-5 mr-2" />
              Start RL Training
            </>
          )}
        </button>
      </div>
    </div>
  );
};

// RL Checkpoint Management Component
const RLCheckpointManager = ({ projects, darkMode, getAvailableCheckpoints, cleanupCheckpoints, resumeTraining, isLoading }) => {
  const [selectedProject, setSelectedProject] = useState('');
  const [checkpoints, setCheckpoints] = useState([]);
  const [loadingCheckpoints, setLoadingCheckpoints] = useState(false);
  const [showResumeModal, setShowResumeModal] = useState(false);
  const [selectedCheckpoint, setSelectedCheckpoint] = useState('');

  const loadCheckpoints = async (projectName) => {
    if (!projectName) return;
    
    setLoadingCheckpoints(true);
    try {
      const response = await getAvailableCheckpoints(projectName);
      setCheckpoints(response.available_checkpoints || []);
    } catch (error) {
      console.error('Failed to load checkpoints:', error);
      setCheckpoints([]);
    } finally {
      setLoadingCheckpoints(false);
    }
  };

  const handleProjectChange = (projectName) => {
    setSelectedProject(projectName);
    setCheckpoints([]);
    if (projectName) {
      loadCheckpoints(projectName);
    }
  };

  const handleCleanup = async () => {
    if (!selectedProject) return;
    
    if (window.confirm(`Are you sure you want to cleanup old checkpoints for ${selectedProject}? This will keep only the latest 5 checkpoints.`)) {
      try {
        await cleanupCheckpoints(selectedProject);
        loadCheckpoints(selectedProject); // Refresh list
      } catch (error) {
        console.error('Cleanup failed:', error);
      }
    }
  };

  const formatCheckpointName = (checkpointPath) => {
    const parts = checkpointPath.split('/');
    const filename = parts[parts.length - 1];
    return filename.replace('checkpoint_', '').replace('.pth', '');
  };

  const inputClass = `w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
    darkMode 
      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
      : 'bg-white border-gray-300 text-gray-900'
  }`;

  return (
    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
      <h3 className={`text-lg font-semibold mb-6 flex items-center ${darkMode ? 'text-white' : 'text-gray-900'}`}>
        <Archive className="w-5 h-5 mr-2 text-blue-600" />
        RL Checkpoint Management
      </h3>

      <div className="space-y-6">
        {/* Project Selection */}
        <div>
          <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Select Project
          </label>
          <select
            value={selectedProject}
            onChange={(e) => handleProjectChange(e.target.value)}
            className={inputClass}
          >
            <option value="">Choose a project...</option>
            {projects.map((project, index) => {
              const projectName = project.project_name || project.name;
              return (
                <option key={index} value={projectName}>
                  {projectName}
                </option>
              );
            })}
          </select>
        </div>

        {/* Checkpoints List */}
        {selectedProject && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h4 className={`text-md font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Available Checkpoints ({checkpoints.length})
              </h4>
              <div className="flex gap-2">
                <button
                  onClick={() => loadCheckpoints(selectedProject)}
                  disabled={loadingCheckpoints}
                  className={`p-2 ${darkMode ? 'text-blue-400 hover:bg-blue-900' : 'text-blue-600 hover:bg-blue-50'} rounded transition`}
                  title="Refresh checkpoints"
                >
                  <RefreshCw className={`w-4 h-4 ${loadingCheckpoints ? 'animate-spin' : ''}`} />
                </button>
                <button
                  onClick={handleCleanup}
                  disabled={!selectedProject || checkpoints.length === 0}
                  className={`px-3 py-1 text-xs rounded transition ${
                    darkMode 
                      ? 'bg-yellow-900 text-yellow-200 hover:bg-yellow-800' 
                      : 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                  }`}
                  title="Cleanup old checkpoints"
                >
                  <Archive className="w-3 h-3 inline mr-1" />
                  Cleanup
                </button>
              </div>
            </div>

            {loadingCheckpoints ? (
              <div className={`p-4 text-center ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" />
                Loading checkpoints...
              </div>
            ) : checkpoints.length === 0 ? (
              <div className={`p-4 text-center ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                No checkpoints found for this project
              </div>
            ) : (
              <div className="space-y-2">
                {checkpoints.map((checkpoint, index) => (
                  <div 
                    key={index}
                    className={`p-3 border rounded-lg flex items-center justify-between ${
                      darkMode 
                        ? 'bg-gray-700 border-gray-600 hover:bg-gray-650' 
                        : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                    } transition cursor-pointer`}
                    onClick={() => setSelectedCheckpoint(checkpoint)}
                  >
                    <div className="flex items-center">
                      <input
                        type="radio"
                        name="checkpoint"
                        value={checkpoint}
                        checked={selectedCheckpoint === checkpoint}
                        onChange={() => setSelectedCheckpoint(checkpoint)}
                        className="mr-3"
                      />
                      <div>
                        <p className={`text-sm font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                          {formatCheckpointName(checkpoint)}
                        </p>
                        <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                          {checkpoint}
                        </p>
                      </div>
                    </div>
                    {checkpoint.includes('final') && (
                      <span className={`px-2 py-1 text-xs rounded ${
                        darkMode 
                          ? 'bg-green-900 text-green-200' 
                          : 'bg-green-100 text-green-800'
                      }`}>
                        Final
                      </span>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Resume/Fine-tune Controls */}
            {checkpoints.length > 0 && (
              <div className="flex gap-3 mt-4">
                <button
                  onClick={() => setShowResumeModal(true)}
                  disabled={!selectedCheckpoint}
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 transition duration-200 flex items-center justify-center"
                >
                  <PlayCircle className="w-4 h-4 mr-2" />
                  Resume Training
                </button>
                <button
                  onClick={() => setShowResumeModal(true)}
                  disabled={!selectedCheckpoint}
                  className="flex-1 bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:bg-gray-400 transition duration-200 flex items-center justify-center"
                >
                  <GitBranch className="w-4 h-4 mr-2" />
                  Fine-tune
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Resume/Fine-tune Modal */}
      {showResumeModal && (
        <RLResumeModal
          isOpen={showResumeModal}
          onClose={() => setShowResumeModal(false)}
          selectedProject={selectedProject}
          selectedCheckpoint={selectedCheckpoint}
          projects={projects}
          darkMode={darkMode}
          resumeTraining={resumeTraining}
          isLoading={isLoading}
        />
      )}
    </div>
  );
};

// RL Resume/Fine-tune Modal Component
const RLResumeModal = ({ isOpen, onClose, selectedProject, selectedCheckpoint, projects, darkMode, resumeTraining, isLoading }) => {
  const [resumeConfig, setResumeConfig] = useState({
    project_name: selectedProject,
    checkpoint_path: selectedCheckpoint,
    fine_tune: false,
    new_env_config: null,
    training_options: {
      n_iters: 10,
      learning_rate: 0.0003,
      frames_per_batch: 6000
    }
  });

  const [targetProject, setTargetProject] = useState(selectedProject);

  useEffect(() => {
    setResumeConfig(prev => ({
      ...prev,
      project_name: selectedProject,
      checkpoint_path: selectedCheckpoint
    }));
    setTargetProject(selectedProject);
  }, [selectedProject, selectedCheckpoint]);

  const handleSubmit = async () => {
    try {
      // Prepare config for fine-tuning if needed
      const finalConfig = { ...resumeConfig };
      
      if (resumeConfig.fine_tune && targetProject !== selectedProject) {
        // Fine-tuning on different project
        const targetProjectData = projects.find(p => (p.project_name || p.name) === targetProject);
        if (targetProjectData) {
          finalConfig.new_env_config = {
            project_name: targetProject,
            udb_path: `/opt/understand_dbs/${targetProject}/${targetProjectData.version_id || 'latest'}/${targetProjectData.version_id || 'latest'}.und`,
            project_path: `/opt/projects/${targetProject}/${targetProjectData.version_id || 'latest'}`
          };
        }
      }

      await resumeTraining(finalConfig);
      onClose();
    } catch (error) {
      console.error('Failed to resume/fine-tune:', error);
    }
  };

  const inputClass = `w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
    darkMode 
      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
      : 'bg-white border-gray-300 text-gray-900'
  }`;

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto`}>
        <div className="flex items-center justify-between mb-6">
          <h3 className={`text-xl font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Resume/Fine-tune Training
          </h3>
          <button
            onClick={onClose}
            className={`p-2 ${darkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'} transition`}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-6">
          {/* Mode Selection */}
          <div>
            <label className={`block text-sm font-medium mb-3 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Training Mode
            </label>
            <div className="grid grid-cols-2 gap-4">
              <label className={`flex items-center p-4 border rounded-lg cursor-pointer ${
                !resumeConfig.fine_tune 
                  ? (darkMode ? 'bg-blue-900 border-blue-700' : 'bg-blue-50 border-blue-300')
                  : (darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-300')
              }`}>
                <input
                  type="radio"
                  name="mode"
                  checked={!resumeConfig.fine_tune}
                  onChange={() => setResumeConfig(prev => ({ ...prev, fine_tune: false }))}
                  className="mr-3"
                />
                <div>
                  <p className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>Resume Training</p>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Continue from checkpoint</p>
                </div>
              </label>
              
              <label className={`flex items-center p-4 border rounded-lg cursor-pointer ${
                resumeConfig.fine_tune 
                  ? (darkMode ? 'bg-purple-900 border-purple-700' : 'bg-purple-50 border-purple-300')
                  : (darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-300')
              }`}>
                <input
                  type="radio"
                  name="mode"
                  checked={resumeConfig.fine_tune}
                  onChange={() => setResumeConfig(prev => ({ ...prev, fine_tune: true }))}
                  className="mr-3"
                />
                <div>
                  <p className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>Fine-tune</p>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Adapt to new project</p>
                </div>
              </label>
            </div>
          </div>

          {/* Target Project (for fine-tuning) */}
          {resumeConfig.fine_tune && (
            <div>
              <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Target Project for Fine-tuning
              </label>
              <select
                value={targetProject}
                onChange={(e) => setTargetProject(e.target.value)}
                className={inputClass}
              >
                {projects.map((project, index) => {
                  const projectName = project.project_name || project.name;
                  return (
                    <option key={index} value={projectName}>
                      {projectName}
                    </option>
                  );
                })}
              </select>
            </div>
          )}

          {/* Training Options */}
          <div className={`border rounded-lg p-4 ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
            <h4 className={`text-md font-semibold mb-3 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Training Options</h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                  Iterations
                </label>
                <input
                  type="number"
                  value={resumeConfig.training_options.n_iters}
                  onChange={(e) => setResumeConfig(prev => ({
                    ...prev,
                    training_options: { ...prev.training_options, n_iters: parseInt(e.target.value) }
                  }))}
                  className={inputClass}
                />
              </div>
              <div>
                <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                  Learning Rate
                </label>
                <input
                  type="number"
                  step="0.0001"
                  value={resumeConfig.training_options.learning_rate}
                  onChange={(e) => setResumeConfig(prev => ({
                    ...prev,
                    training_options: { ...prev.training_options, learning_rate: parseFloat(e.target.value) }
                  }))}
                  className={inputClass}
                />
              </div>
              <div>
                <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                  Frames per Batch
                </label>
                <input
                  type="number"
                  value={resumeConfig.training_options.frames_per_batch}
                  onChange={(e) => setResumeConfig(prev => ({
                    ...prev,
                    training_options: { ...prev.training_options, frames_per_batch: parseInt(e.target.value) }
                  }))}
                  className={inputClass}
                />
              </div>
            </div>
          </div>

          {/* Checkpoint Info */}
          <div className={`p-4 border rounded-lg ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
            <h4 className={`text-sm font-medium mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Checkpoint Information</h4>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              <strong>Source Project:</strong> {selectedProject}
            </p>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              <strong>Checkpoint:</strong> {selectedCheckpoint}
            </p>
            {resumeConfig.fine_tune && targetProject !== selectedProject && (
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} mt-2`}>
                <strong>Note:</strong> Model will be fine-tuned for project "{targetProject}"
              </p>
            )}
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className={`flex-1 px-4 py-2 border rounded-md transition ${
                darkMode
                  ? 'border-gray-600 text-gray-300 hover:bg-gray-700'
                  : 'border-gray-300 text-gray-700 hover:bg-gray-50'
              }`}
            >
              Cancel
            </button>
            <button
              onClick={handleSubmit}
              disabled={isLoading}
              className={`flex-1 px-4 py-2 rounded-md transition ${
                resumeConfig.fine_tune
                  ? 'bg-purple-600 hover:bg-purple-700'
                  : 'bg-blue-600 hover:bg-blue-700'
              } text-white disabled:bg-gray-400 flex items-center justify-center`}
            >
              {isLoading ? (
                <RefreshCw className="w-4 h-4 animate-spin mr-2" />
              ) : resumeConfig.fine_tune ? (
                <GitBranch className="w-4 h-4 mr-2" />
              ) : (
                <PlayCircle className="w-4 h-4 mr-2" />
              )}
              {resumeConfig.fine_tune ? 'Start Fine-tuning' : 'Resume Training'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Enhanced Task Card with RL Management Controls
const EnhancedTaskCard = ({ task, darkMode, onCancel, onRefresh, stopTraining }) => {
  const isRLTask = task.type === 'RL_TRAINING' || task.type === 'RL_RESUME' || task.type === 'RL_FINE_TUNE';
  const canStop = task.status === 'PROGRESS' || task.status === 'PENDING';

  return (
    <div className={`p-6 ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50'} transition`}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h4 className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              {task.project_name}
            </h4>
            <StatusBadge status={task.status} darkMode={darkMode} />
            {isRLTask && (
              <span className={`px-2 py-1 text-xs rounded ${
                task.type === 'RL_FINE_TUNE' 
                  ? (darkMode ? 'bg-purple-900 text-purple-200' : 'bg-purple-100 text-purple-800')
                  : task.type === 'RL_RESUME'
                  ? (darkMode ? 'bg-blue-900 text-blue-200' : 'bg-blue-100 text-blue-800') 
                  : (darkMode ? 'bg-green-900 text-green-200' : 'bg-green-100 text-green-800')
              }`}>
                {task.type === 'RL_FINE_TUNE' ? 'Fine-tune' : task.type === 'RL_RESUME' ? 'Resume' : 'RL'}
              </span>
            )}
          </div>
          <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} space-y-1`}>
            <p>Task ID: <span className="font-mono">{task.task_id}</span></p>
            <p>Type: {task.type}</p>
            <p>Started: {new Date(task.timestamp).toLocaleString()}</p>
          </div>
          
          {(task.status === 'PROGRESS' && task.progress !== undefined) && (
            <div className="mt-4">
              <ProgressBar 
                progress={task.progress} 
                label={`Training Progress (Iteration ${task.current_iteration || 'N/A'})`}
                color={isRLTask ? "green" : "blue"} 
                darkMode={darkMode} 
              />
            </div>
          )}
          
          {task.error && (
            <div className={`mt-3 p-3 ${darkMode ? 'bg-red-900 border-red-700' : 'bg-red-50 border-red-200'} border rounded-md`}>
              <p className={`text-sm ${darkMode ? 'text-red-200' : 'text-red-800'}`}>{task.error}</p>
            </div>
          )}
        </div>
        
        <div className="flex items-center gap-2 ml-4">
          <button
            onClick={onRefresh}
            className={`p-2 ${darkMode ? 'text-blue-400 hover:bg-blue-900' : 'text-blue-600 hover:bg-blue-50'} rounded transition`}
            title="Refresh Status"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
          
          {isRLTask && canStop && (
            <button
              onClick={() => stopTraining(task.task_id, true)}
              className={`p-2 ${darkMode ? 'text-yellow-400 hover:bg-yellow-900' : 'text-yellow-600 hover:bg-yellow-50'} rounded transition`}
              title="Stop with Checkpoint"
            >
              <Square className="w-4 h-4" />
            </button>
          )}
          
          {canStop && (
            <button
              onClick={() => onCancel(task.task_id)}
              className={`p-2 ${darkMode ? 'text-red-400 hover:bg-red-900' : 'text-red-600 hover:bg-red-50'} rounded transition`}
              title="Cancel Task"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

// Task Card Component
const TaskCard = ({ task, darkMode, onCancel, onRefresh }) => (
  <div className={`p-6 ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50'} transition`}>
    <div className="flex items-center justify-between">
      <div className="flex-1">
        <div className="flex items-center gap-3 mb-2">
          <h4 className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            {task.project_name}
          </h4>
          <StatusBadge status={task.status} darkMode={darkMode} />
        </div>
        <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} space-y-1`}>
          <p>Task ID: <span className="font-mono">{task.task_id}</span></p>
          <p>Type: {task.type}</p>
          <p>Started: {new Date(task.timestamp).toLocaleString()}</p>
        </div>
        
        {(task.status === 'PROGRESS' && task.progress !== undefined) && (
          <div className="mt-4">
            <ProgressBar 
              progress={task.progress} 
              label={`Training Progress (Iteration ${task.current_iteration || 'N/A'})`}
              color="green" 
              darkMode={darkMode} 
            />
          </div>
        )}
        
        {task.error && (
          <div className={`mt-3 p-3 ${darkMode ? 'bg-red-900 border-red-700' : 'bg-red-50 border-red-200'} border rounded-md`}>
            <p className={`text-sm ${darkMode ? 'text-red-200' : 'text-red-800'}`}>{task.error}</p>
          </div>
        )}
      </div>
      
      <div className="flex items-center gap-2 ml-4">
        <button
          onClick={onRefresh}
          className={`p-2 ${darkMode ? 'text-blue-400 hover:bg-blue-900' : 'text-blue-600 hover:bg-blue-50'} rounded transition`}
          title="Refresh Status"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
        {(task.status === 'PROGRESS' || task.status === 'PENDING') && (
          <button
            onClick={() => onCancel(task.task_id)}
            className={`p-2 ${darkMode ? 'text-red-400 hover:bg-red-900' : 'text-red-600 hover:bg-red-50'} rounded transition`}
            title="Cancel Task"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  </div>
);

// Testability Training Form Component
const TestabilityTrainingForm = ({ onSubmit, projects, fetchAvailableDatasets, darkMode, isLoading }) => {
  const [trainingConfig, setTrainingConfig] = useState({
    dataset_path: '',
    ds_number: 8,
    model_version: '',
    project_name: ''
  });
  const [availableDatasets, setAvailableDatasets] = useState([]);
  const [loadingDatasets, setLoadingDatasets] = useState(false);
  const [selectedProject, setSelectedProject] = useState('');
  const [availableVersions, setAvailableVersions] = useState([]);
  
  // Get available versions for selected project
  const getProjectVersions = (projectName) => {
    const project = projects.find(p => (p.project_name || p.name) === projectName);
    if (project && project.versions) {
      return project.versions;
    } else if (project && project.version_id) {
      return [{ version_id: project.version_id }];
    }
    return [];
  };
  
  // Update available versions when project changes
  useEffect(() => {
    if (selectedProject) {
      const versions = getProjectVersions(selectedProject);
      setAvailableVersions(versions);
      
      // Auto-select latest version if available
      if (versions.length > 0 && !trainingConfig.model_version) {
        const project = projects.find(p => (p.project_name || p.name) === selectedProject);
        const latestVersion = project?.latest_version || versions[0]?.version_id;
        if (latestVersion) {
          setTrainingConfig(prev => ({ ...prev, model_version: latestVersion }));
        }
      }
    } else {
      setAvailableVersions([]);
    }
  }, [selectedProject, projects]);

  // Fetch datasets when component mounts or projects change
  useEffect(() => {
    const loadDatasets = async () => {
      if (projects.length > 0) {
        setLoadingDatasets(true);
        try {
          const datasets = await fetchAvailableDatasets();
          setAvailableDatasets(datasets);
        } catch (error) {
          console.error('Failed to load datasets:', error);
          setAvailableDatasets([]);
        } finally {
          setLoadingDatasets(false);
        }
      }
    };
    
    loadDatasets();
  }, [projects, fetchAvailableDatasets]);

  const handleSubmit = async () => {
    if (!trainingConfig.dataset_path) {
      alert('Please select a dataset');
      return;
    }
    await onSubmit(trainingConfig);
  };

  const handleRefreshDatasets = async () => {
    setLoadingDatasets(true);
    try {
      const datasets = await fetchAvailableDatasets();
      setAvailableDatasets(datasets);
    } catch (error) {
      console.error('Failed to refresh datasets:', error);
    } finally {
      setLoadingDatasets(false);
    }
  };

  const inputClass = `w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
    darkMode 
      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
      : 'bg-white border-gray-300 text-gray-900'
  }`;

  return (
    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
      <h3 className={`text-lg font-semibold mb-6 flex items-center ${darkMode ? 'text-white' : 'text-gray-900'}`}>
        <Target className="w-5 h-5 mr-2 text-purple-600" />
        Start Testability Model Training
      </h3>

      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className={`block text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Dataset Path *
              </label>
              <button
                onClick={handleRefreshDatasets}
                disabled={loadingDatasets}
                className={`p-1 ${darkMode ? 'text-gray-400 hover:text-blue-400' : 'text-gray-600 hover:text-blue-600'} transition`}
                title="Refresh datasets"
              >
                <RefreshCw className={`w-3 h-3 ${loadingDatasets ? 'animate-spin' : ''}`} />
              </button>
            </div>
            <select
              value={trainingConfig.dataset_path}
              onChange={(e) => setTrainingConfig(prev => ({...prev, dataset_path: e.target.value}))}
              className={inputClass}
              disabled={loadingDatasets}
            >
              <option value="">
                {loadingDatasets ? 'Loading datasets...' : 'Select available dataset...'}
              </option>
              {availableDatasets.map((dataset, index) => (
                <option key={index} value={dataset.file_path}>
                  {dataset.display_name}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Dataset Number
            </label>
            <input
              type="number"
              value={trainingConfig.ds_number}
              onChange={(e) => setTrainingConfig(prev => ({...prev, ds_number: parseInt(e.target.value)}))}
              className={inputClass}
              min="1"
              max="20"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Project Name
            </label>
            <select
              value={selectedProject}
              onChange={(e) => {
                setSelectedProject(e.target.value);
                setTrainingConfig(prev => ({
                  ...prev, 
                  project_name: e.target.value,
                  model_version: '' // Reset version when project changes
                }));
              }}
              className={inputClass}
            >
              <option value="">Select project (optional)...</option>
              {projects.map((project, index) => {
                const projectName = project.project_name || project.name;
                const versionCount = project.versions ? project.versions.length : 1;
                return (
                  <option key={index} value={projectName}>
                    {projectName} ({versionCount} version{versionCount > 1 ? 's' : ''})
                  </option>
                );
              })}
            </select>
          </div>
          
          <div>
            <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Model Version
            </label>
            <select
              value={trainingConfig.model_version}
              onChange={(e) => setTrainingConfig(prev => ({...prev, model_version: e.target.value}))}
              className={inputClass}
              disabled={!selectedProject}
            >
              <option value="">Select version (optional)...</option>
              {availableVersions.map((version, index) => (
                <option key={index} value={version.version_id}>
                  {version.version_id} {version.upload_date && `(${new Date(version.upload_date).toLocaleDateString()})`}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className={`border rounded-lg p-4 ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
          <h4 className={`text-md font-semibold mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Training Info</h4>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            This training will create 4 different testability prediction models:
          </p>
          <ul className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} mt-2 space-y-1`}>
            <li>• <strong>RFR1</strong> - Random Forest Regressor</li>
            <li>• <strong>HGBR1</strong> - Histogram Gradient Boosting Regressor</li>
            <li>• <strong>MLPR1</strong> - Multi-layer Perceptron Regressor</li>
            <li>• <strong>VR1</strong> - Voting Regressor (ensemble)</li>
          </ul>
        </div>

        <button
          onClick={handleSubmit}
          disabled={!trainingConfig.dataset_path || isLoading}
          className="w-full bg-purple-600 text-white py-3 px-4 rounded-md hover:bg-purple-700 disabled:bg-gray-400 transition duration-200 flex items-center justify-center text-lg font-medium"
        >
          {isLoading ? (
            <>
              <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
              Starting Training...
            </>
          ) : (
            <>
              <Target className="w-5 h-5 mr-2" />
              Start Testability Training
            </>
          )}
        </button>
      </div>
    </div>
  );
};

// Metrics Export Form Component
const MetricsExportForm = ({ onSubmit, projects, darkMode, isLoading }) => {
  const [exportConfig, setExportConfig] = useState({
    project_name: '',
    version_id: '',
    metric_types: ['testability'],
    n_jobs: 1
  });
  const [availableVersions, setAvailableVersions] = useState([]);
  
  // Get available versions for selected project
  const getProjectVersions = (projectName) => {
    const project = projects.find(p => (p.project_name || p.name) === projectName);
    if (project && project.versions) {
      return project.versions;
    } else if (project && project.version_id) {
      return [{ version_id: project.version_id }];
    }
    return [];
  };
  
  // Update available versions when project changes
  useEffect(() => {
    if (exportConfig.project_name) {
      const versions = getProjectVersions(exportConfig.project_name);
      setAvailableVersions(versions);
      
      // Auto-select latest version if available
      if (versions.length > 0 && !exportConfig.version_id) {
        const project = projects.find(p => (p.project_name || p.name) === exportConfig.project_name);
        const latestVersion = project?.latest_version || versions[0]?.version_id;
        if (latestVersion) {
          setExportConfig(prev => ({ ...prev, version_id: latestVersion }));
        }
      }
    } else {
      setAvailableVersions([]);
    }
  }, [exportConfig.project_name, projects]);

  const handleSubmit = async () => {
    if (!exportConfig.project_name) {
      alert('Please select a project');
      return;
    }
    await onSubmit(exportConfig);
  };

  const inputClass = `w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
    darkMode 
      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
      : 'bg-white border-gray-300 text-gray-900'
  }`;

  return (
    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
      <h3 className={`text-lg font-semibold mb-6 flex items-center ${darkMode ? 'text-white' : 'text-gray-900'}`}>
        <TrendingUp className="w-5 h-5 mr-2 text-orange-600" />
        Export Metrics
      </h3>

      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Project *
            </label>
            <select
              value={exportConfig.project_name}
              onChange={(e) => {
                setExportConfig(prev => ({
                  ...prev, 
                  project_name: e.target.value,
                  version_id: '' // Reset version when project changes
                }));
              }}
              className={inputClass}
            >
              <option value="">Select project...</option>
              {projects.map((project, index) => {
                const projectName = project.project_name || project.name;
                const versionCount = project.versions ? project.versions.length : 1;
                return (
                  <option key={index} value={projectName}>
                    {projectName} ({versionCount} version{versionCount > 1 ? 's' : ''})
                  </option>
                );
              })}
            </select>
          </div>
          
          <div>
            <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Version *
            </label>
            <select
              value={exportConfig.version_id}
              onChange={(e) => setExportConfig(prev => ({...prev, version_id: e.target.value}))}
              className={inputClass}
              disabled={!exportConfig.project_name}
            >
              <option value="">Select version...</option>
              {availableVersions.map((version, index) => (
                <option key={index} value={version.version_id}>
                  {version.version_id} {version.upload_date && `(${new Date(version.upload_date).toLocaleDateString()})`}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div>
          <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Metric Types
          </label>
          <div className="space-y-2">
            {['testability', 'evosuite'].map(metricType => (
              <label key={metricType} className="flex items-center">
                <input
                  type="checkbox"
                  checked={exportConfig.metric_types.includes(metricType)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setExportConfig(prev => ({
                        ...prev,
                        metric_types: [...prev.metric_types, metricType]
                      }));
                    } else {
                      setExportConfig(prev => ({
                        ...prev,
                        metric_types: prev.metric_types.filter(t => t !== metricType)
                      }));
                    }
                  }}
                  className="mr-2"
                />
                <span className={`capitalize ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                  {metricType}
                </span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Number of Jobs (Parallel Processing)
          </label>
          <input
            type="number"
            value={exportConfig.n_jobs}
            onChange={(e) => setExportConfig(prev => ({...prev, n_jobs: parseInt(e.target.value)}))}
            className={inputClass}
            min="1"
            max="8"
          />
        </div>

        <button
          onClick={handleSubmit}
          disabled={!exportConfig.project_name || !exportConfig.version_id || exportConfig.metric_types.length === 0 || isLoading}
          className="w-full bg-orange-600 text-white py-3 px-4 rounded-md hover:bg-orange-700 disabled:bg-gray-400 transition duration-200 flex items-center justify-center text-lg font-medium"
        >
          {isLoading ? (
            <>
              <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
              Exporting...
            </>
          ) : (
            <>
              <TrendingUp className="w-5 h-5 mr-2" />
              Export Metrics
            </>
          )}
        </button>
      </div>
    </div>
  );
};

// Metrics Download Section Component
const MetricsDownloadSection = ({ availableMetrics, projects, darkMode, onDownload, onRefresh }) => {
  const [selectedProject, setSelectedProject] = useState('');
  const [selectedVersion, setSelectedVersion] = useState('');
  const [availableVersions, setAvailableVersions] = useState([]);
  
  // Get available versions for selected project
  const getProjectVersions = (projectName) => {
    const project = projects.find(p => (p.project_name || p.name) === projectName);
    if (project && project.versions) {
      return project.versions;
    } else if (project && project.version_id) {
      return [{ version_id: project.version_id }];
    }
    return [];
  };
  
  // Update available versions when project changes
  useEffect(() => {
    if (selectedProject) {
      const versions = getProjectVersions(selectedProject);
      setAvailableVersions(versions);
      
      // Auto-select latest version if available
      if (versions.length > 0 && !selectedVersion) {
        const project = projects.find(p => (p.project_name || p.name) === selectedProject);
        const latestVersion = project?.latest_version || versions[0]?.version_id;
        if (latestVersion) {
          setSelectedVersion(latestVersion);
        }
      }
    } else {
      setAvailableVersions([]);
      setSelectedVersion('');
    }
  }, [selectedProject, projects]);

  const handleDownload = (type, project, version, fileName) => {
    let endpoint = '';
    
    switch (type) {
      case 'metrics':
        if (project && version) {
          endpoint = `/api/v1/download/metrics/${project}?version_id=${version}`;
        } else if (project) {
          endpoint = `/api/v1/download/metrics/${project}`;
        }
        break;
      case 'models':
        if (project && version) {
          endpoint = `/api/v1/download/joblib/${project}/${version}`;
        } else if (project) {
          endpoint = `/api/v1/download/models/${project}`;
        }
        break;
      case 'codesmells':
        if (project && version) {
          endpoint = `/api/v1/download/codesmells/${project}?version_id=${version}`;
        } else if (project) {
          endpoint = `/api/v1/download/codesmells/${project}`;
        }
        break;
      default:
        return;
    }
    
    onDownload(endpoint, fileName || `${project}-${type}.zip`);
  };

  return (
    <div className="space-y-6">
      {/* Download Controls */}
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
        <div className="flex items-center justify-between mb-6">
          <h3 className={`text-lg font-semibold flex items-center ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            <Download className="w-5 h-5 mr-2 text-blue-600" />
            Download Files
          </h3>
          <button
            onClick={onRefresh}
            className={`p-2 ${darkMode ? 'text-gray-400 hover:text-blue-400 hover:bg-gray-700' : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'} rounded transition`}
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Project
            </label>
            <select
              value={selectedProject}
              onChange={(e) => {
                setSelectedProject(e.target.value);
                setSelectedVersion(''); // Reset version when project changes
              }}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                darkMode 
                  ? 'bg-gray-700 border-gray-600 text-white' 
                  : 'bg-white border-gray-300 text-gray-900'
              }`}
            >
              <option value="">All projects</option>
              {projects.map((project, index) => {
                const projectName = project.project_name || project.name;
                const versionCount = project.versions ? project.versions.length : 1;
                return (
                  <option key={index} value={projectName}>
                    {projectName} ({versionCount} version{versionCount > 1 ? 's' : ''})
                  </option>
                );
              })}
            </select>
          </div>
          
          <div>
            <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Version
            </label>
            <select
              value={selectedVersion}
              onChange={(e) => setSelectedVersion(e.target.value)}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                darkMode 
                  ? 'bg-gray-700 border-gray-600 text-white' 
                  : 'bg-white border-gray-300 text-gray-900'
              }`}
              disabled={!selectedProject}
            >
              <option value="">All versions</option>
              {availableVersions.map((version, index) => (
                <option key={index} value={version.version_id}>
                  {version.version_id} {version.upload_date && `(${new Date(version.upload_date).toLocaleDateString()})`}
                </option>
              ))}
            </select>
          </div>
          
          <div className="flex items-end">
            <div className="grid grid-cols-3 gap-2 w-full">
              <button
                onClick={() => handleDownload('metrics', selectedProject, selectedVersion)}
                className="bg-green-600 text-white py-2 px-3 rounded-md hover:bg-green-700 transition text-sm"
              >
                Metrics
              </button>
              <button
                onClick={() => handleDownload('models', selectedProject, selectedVersion)}
                className="bg-purple-600 text-white py-2 px-3 rounded-md hover:bg-purple-700 transition text-sm"
              >
                Models
              </button>
              <button
                onClick={() => handleDownload('codesmells', selectedProject, selectedVersion)}
                className="bg-red-600 text-white py-2 px-3 rounded-md hover:bg-red-700 transition text-sm"
              >
                Smells
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Available Metrics List */}
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg`}>
        <div className={`px-6 py-4 border-b ${darkMode ? 'bg-gray-900 border-gray-700' : 'bg-gray-50 border-gray-200'}`}>
          <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Available Metrics</h3>
        </div>
        
        <div className={`divide-y ${darkMode ? 'divide-gray-700' : 'divide-gray-200'}`}>
          {availableMetrics.length === 0 ? (
            <div className="p-12 text-center">
              <BarChart3 className={`w-16 h-16 mx-auto ${darkMode ? 'text-gray-600' : 'text-gray-300'} mb-4`} />
              <p className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>No metrics available. Export some metrics first!</p>
            </div>
          ) : (
            availableMetrics.map((metric, index) => (
              <div key={index} className={`p-4 ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50'} transition`}>
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h4 className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      {metric.project_name} - {metric.metric_type}
                    </h4>
                    <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} mt-1 space-y-1`}>
                      <p>File: {metric.name}</p>
                      <p>Size: {(metric.size / 1024).toFixed(2)} KB</p>
                      <p>Modified: {new Date(metric.last_modified).toLocaleString()}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => onDownload(metric.path, metric.name)}
                    className={`p-2 ${darkMode ? 'text-blue-400 hover:bg-blue-900' : 'text-blue-600 hover:bg-blue-50'} rounded transition`}
                    title="Download File"
                  >
                    <Download className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

// Refactoring Prediction Form Component
const RefactoringPredictionForm = ({ onSubmit, projects, darkMode, isLoading, getAvailableModels, loadModelForInference }) => {
  const [predictionConfig, setPredictionConfig] = useState({
    project_name: '',
    model_checkpoint: '',
    max_steps: 10,
    temperature: 1.0
  });
  const [availableModels, setAvailableModels] = useState([]);
  const [loadingModels, setLoadingModels] = useState(false);
  const [selectedModel, setSelectedModel] = useState(null);

  const loadModels = async (projectName) => {
    if (!projectName) return;
    
    setLoadingModels(true);
    try {
      const models = await getAvailableModels(projectName);
      setAvailableModels(models);
      
      // Auto-select latest model if available
      if (models.length > 0) {
        const latestModel = models[0]; // Already sorted by modification time
        setPredictionConfig(prev => ({
          ...prev,
          model_checkpoint: latestModel.checkpoint_path
        }));
        setSelectedModel(latestModel);
      }
    } catch (error) {
      console.error('Failed to load models:', error);
      setAvailableModels([]);
    } finally {
      setLoadingModels(false);
    }
  };

  const handleProjectChange = (projectName) => {
    setPredictionConfig(prev => ({
      ...prev,
      project_name: projectName,
      model_checkpoint: ''
    }));
    setAvailableModels([]);
    setSelectedModel(null);
    
    if (projectName) {
      loadModels(projectName);
    }
  };

  const handleSubmit = async () => {
    if (!predictionConfig.project_name) {
      alert('Please select a project');
      return;
    }
    
    if (!predictionConfig.model_checkpoint) {
      alert('Please select a model checkpoint');
      return;
    }

    await onSubmit(predictionConfig);
  };

  const formatModelName = (model) => {
    const parts = model.checkpoint_path.split('/');
    const filename = parts[parts.length - 1];
    return filename.replace('checkpoint_', '').replace('.pth', '');
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const inputClass = `w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
    darkMode 
      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
      : 'bg-white border-gray-300 text-gray-900'
  }`;

  return (
    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
      <h3 className={`text-lg font-semibold mb-6 flex items-center ${darkMode ? 'text-white' : 'text-gray-900'}`}>
        <Sparkles className="w-5 h-5 mr-2 text-purple-600" />
        Generate Refactoring Sequence Predictions
      </h3>

      <div className="space-y-6">
        {/* Project Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Select Project *
            </label>
            <select
              value={predictionConfig.project_name}
              onChange={(e) => handleProjectChange(e.target.value)}
              className={inputClass}
            >
              <option value="">Choose a project...</option>
              {projects.map((project, index) => {
                const projectName = project.project_name || project.name;
                return (
                  <option key={index} value={projectName}>
                    {projectName}
                  </option>
                );
              })}
            </select>
          </div>

          <div>
            <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Max Refactoring Steps
            </label>
            <input
              type="number"
              value={predictionConfig.max_steps}
              onChange={(e) => setPredictionConfig(prev => ({
                ...prev,
                max_steps: parseInt(e.target.value) || 10
              }))}
              className={inputClass}
              min="1"
              max="50"
            />
          </div>
        </div>

        {/* Model Selection */}
        {predictionConfig.project_name && (
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className={`block text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Select Model Checkpoint *
              </label>
              <button
                onClick={() => loadModels(predictionConfig.project_name)}
                disabled={loadingModels}
                className={`p-1 ${darkMode ? 'text-gray-400 hover:text-blue-400' : 'text-gray-600 hover:text-blue-600'} transition`}
                title="Refresh models"
              >
                <RefreshCw className={`w-3 h-3 ${loadingModels ? 'animate-spin' : ''}`} />
              </button>
            </div>
            
            {loadingModels ? (
              <div className={`p-4 text-center ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" />
                Loading available models...
              </div>
            ) : availableModels.length === 0 ? (
              <div className={`p-4 text-center ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                <Brain className="w-8 h-8 mx-auto mb-2" />
                No trained models found for this project. Train a model first!
              </div>
            ) : (
              <div className="space-y-2">
                {availableModels.map((model, index) => (
                  <div
                    key={index}
                    className={`p-3 border rounded-lg cursor-pointer transition ${
                      predictionConfig.model_checkpoint === model.checkpoint_path
                        ? (darkMode ? 'bg-purple-900 border-purple-700' : 'bg-purple-50 border-purple-300')
                        : (darkMode ? 'bg-gray-700 border-gray-600 hover:bg-gray-650' : 'bg-gray-50 border-gray-200 hover:bg-gray-100')
                    }`}
                    onClick={() => {
                      setPredictionConfig(prev => ({
                        ...prev,
                        model_checkpoint: model.checkpoint_path
                      }));
                      setSelectedModel(model);
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <input
                          type="radio"
                          name="model"
                          value={model.checkpoint_path}
                          checked={predictionConfig.model_checkpoint === model.checkpoint_path}
                          onChange={() => {
                            setPredictionConfig(prev => ({
                              ...prev,
                              model_checkpoint: model.checkpoint_path
                            }));
                            setSelectedModel(model);
                          }}
                          className="mr-3"
                        />
                        <div>
                          <p className={`text-sm font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                            {formatModelName(model)}
                          </p>
                          <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                            {formatFileSize(model.size)} • {new Date(model.last_modified).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      {model.checkpoint_path.includes('final') && (
                        <span className={`px-2 py-1 text-xs rounded ${
                          darkMode 
                            ? 'bg-green-900 text-green-200' 
                            : 'bg-green-100 text-green-800'
                        }`}>
                          Final
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Advanced Options */}
        <div className={`border rounded-lg p-4 ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
          <h4 className={`text-md font-semibold mb-3 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Advanced Options</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Temperature (Sampling Randomness)
              </label>
              <input
                type="number"
                step="0.1"
                min="0.1"
                max="2.0"
                value={predictionConfig.temperature}
                onChange={(e) => setPredictionConfig(prev => ({
                  ...prev,
                  temperature: parseFloat(e.target.value) || 1.0
                }))}
                className={inputClass}
              />
              <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-500'} mt-1`}>
                Lower = more deterministic, Higher = more random
              </p>
            </div>
            
            <div>
              <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Confidence Threshold
              </label>
              <input
                type="number"
                step="0.1"
                min="0.1"
                max="1.0"
                value={0.3}
                disabled
                className={`${inputClass} opacity-50`}
              />
              <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-500'} mt-1`}>
                Fixed at 0.3 for now
              </p>
            </div>
          </div>
        </div>

        {/* Model Info */}
        {selectedModel && (
          <div className={`border rounded-lg p-4 ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
            <h4 className={`text-sm font-medium mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Selected Model Info</h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  <strong>Model:</strong> {formatModelName(selectedModel)}
                </p>
                <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  <strong>Size:</strong> {formatFileSize(selectedModel.size)}
                </p>
              </div>
              <div>
                <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  <strong>Created:</strong> {new Date(selectedModel.last_modified).toLocaleString()}
                </p>
                <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  <strong>Path:</strong> {selectedModel.checkpoint_name}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button
          onClick={handleSubmit}
          disabled={!predictionConfig.project_name || !predictionConfig.model_checkpoint || isLoading}
          className="w-full bg-purple-600 text-white py-3 px-4 rounded-md hover:bg-purple-700 disabled:bg-gray-400 transition duration-200 flex items-center justify-center text-lg font-medium"
        >
          {isLoading ? (
            <>
              <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
              Generating Predictions...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5 mr-2" />
              Generate Refactoring Predictions
            </>
          )}
        </button>
      </div>
    </div>
  );
};

// Prediction Results Section Component
const PredictionResultsSection = ({ predictionResults, predictionHistory, darkMode, onClearHistory, setPredictionResults }) => {
  const [selectedPrediction, setSelectedPrediction] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  const getRefactoringTypeColor = (type) => {
    const colors = {
      'Move Method': 'bg-blue-100 text-blue-800',
      'Extract Class': 'bg-green-100 text-green-800',
      'Extract Method': 'bg-purple-100 text-purple-800',
      'Pull Up Method': 'bg-orange-100 text-orange-800',
      'Push Down Method': 'bg-red-100 text-red-800',
      'Move Class': 'bg-indigo-100 text-indigo-800'
    };
    
    const darkColors = {
      'Move Method': 'bg-blue-900 text-blue-200',
      'Extract Class': 'bg-green-900 text-green-200',
      'Extract Method': 'bg-purple-900 text-purple-200',
      'Pull Up Method': 'bg-orange-900 text-orange-200',
      'Push Down Method': 'bg-red-900 text-red-200',
      'Move Class': 'bg-indigo-900 text-indigo-200'
    };
    
    return darkMode ? (darkColors[type] || 'bg-gray-700 text-gray-300') : (colors[type] || 'bg-gray-100 text-gray-800');
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.7) return darkMode ? 'text-green-400' : 'text-green-600';
    if (confidence >= 0.5) return darkMode ? 'text-yellow-400' : 'text-yellow-600';
    return darkMode ? 'text-red-400' : 'text-red-600';
  };

  const formatImprovement = (improvement) => {
    if (!improvement) return 'N/A';
    const entries = Object.entries(improvement);
    if (entries.length === 0) return 'N/A';
    
    const topImprovement = entries.reduce((max, [key, value]) => 
      Math.abs(value) > Math.abs(max[1]) ? [key, value] : max
    );
    
    return `${topImprovement[0]}: ${topImprovement[1] >= 0 ? '+' : ''}${topImprovement[1].toFixed(3)}`;
  };

  return (
    <div className="space-y-6">
      {/* Current Results */}
      {predictionResults.length > 0 && (
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg`}>
          <div className={`px-6 py-4 border-b ${darkMode ? 'bg-gray-900 border-gray-700' : 'bg-gray-50 border-gray-200'}`}>
            <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Latest Prediction Results
            </h3>
          </div>
          
          {predictionResults.map((result, index) => (
            <div key={index} className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h4 className={`text-lg font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    {result.project_name}
                  </h4>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    Model: {result.model_checkpoint} • {result.predictions.length} recommendations
                  </p>
                </div>
                <div className="text-right">
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    Generated: {new Date(result.timestamp).toLocaleString()}
                  </p>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    Execution: {result.execution_time?.toFixed(2)}s
                  </p>
                </div>
              </div>

              {/* Recommendations */}
              <div className="space-y-3">
                {result.predictions.map((prediction, idx) => (
                  <div 
                    key={idx} 
                    className={`p-4 border rounded-lg transition cursor-pointer ${
                      darkMode 
                        ? 'bg-gray-700 border-gray-600 hover:bg-gray-650' 
                        : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                    }`}
                    onClick={() => {
                      setSelectedPrediction(prediction);
                      setShowDetails(true);
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <span className={`px-2 py-1 text-xs font-medium rounded ${
                          darkMode ? 'bg-gray-600 text-gray-200' : 'bg-gray-200 text-gray-800'
                        }`}>
                          Step {prediction.step}
                        </span>
                        <span className={`px-2 py-1 text-xs font-medium rounded ${getRefactoringTypeColor(prediction.refactoring_type)}`}>
                          {prediction.refactoring_type}
                        </span>
                        <span className={`text-sm font-medium ${getConfidenceColor(prediction.confidence)}`}>
                          {(prediction.confidence * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                          {formatImprovement(prediction.expected_improvement)}
                        </span>
                        <ChevronRight className={`w-4 h-4 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`} />
                      </div>
                    </div>
                    
                    <div className="mt-2">
                      <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                        Target: {prediction.target_class}
                        {prediction.target_method && ` → ${prediction.target_method}`}
                      </p>
                      <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'} mt-1`}>
                        {prediction.rationale}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Total Improvement Summary */}
              {result.total_expected_improvement && (
                <div className={`mt-4 p-4 border rounded-lg ${
                  darkMode ? 'bg-gray-700 border-gray-600' : 'bg-blue-50 border-blue-200'
                }`}>
                  <h5 className={`text-sm font-medium mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    Total Expected Improvement
                  </h5>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    {Object.entries(result.total_expected_improvement).map(([objective, value]) => (
                      <div key={objective} className="text-center">
                        <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                          {objective}
                        </p>
                        <p className={`text-sm font-medium ${value >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {value >= 0 ? '+' : ''}{value.toFixed(3)}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Prediction History */}
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg`}>
        <div className={`px-6 py-4 border-b ${darkMode ? 'bg-gray-900 border-gray-700' : 'bg-gray-50 border-gray-200'}`}>
          <div className="flex items-center justify-between">
            <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Prediction History
            </h3>
            <div className="flex items-center space-x-2">
              <button
                onClick={onClearHistory}
                className={`px-3 py-1 text-xs rounded transition ${
                  darkMode 
                    ? 'bg-red-900 text-red-200 hover:bg-red-800' 
                    : 'bg-red-100 text-red-800 hover:bg-red-200'
                }`}
              >
                Clear History
              </button>
            </div>
          </div>
        </div>

        <div className={`divide-y ${darkMode ? 'divide-gray-700' : 'divide-gray-200'}`}>
          {predictionHistory.length === 0 ? (
            <div className="p-12 text-center">
              <History className={`w-16 h-16 mx-auto ${darkMode ? 'text-gray-600' : 'text-gray-300'} mb-4`} />
              <p className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                No prediction history yet. Generate your first prediction above!
              </p>
            </div>
          ) : (
            predictionHistory.map((prediction, index) => (
              <div 
                key={index} 
                className={`p-4 ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50'} transition cursor-pointer`}
                onClick={() => setPredictionResults([prediction])}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h4 className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                        {prediction.project_name}
                      </h4>
                      <span className={`px-2 py-1 text-xs rounded ${
                        darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'
                      }`}>
                        {prediction.predictions.length} recommendations
                      </span>
                    </div>
                    <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} space-y-1`}>
                      <p>Generated: {new Date(prediction.timestamp).toLocaleString()}</p>
                      <p>Model: {prediction.model_checkpoint}</p>
                      <p>Execution: {prediction.execution_time?.toFixed(2)}s</p>
                    </div>
                  </div>
                  <ChevronRight className={`w-4 h-4 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`} />
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Prediction Details Modal */}
      {showDetails && selectedPrediction && (
        <PredictionDetailsModal
          prediction={selectedPrediction}
          isOpen={showDetails}
          onClose={() => setShowDetails(false)}
          darkMode={darkMode}
        />
      )}
    </div>
  );
};

// Prediction Details Modal Component
const PredictionDetailsModal = ({ prediction, isOpen, onClose, darkMode }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto`}>
        <div className="flex items-center justify-between mb-6">
          <h3 className={`text-xl font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Refactoring Prediction Details
          </h3>
          <button
            onClick={onClose}
            className={`p-2 ${darkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'} transition`}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-6">
          {/* Basic Info */}
          <div className={`p-4 border rounded-lg ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
            <h4 className={`text-lg font-medium mb-3 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Step {prediction.step}: {prediction.refactoring_type}
            </h4>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  <strong>Target Class:</strong> {prediction.target_class}
                </p>
                {prediction.target_method && (
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    <strong>Target Method:</strong> {prediction.target_method}
                  </p>
                )}
              </div>
              <div>
                <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  <strong>Confidence:</strong> {(prediction.confidence * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>

          {/* Rationale */}
          <div>
            <h4 className={`text-md font-medium mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Rationale
            </h4>
            <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'} p-3 border rounded ${
              darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'
            }`}>
              {prediction.rationale}
            </p>
          </div>

          {/* Expected Improvements */}
          {prediction.expected_improvement && (
            <div>
              <h4 className={`text-md font-medium mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Expected Improvements
              </h4>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(prediction.expected_improvement).map(([objective, value]) => (
                  <div 
                    key={objective} 
                    className={`p-2 border rounded text-center ${
                      darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'
                    }`}
                  >
                    <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                      {objective}
                    </p>
                    <p className={`text-sm font-medium ${value >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {value >= 0 ? '+' : ''}{value.toFixed(4)}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Parameters */}
          {prediction.parameters && Object.keys(prediction.parameters).length > 0 && (
            <div>
              <h4 className={`text-md font-medium mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Parameters
              </h4>
              <div className={`p-3 border rounded ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
                <pre className={`text-xs ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                  {JSON.stringify(prediction.parameters, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;