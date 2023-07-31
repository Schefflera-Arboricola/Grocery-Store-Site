#! /bin/sh
echo "============================================================================="
echo "Welcome to the setup. This will setup the local virtual env."
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "-----------------------------------------------------------------------------"
if [ -d ".environ" ];
then
    echo "Enabling virtual environ"
else
    echo "No Virtual environ. Please run setup.sh first"
    exit N
fi
# Activate virtual env
. .environ/bin/activate
export ENV=development

#initialize API credentials
export TWILIO_ACCOUNT_SID=
export TWILIO_AUTH_TOKEN=
export TWILIO_SENDER_PHONE=
export STRIPE_PUBLIC_KEY=
export STRIPE_SECRET_KEY=

python main.py
deactivate