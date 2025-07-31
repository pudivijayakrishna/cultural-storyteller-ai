import subprocess
import sys
import os
import time

# Paths
backend_dir = os.path.join(os.getcwd(), 'backend')
frontend_dir = os.path.join(os.getcwd(), 'frontend')
venv_python = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python.exe')

# Start backend Flask server
backend_cmd = [venv_python, 'app.py']
backend_proc = subprocess.Popen(
    backend_cmd,
    cwd=backend_dir,
    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
)
print('Started backend Flask server.')

# Give backend a moment to start
time.sleep(2)

# Start frontend HTTP server
frontend_cmd = [venv_python, '-m', 'http.server', '8000']
frontend_proc = subprocess.Popen(
    frontend_cmd,
    cwd=frontend_dir,
    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
)
print('Started frontend HTTP server at http://localhost:8000')

print('\nBoth backend and frontend are running. Press Ctrl+C to stop.')

try:
    backend_proc.wait()
    frontend_proc.wait()
except KeyboardInterrupt:
    print('Stopping servers...')
    backend_proc.terminate()
    frontend_proc.terminate()
    print('Servers stopped.') 