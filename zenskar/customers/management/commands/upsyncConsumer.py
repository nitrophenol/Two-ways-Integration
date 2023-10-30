# YourApp/management/commands/process_messages.py

from django.core.management.base import BaseCommand
import pika
import stripe
import json
from zenskar.settings import SECRET_KEY, BASE_URL,PIKA_PASSWORD,PIKA_USER,HOST,VIRTUAL_HOST
class Command(BaseCommand):
    help = 'Process messages from a queue'

    def handle(self, *args, **kwargs):
        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)

            try:
                # Assuming the message body is in JSON format
                data = json.loads(body)
                name = data.get("name")
                email = data.get("email")
                method = data.get("method")
                print(method)
                print(name)
                # Create a Stripe customer and add name and email as metadata
                stripe.api_key = SECRET_KEY
                
                if method == "update":
                    customers = stripe.Customer.list(limit=10)
                    for customer in customers.auto_paging_iter():
                        if customer.email == email:
                            # Retrieve the customer
                            customer = stripe.Customer.retrieve(customer.id)
                            
                            # Update the customer's name
                            customer.name = name
                            
                            # Save the changes
                            customer.save()
                            break
                    
                if method == "create":
                    customer = stripe.Customer.create(name=name, email=email)
                
                if method == "delete":
                    customers = stripe.Customer.list(limit=10)
                    for customer in customers.auto_paging_iter():
                        if customer.email == email:
                            customer.delete()
                            break

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except Exception as e:
                print(f"Error processing message: {e}")

        credentials = pika.PlainCredentials(PIKA_USER, PIKA_PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=HOST, credentials=credentials, virtual_host=VIRTUAL_HOST
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue="hello")
        channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

        print(" [*] Waiting for messages. To exit, press CTRL+C")
        channel.start_consuming()
