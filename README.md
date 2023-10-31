# Django Customer Sync App

## Overview

This Django app provides a set of REST APIs for performing CRUD operations on customer data in the database. It has a unique twist where email is treated as the primary key for customers due to differences in customer IDs between Stripe and the database. The app supports both upsync and downsync operations to synchronize customer data between the database and Stripe.

## Components

### 1. REST APIs

The app exposes the following REST API endpoints for managing customer data:

- `POST http://localhost:8000/api/create-customer/`: Create a new customer in the database and publish the operation to a RabbitMQ queue for upsync.

- `PUT http://localhost:8000/api/update-customer/`: Update an existing customer in the database and publish the operation to the upsync queue.

- `DELETE http://localhost:8000/api/delete-customer/`: Delete a customer from the database and publish the operation to the upsync queue.
- `{
    "name":"badger980",
     "email":"badgerrooockes1383@gmail.com"
  }`   :  this will be the formate of json payload for all request you can remove name field in delete request

### 2. Upsync

#### Publisher

When a customer uses one of the POST, PUT, or DELETE requests, the app publishes the operation to a RabbitMQ queue. This operation is handled by the upsyncConsumer.py script.

### 3. Upsync Consumer

Located at `/zenskar/customers/management/commands/upsyncConsumer.py`, this script listens to the upsync queue. When it detects an operation, it synchronizes the data with Stripe.

### 4. Downsync

#### downsync.py

This script fetches customer information from both Stripe and the database and checks for differences. If there are changes, it adds the necessary updates to a queue.

#### Run Scheduler

To run downsync.py at regular intervals (e.g., every 10 seconds), a `run.py` script in the same directory can be used as a scheduler.

### 5. Downsync Consumer

The `downsyncConsumer.py` script listens to the downsync queue. When it detects changes in the queue, it triggers PUT or POST requests to update the customer data in the database.

## How to Use

1. Install the required dependencies and set up your Django environment.

2. Configure RabbitMQ to work with your Django project.

3. Run run.sh in zenskar/ it will run all the consumers and Django server.

4. Use the provided REST APIs to create, update, or delete customer data in the database.

5. The upsyncConsumer.py script will handle upsync operations.

6. Configure the downsync.py script to run at your desired intervals using the run.py scheduler.

7. The downsyncConsumer.py script will handle downsync operations.

## Configuration

Make sure to update the following configurations in your Django project:

- RabbitMQ settings for upsync and downsync queues.

- Stripe API keys for interacting with Stripe's customer data.

## Dependencies

Ensure you have the following dependencies installed:

- Django

- RabbitMQ

- Stripe Python library
