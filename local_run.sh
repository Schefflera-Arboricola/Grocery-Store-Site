#!/bin/sh
echo "============================================================================="
echo "Welcome to the setup. This will setup the local virtual env."
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "-----------------------------------------------------------------------------"

if [ -d ".environ" ]; then
    echo "Enabling virtual environ"
else
    echo "No Virtual environ. Please run local_setup.sh first"
    exit 1
fi
# Activate virtual env
. .environ/bin/activate
export ENV=development


# Load environment variables from .env file
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    set -o allexport
    source .env
    set +o allexport
else
    echo ".env file not found. Ensure it exists with necessary credentials."
    exit 1
fi

# Check if wkhtmltopdf is installed
if ! command -v wkhtmltopdf &> /dev/null; then
    echo "Installing wkhtmltopdf..."
    # Install wkhtmltopdf using Homebrew (macOS)
    brew install Caskroom/cask/wkhtmltopdf
fi

# Set the path to wkhtmltopdf for pdfkit
export WKHTMLTOPDF_PATH=$(which wkhtmltopdf)

redis-server --daemonize yes

celery -A main.celery beat --loglevel=info &

# Run Celery Worker in the background
celery -A main.celery worker -n worker1 --loglevel=info &

# Run the Flask app
python main.py

# To stop Redis
redis-cli shutdown

# To stop Celery worker
pkill -f 'celery worker'

# To stop Celery beat
pkill -f 'celery beat'

deactivate