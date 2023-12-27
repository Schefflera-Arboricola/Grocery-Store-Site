if [ -d ".environ" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run local_setup.sh first"
    exit N
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

# Run Celery Worker in the background
celery -A main.celery worker -n worker1 --loglevel=info

deactivate
# To stop Celery worker
# pkill -f 'celery worker'

