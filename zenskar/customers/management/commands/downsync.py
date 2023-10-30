# myapp/management/commands/my_custom_command.py
from ast import If
import email
from django.core.management.base import BaseCommand
import stripe
from customers.models import Customer
from django.db.models import Q
from functools import reduce
from operator import or_
import stripe
import pika
import time
from zenskar.settings import SECRET_KEY, BASE_URL,PIKA_PASSWORD,PIKA_USER,HOST,VIRTUAL_HOST
 # Corrected import statement

# Set your Stripe API key
stripe.api_key = SECRET_KEY  # Replace with your own secret API key

# Set your RabbitMQ connection parameters
rabbitmq_credentials = pika.PlainCredentials(PIKA_USER, PIKA_PASSWORD)
rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, credentials=rabbitmq_credentials, virtual_host=VIRTUAL_HOST))
channel = rabbitmq_connection.channel()

# Initialize the last processed timestamp or event ID
last_processed_timestamp = 0

# Define the queue to send updates to
queue_name = 'customer_updates'
# Set your Stripe API key
stripe.api_key = SECRET_KEY
class Command(BaseCommand):
    help = 'My custom management command'
    def handle(self, *args, **options):
        # Your custom command logic goes here
        self.stdout.write(self.style.SUCCESS('This is a custom management command!'))
        
        
        
        try:
             obj1={}
             customers = stripe.Customer.list(limit=10)  # Limit specifies the number of customers to retrieve
             
             for customer in customers.auto_paging_iter():
              obj1[customer.email]=customer.name
             # print(f"Customer ID: {customer.id}, Email: {customer.email},Name:{customer.name}")
              
             # Create a list of Q objects representing the conditions
             all_customers = Customer.objects.all()
             for customer in all_customers:   
                  if customer.name!=obj1[customer.email]:
                   # arr.append(customer)
                    channel.queue_declare(queue=queue_name)   
                    obj={"name":obj1[customer.email],
                         "email":customer.email,
                          "method":"update"}
                    print(f"Name: {customer.name}, Email: {customer.email},Id :{customer.id}")
                    channel.basic_publish(exchange='', routing_key=queue_name, body=str(obj))   
                  obj1.pop(customer.email)

                   #print(len(all_customers))
             for key in obj1:
                    channel.queue_declare(queue=queue_name)   
                    obj={"name":obj1[key],
                        "email":key,
                        "method":"create"}
                    print(f"Name: {obj1[key]}, Email: {key}")
                    channel.basic_publish(exchange='', routing_key=queue_name, body=str(obj))  
             

        except Exception as e:

             print(f"Error: {e}")
        