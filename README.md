

# Two-Ways Integration

Two-Ways Integration is a Django project designed to run locally and deploy to a virtual machine. It handles interactions with Stripe, downsync, upsync, and APIs. This `readme.md` provides instructions for running the project locally and deploying it to a virtual machine.

## Running Locally

To run the project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/Two-Ways-Integration.git
   cd Two-Ways-Integration


Install project dependencies:<br>
pip install -r requirements.txt


Edit settings.py to include the correct Stripe API credentials:<br>
       STRIPE_SECRET = "sk_test_your_stripe_secret_key"<br>
    ```bash
       bash run.sh
       
The following commands will be executed in the background:<br>

python manage.py runserver<br>
python manage.py downsyncConsumer<br>
python manage.py upsyncConsumer<br>
python manage.py run<br>

The project is now running locally, and the various management commands are listening for events and processing data. <br>

Configuration<br>
STRIPE_PUBLIC: Your Stripe public key.<br>
STRIPE_SECRET: Your Stripe secret key.<br>
BASE_URL: The base URL for your project.<br>
HOST: Hostname for your message broker (e.g., RabbitMQ).<br>
VIRTUAL_HOST: Virtual host for your message broker.<br>
PIKA_PASSWORD: Password for the message broker.<br>
PIKA_USER: Username for the message broker.<br>
Ensure that these settings are correctly configured for your specific environment.<br>
