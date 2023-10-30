#!/bin/bash

# Start the Django development server in the background
nohup python manage.py runserver &

# Run the 'downsyncConsumer' management command in the background
echo "runserver done"
nohup python manage.py downsyncConsumer &

# Run the 'upsync' management command in the background
echo "downsyncConsumer done"

# Run the 'upsyncConsumer' management command in the background
nohup python manage.py upsyncConsumer &
echo "upsyncConsumer done"
# Run the 'run' management command in the background
nohup python manage.py run &
echo "run done"
# Optionally, you can add a sleep to keep the script running
# This is useful if you want to keep the commands running for a specific duration
# For example, sleep for 12 hours (43200 seconds)
# sleep 43200

# Optionally, you can add a message for when the script completes
echo "All commands have been started in the background."

# You can save this script and make it executable with the following command:
# chmod +x run_commands.sh

# To execute the script, simply run:
# ./run_commands.sh

