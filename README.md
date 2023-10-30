

# Two-Ways Integration

Two-Ways Integration is a Django project designed to run locally and deploy to a virtual machine. It handles interactions with Stripe, downsync, upsync, and APIs. This `readme.md` provides instructions for running the project locally and deploying it to a virtual machine.

## Running Locally

To run the project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/Two-Ways-Integration.git
   cd Two-Ways-Integration


Install project dependencies:
   pip install -r requirements.txt


Edit settings.py to include the correct Stripe API credentials:
       STRIPE_SECRET = "sk_test_your_stripe_secret_key"
    ```bash
       bash run.sh
       
The following commands will be executed in the background:

python manage.py runserver
python manage.py downsyncConsumer
python manage.py upsyncConsumer
python manage.py run

The project is now running locally, and the various management commands are listening for events and processing data. 

Configuration
STRIPE_PUBLIC: Your Stripe public key.
STRIPE_SECRET: Your Stripe secret key.
BASE_URL: The base URL for your project.
HOST: Hostname for your message broker (e.g., RabbitMQ).
VIRTUAL_HOST: Virtual host for your message broker.
PIKA_PASSWORD: Password for the message broker.
PIKA_USER: Username for the message broker.
Ensure that these settings are correctly configured for your specific environment.
