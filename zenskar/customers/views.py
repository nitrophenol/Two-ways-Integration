from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer
import pika
import json
from zenskar.settings import PIKA_PASSWORD,PIKA_USER,HOST,VIRTUAL_HOST
@csrf_exempt
def customer(request):
    if request.method == 'POST':
        try:
            # Extract data from the request
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')

            # Create a new customer
            customer = Customer(name=name, email=email)
            customer.save()

            # Response data
            response_data = {
                "method":"create",
                'name': customer.name,
                'email': customer.email
            }
            responsedata = {
                'name': customer.name,
                'email': customer.email
            }
            message_body = json.dumps(response_data)
            credential = pika.PlainCredentials(username=PIKA_USER, password=PIKA_PASSWORD, erase_on_connect=True)
           # message_body = json.dumps(response_data)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST,credentials=credential,virtual_host=VIRTUAL_HOST))
            channel = connection.channel()
            channel.queue_declare(queue='hello')
            channel.basic_publish(exchange='', routing_key='hello', body=message_body)
            print(" [x] Sent 'Hello World!'")
            connection.close()
            return JsonResponse(responsedata, status=201)

        except Exception as e:
            error_message = {'error': str(e)}
            return JsonResponse(error_message, status=400)

    elif request.method == 'GET':
        try:
            # Handle GET request to retrieve customer data
            customers = Customer.objects.all()
            customer_list = []
            for customer in customers:
                customer_data = {
                    'id': customer.id,
                    'name': customer.name,
                    'email': customer.email
                }
                customer_list.append(customer_data)

            # Connect to RabbitMQ and send a message

            return JsonResponse(customer_list, safe=False)

        except Exception as e:
            error_message = {'error': str(e)}
            return JsonResponse(error_message, status=500)

    elif request.method == 'PUT':
        try:
            # Extract data from the request
            data = json.loads(request.body)
          #  customer_id = data.get('id')
            name = data.get('name')
            email = data.get('email')

            # Find the customer by ID and update their data
            customer = Customer.objects.get(email=email)
            customer.name = name
            customer.email = email
            customer.save()

            # Response data
            response_data = {
                "method":"update",
                'name': customer.name,
                'email': customer.email
            }
            responsedata = {

                'name': customer.name,
                'email': customer.email
            }

            message_body = json.dumps(response_data)
            credential = pika.PlainCredentials(username=PIKA_USER, password=PIKA_PASSWORD, erase_on_connect=True)
              # message_body = json.dumps(response_data)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST,credentials=credential,virtual_host=VIRTUAL_HOST))
            channel = connection.channel()
            channel.queue_declare(queue='hello')
            channel.basic_publish(exchange='', routing_key='hello', body=message_body)

            return JsonResponse(responsedata)

        except Exception as e:
            error_message = {'error': str(e)}
            return JsonResponse(error_message, status=400)

    elif request.method == 'DELETE':
        try:
            # Extract data from the request
            data = json.loads(request.body)
            email = data.get('email')
            response_data = {
                "method":"delete",
                'email': email
            }

            message_body = json.dumps(response_data)
            credential = pika.PlainCredentials(username=PIKA_USER, password=PIKA_PASSWORD, erase_on_connect=True)
              # message_body = json.dumps(response_data)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST,credentials=credential,virtual_host=VIRTUAL_HOST))
            channel = connection.channel()
            channel.queue_declare(queue='hello')
            channel.basic_publish(exchange='', routing_key='hello', body=message_body)

            # Find the customer by ID and delete them
            customer = Customer.objects.get(email=email)
            customer.delete()
            return HttpResponse(status=204)

        except Exception as e:
            error_message = {'error': str(e)}
            return JsonResponse(error_message, status=400)

    else:
        return HttpResponse("Method not allowed", status=405)
