import React, { useState, useEffect, useCallback } from 'react';
import { Upload, Download, Play, Pause, Trash2, FileText, Activity, Package, AlertCircle, CheckCircle, Clock, X, RefreshCw, Moon, Sun, Save, Database, Brain, TrendingUp, BarChart3, Settings, Target } from 'lucide-react';

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
              <TaskCard
                key={task.task_id}
                task={task}
                darkMode={darkMode}
                onCancel={cancelTraining}
                onRefresh={() => getTaskStatus(task.task_id)}
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
        udb_path: `/opt/understand_dbs/${trainingConfig.env_config.project_name}/${trainingConfig.env_config.version_id}/${trainingConfig.env_config.project_name}.und`,
        project_path: `/opt/projects/${trainingConfig.env_config.project_name}/${trainingConfig.env_config.version_id}/source`
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

export default App;