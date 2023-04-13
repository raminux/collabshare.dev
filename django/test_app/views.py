from django.http import HttpResponse
import pika
import os


def test_pika(request):

    credentials = pika.PlainCredentials('admin', 'pass')
    rabbit_srv = os.environ.get('RABBIT_SERVICE')
    print(f'rabbit_srv = {rabbit_srv}')
    # rabbit_srv = 'host.docker.internal'
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_srv, credentials=credentials))
    channel = connection.channel()
    queue_name = 'TEST_EVENT'
    channel.queue_declare(queue=queue_name)
    channel.basic_publish('', routing_key=queue_name, body='First simple message')



    html = "<html><body>A test event has been sent.</body></html>" 
    return HttpResponse(html)   
