# vitesse moyenne pour tous les bateaux (bof)
# créer un dictionnaire pour catégorier chq bateaux et leur vitesse moyenne
# (si on reçoit le meme signal)

#!/usr/bin/env python
import pika
import json

# global var: dict of all at_sea_boats
# used in the callback

# defining what to do when a message is received
def callback(ch, method, properties, body):

    print(" [x] Received %r" % body)

    # decoding bytes into string and formatting into JSON
    body_str = body.decode('utf8').replace("'", '"')
    body_json = json.loads(body_str)

    # Check if a boat leaves a port/sea 

    print(json.dumps(body_json, indent=4, sort_keys=True))
    
def main():
    # credentials = pika.PlainCredentials('zprojet', 'rabbit23')
    # parameters = pika.ConnectionParameters('rmqserver.istic.univ-rennes1.fr', 5672, '/', credentials)

    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(
        'localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring input and output queues
    channel.queue_declare(queue='Olf-at_sea_stream')

    # auto_ack: as soon as collected, a message is considered as acked
    channel.basic_consume(queue='Olf-at_sea_stream',
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
