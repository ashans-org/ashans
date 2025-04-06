import os
import subprocess
import sys

def create_virtualenv():
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    print("Virtual environment created in ./venv")

def install_requirements():
    print("Installing dependencies from requirements.txt...")
    if os.name == "nt":
        pip_path = ".\\venv\\Scripts\\pip"
    else:
        pip_path = "./venv/bin/pip"
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    print("Dependencies installed.")

if __name__ == "__main__":
    create_virtualenv()
    install_requirements()