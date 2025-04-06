
#!/bin/bash

echo "Setting up Ashans virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Ashans environment is ready."
