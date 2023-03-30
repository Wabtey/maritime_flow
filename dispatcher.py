

#!/usr/bin/env python
import pika
import json

# defining what to do when a message is received
def callback(ch, method, properties, body):

    print(" [x] Received %r" % body)

    # decoding bytes into string and formatting into JSON
    body_str = body.decode('utf8').replace("'", '"')
    body_json = json.loads(body_str)

    print(json.dumps(body_json, indent=4, sort_keys=True))

    # Seperate low speed < 4 and put them in a list to send
    # instant Redirect to the good channel
    if body_json['boat_speed'] > 4:
        send_at_sea(body_str)
    else:
        send_at_port(body_str)

# Redirect to the at_sea_stream channel 
def send_at_sea(nonstationary_boat):
    # --- Send Data ---
    
    credentials = pika.PlainCredentials('zprojet', 'rabbit23')
    parameters = pika.ConnectionParameters('rmqserver.istic.univ-rennes1.fr', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring the queue
    channel.queue_declare(queue='Olf-at_sea_stream')

    # send the message, through the exchange ''
    # which simply delivers to the queue having the key as name
    # + our name to have unique key
    channel.basic_publish(exchange='',
                      routing_key='Olf-at_sea_stream',
                      body=str(nonstationary_boat))

    print(" [x] Sent to at_sea_stream: " + str(nonstationary_boat))

    # gently close (flush)
    connection.close()

# Redirect to the at_port_stream channel
def send_at_port(stationary_boat):
    # --- Send Data ---
    
    credentials = pika.PlainCredentials('zprojet', 'rabbit23')
    parameters = pika.ConnectionParameters('rmqserver.istic.univ-rennes1.fr', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring the queue
    channel.queue_declare(queue='Olf-at_port_stream')

    # send the message, through the exchange ''
    # which simply delivers to the queue having the key as name
    # + our name to have unique key
    channel.basic_publish(exchange='',
                      routing_key='Olf-at_port_stream',
                      body=str(stationary_boat))

    print(" [x] Sent to at_port_stream: " + str(stationary_boat))

    # gently close (flush)
    connection.close()

def main():
    credentials = pika.PlainCredentials('zprojet', 'rabbit23')
    parameters = pika.ConnectionParameters('rmqserver.istic.univ-rennes1.fr', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring input and output queues
    channel.queue_declare(queue='Olf-boat_stream')

    # auto_ack: as soon as collected, a message is considered as acked
    channel.basic_consume(queue='Olf-boat_stream',
                      auto_ack=True,
                      on_message_callback=callback)

    # wait for messages
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
