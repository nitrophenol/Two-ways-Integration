# myapp/management/commands/my_custom_command.py
from ...models import Customer
from django.core.management.base import BaseCommand
import pika, json, requests
from zenskar.settings import SECRET_KEY, BASE_URL,PIKA_PASSWORD,PIKA_USER,HOST,VIRTUAL_HOST
class Command(BaseCommand):
    help = 'Custom command to process messages from a queue'

    def handle(self, *args, **kwargs):
        def preprocess_message(body):
            valid_json_str = body.decode('utf-8').replace("'", '"')
            return valid_json_str

        credentials = pika.PlainCredentials(PIKA_USER, PIKA_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, credentials=credentials, virtual_host=VIRTUAL_HOST))
        channel = connection.channel()
        channel.queue_declare(queue='customer_updates')

        def callback(ch, method, properties, body):
            try:
                valid_json_str = preprocess_message(body)
                data = json.loads(valid_json_str)
                name = data.get('name')
                email = data.get('email')
                print(name)

                # Update the URL and data to match your API endpoint
                url = f"{BASE_URL}api/update-customer/"
                payload = {
                    'name': name,
                    'email': email
                }

                headers = {'Content-Type': 'application/json'}

                if data.get("method") == "create":
                    url = f"{BASE_URL}api/create-customer/"
                    customer = Customer(name=name, email=email)
                    customer.save()
                    
                elif data.get("method") == "delete":
                    url = f"{BASE_URL}api/delete-customer/"
                    payload = {
                    'email': email
                       }
                    response = requests.delete(url, json=payload, headers=headers)
                elif data.get("method") == "update":
                    response = requests.put(url, json=payload, headers=headers)
                # print(response.status_code)
                # if response.status_code == 200:
                #     print(f"Successfully processed message: {body}")
                # if response.status_code == 400:
                #     print(f"Error processing message: {body}")
                # if response.status_code == 204:
                #     print(f"Successfully processed message: {body}")        
                # if response.status_code == 404:
                #     print(f"Error processing message: {body}")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except Exception as e:
                print(f"Error creating customer: {e}")

        channel.basic_consume(queue='customer_updates', on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit, press CTRL+C')
        channel.start_consuming()
