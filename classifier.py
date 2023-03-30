# créer un dictionnaire pour stocker les bateaux à quais

#!/usr/bin/env python
import pika
import json
from typing import Optional

at_port_boat = {}

# defining what to do when a message is received
def callback(ch, method, properties, body):

    print(" [x] Received %r" % body)

    # decoding bytes into string and formatting into JSON
    inc_boat_str = body.decode('utf8').replace("'", '"')
    inc_boat_json = json.loads(inc_boat_str)

    # match at_port_boat.get(inc_boat_json['boat_id']):
    #     case None: at_port_boat.extend(inc_boat_json)
    #     case Optional[boat]: 

    at_port_boat_json = json.load(at_port_boat)
    
    if inc_boat_json['boat_id'] in at_port_boat_json:
        print("IN")
    else:
        print("NOT IN")
        at_port_boat_json.update(inc_boat_json)

    # Check if a boat leaves a port/sea 

    print(json.dumps(at_port_boat_json, indent=4, sort_keys=True))
        
def main():
    
    credentials = pika.PlainCredentials('zprojet', 'rabbit23')
    parameters = pika.ConnectionParameters('rmqserver.istic.univ-rennes1.fr', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring input and output queues
    channel.queue_declare(queue='Olf-at_port_stream')

    # auto_ack: as soon as collected, a message is considered as acked
    channel.basic_consume(queue='Olf-at_port_stream',
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
