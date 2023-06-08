

#! /bin/sh
echo "============================================================================="
echo "Welcome to the setup. This will setup the local virtual env."
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "-----------------------------------------------------------------------------"

# Check available Python versions
python_versions=(python3.9 python3.8 python3.7 python3.6 python3.5 python)

# Find the first available Python version
for version in "${python_versions[@]}"; do
  if command -v $version &>/dev/null; then
    python_command=$version
    break
  fi
done

# Check if Python is found
if [ -z "$python_command" ]; then
  echo "Python not found on the system. Please install Python and try again."
  exit 1
fi

if [ -d ".env" ]; then
  echo ".env folder exists. Installing using pip"
else
  echo "Creating .env and installing using pip"
  $python_command -m venv .env
fi

# Activate virtual env
. .env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Deactivate virtual env
deactivate
