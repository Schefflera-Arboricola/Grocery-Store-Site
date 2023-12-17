#!/bin/sh
echo "============================================================================="
echo "Welcome to the setup. This will setup the local virtual env."
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "-----------------------------------------------------------------------------"

# Check if running within Docker
if [ -z "$ENV" ]; then
  # Not running within Docker, create and activate virtual env
  if [ -d ".environ" ]; then
    echo ".environ folder exists. Installing using pip"
  else
    echo "Creating .environ and installing using pip"
    python -m venv .environ
  fi

  # Activate virtual env
  . .environ/bin/activate

  pip install --upgrade pip

  # Install requirements
  pip install -r requirements.txt

  # Deactivate virtual env
  deactivate
fi
