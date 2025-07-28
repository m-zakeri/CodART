#!/bin/bash

# Create UI directory structure
echo "Setting up ML Platform UI..."

# Create directories
mkdir -p ui/src/components
mkdir -p ui/public

# Create public/index.html
cat > ui/public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="ML Training Platform" />
    <title>ML Training Platform</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
EOF

# Create src/index.css with Tailwind directives
cat > ui/src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
EOF

# Create src/index.js
cat > ui/src/index.js << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

# Note: The App.js content should be copied from the artifact you already have


# Make script executable
chmod +x setup-ui.sh

echo "✅ UI setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy the App.js content from the previous artifact to ui/src/App.js"
echo "2. Copy the configuration files (package.json, tailwind.config.js, etc.) to the ui/ directory"
echo "3. Copy nginx.conf and Dockerfile to the ui/ directory"
echo "4. Add the UI service to your docker-compose.yml"
echo "5. Run: docker-compose up --build ui"
echo ""
echo "The UI will be available at http://localhost:3000"