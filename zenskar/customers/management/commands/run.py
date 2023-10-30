
import time
from django.core.management import call_command

while True:
    # Call your custom management command
    call_command('downsync')
    
    # Sleep for 10 seconds
    time.sleep(10)