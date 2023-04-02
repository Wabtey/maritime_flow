# créer un dictionnaire pour stocker les bateaux à quais

#!/usr/bin/env python
import pika
import json
from typing import Optional

# defining what to do when a message is received
def callback(ch, method, properties, body):

    print(" [x] Received %r" % body)

    # decoding bytes into string and formatting into JSON
    inc_boat_str = body.decode('utf8').replace("'", '"')
    inc_boat_dict = json.loads(inc_boat_str)

    with open('data/at_port_boat.json', 'r') as data_file:    
        # load the json into a `list of dict`
        at_port_boat_list = json.load(data_file)
    
    if inc_boat_dict['boat_id'] in at_port_boat_list:
        print("IN")
        # update their value
        at_port_boat_list[inc_boat_dict['boat_id']] = inc_boat_dict
    else:
        print("NOT IN")
        # append the new boat into the file
        at_port_boat_list.append(inc_boat_dict)
    # Check if a boat leaves a port/sea 
        
    with open('data/at_port_boat.json', 'w') as outfile:
        json.dump(at_port_boat_list, outfile, indent=4, sort_keys=True)

    print(json.dumps(at_port_boat_list, indent=4, sort_keys=True))


def main():

    # credentials = pika.PlainCredentials('zprojet', 'rabbit23')
    # parameters = pika.ConnectionParameters('rmqserver.istic.univ-rennes1.fr', 5672, '/', credentials)

    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(
        'localhost', 5672, '/', credentials)
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
