"""
Launcher script for the Adaptive RAG UI.
"""

import os
import sys
import argparse
import subprocess
import importlib.util

def check_module_installed(module_name):
    """Check if a module is installed."""
    return importlib.util.find_spec(module_name) is not None

def install_requirements(ui_type):
    """Install requirements for the selected UI."""
    req_file = None
    
    if ui_type == 'streamlit':
        req_file = 'requirements.txt'
    elif ui_type == 'gradio':
        req_file = 'gradio_requirements.txt'
    elif ui_type == 'flask':
        req_file = 'flask_requirements.txt'
    
    if req_file:
        print(f"Installing requirements for {ui_type} UI...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_file])

def launch_ui(ui_type):
    """Launch the selected UI."""
    if ui_type == 'streamlit':
        if not check_module_installed('streamlit'):
            install_requirements('streamlit')
        print("Launching Streamlit UI...")
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
    elif ui_type == 'gradio':
        if not check_module_installed('gradio'):
            install_requirements('gradio')
        print("Launching Gradio UI...")
        subprocess.run([sys.executable, 'gradio_app.py'])
    elif ui_type == 'flask':
        if not check_module_installed('flask'):
            install_requirements('flask')
        print("Launching Flask UI...")
        subprocess.run([sys.executable, 'flask_app.py'])
    else:
        print(f"Unknown UI type: {ui_type}")
        sys.exit(1)

def main():
    """Parse command line arguments and launch the UI."""
    parser = argparse.ArgumentParser(description='Launch Adaptive RAG UI')
    parser.add_argument('--ui', '-u', type=str, choices=['streamlit', 'gradio', 'flask'], 
                        default='streamlit', help='UI type to launch')
    args = parser.parse_args()
    
    # Change to the directory of this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Launch the UI
    try:
        launch_ui(args.ui)
    except KeyboardInterrupt:
        print("\nUI process terminated by user.")
    except Exception as e:
        print(f"Error launching UI: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()