#!/bin/sh
echo "============================================================================="
echo "Welcome to the setup. This will setup the local virtual env."
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "-----------------------------------------------------------------------------"

if [ -d ".environ" ]; then
    echo "Enabling virtual environ"
else
    echo "No Virtual environ. Please run setup.sh first"
    exit 1
fi
# Activate virtual env
. .environ/bin/activate
export ENV=development

# Initialize API credentials
export TWILIO_ACCOUNT_SID=
export TWILIO_AUTH_TOKEN=
export TWILIO_SENDER_PHONE=
export STRIPE_PUBLIC_KEY=
export STRIPE_SECRET_KEY=

# Initialize mail credentials
export MAIL_USERNAME=''
export MAIL_PASSWORD=''
export MAIL_DEFAULT_SENDER=''

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