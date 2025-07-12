import React, { useState, useEffect, useCallback } from 'react';
import { Upload, Download, Play, Pause, Trash2, FileText, Activity, Package, AlertCircle, CheckCircle, Clock, X, RefreshCw, Moon, Sun, Save, Database, Brain } from 'lucide-react';

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
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
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
        headers: {}, // Let browser set content-type for FormData
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
        headers: {},
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
                onSelectForML={() => {
                  setSelectedProject(project);
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
            <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Training Tasks</h3>
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
              <p className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>No training tasks yet. Start a training from the ML Training tab!</p>
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
const ProjectCard = ({ project, darkMode, onAnalyze, onDelete, onSelectForML, isLoading }) => (
  <div className={`p-6 ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50'} transition`}>
    <div className="flex items-center justify-between">
      <div className="flex-1">
        <h4 className={`font-medium text-lg ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          {project.name || project.project_name}
        </h4>
        <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} mt-1`}>
          {project.description || 'No description provided'}
        </p>
        <div className="flex items-center gap-4 mt-3">
          {project.version_id && (
            <span className={`inline-flex items-center px-2 py-1 rounded-md ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'} text-xs`}>
              Version: {project.version_id}
            </span>
          )}
          {project.git_url && (
            <a href={project.git_url} target="_blank" rel="noopener noreferrer"
               className="text-xs text-blue-600 hover:underline">
              Git Repository
            </a>
          )}
        </div>
      </div>
      <div className="flex items-center gap-2 ml-4">
        <button
          onClick={() => onAnalyze(project.name, project.version_id || 'v1.0')}
          className={`p-2 ${darkMode ? 'text-purple-400 hover:bg-purple-900' : 'text-purple-600 hover:bg-purple-50'} rounded transition`}
          title="Analyze Project"
          disabled={isLoading}
        >
          <Activity className="w-4 h-4" />
        </button>
        <button
          onClick={onSelectForML}
          className={`p-2 ${darkMode ? 'text-green-400 hover:bg-green-900' : 'text-green-600 hover:bg-green-50'} rounded transition`}
          title="Start ML Training"
        >
          <Brain className="w-4 h-4" />
        </button>
        <button
          onClick={() => onDelete(project.name, project.version_id)}
          className={`p-2 ${darkMode ? 'text-red-400 hover:bg-red-900' : 'text-red-600 hover:bg-red-50'} rounded transition`}
          title="Delete Project"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
);

// ML Training Form Component
const MLTrainingForm = ({ onSubmit, projects, selectedProject, darkMode, isLoading }) => {
  const [trainingConfig, setTrainingConfig] = useState({
    env_config: {
      project_name: selectedProject?.name || '',
      udb_path: '',
      n_obj: 8,
      lower_band: 1,
      upper_bound: 50,
      population_size: 100,
      version_id: 'v1.0',
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

  // Update config when selected project changes
  useEffect(() => {
    if (selectedProject) {
      setTrainingConfig(prev => ({
        ...prev,
        env_config: {
          ...prev.env_config,
          project_name: selectedProject.name,
          udb_path: `/opt/understand_dbs/${selectedProject.name}/${prev.env_config.version_id}/${selectedProject.name}.und`,
          project_path: `/opt/projects/${selectedProject.name}/${prev.env_config.version_id}/source`
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
        {/* Project Selection */}
        <div>
          <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Select Project *
          </label>
          <select
            value={trainingConfig.env_config.project_name}
            onChange={(e) => setTrainingConfig(prev => ({
              ...prev,
              env_config: { ...prev.env_config, project_name: e.target.value }
            }))}
            className={inputClass}
          >
            <option value="">Choose a project...</option>
            {projects.map((project, index) => (
              <option key={index} value={project.name}>
                {project.name} {project.version_id && `(${project.version_id})`}
              </option>
            ))}
          </select>
        </div>

        {/* Environment Configuration */}
        <div className={`border rounded-lg p-4 ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
          <h4 className={`text-md font-semibold mb-3 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Environment Configuration</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                Version ID
              </label>
              <input
                type="text"
                value={trainingConfig.env_config.version_id}
                onChange={(e) => setTrainingConfig(prev => ({
                  ...prev,
                  env_config: { ...prev.env_config, version_id: e.target.value }
                }))}
                className={inputClass}
              />
            </div>
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
          disabled={!trainingConfig.env_config.project_name || isLoading}
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

export default App;