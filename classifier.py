# créer un dictionnaire pour stocker les bateaux à quais

#!/usr/bin/env python
import pika
import json
from typing import Optional


def index_port(port):
    if port == "BREST":
        return 0
    elif port == "VALENCIA":
        return 1
    elif port == "PALERMO":
        return 2
    elif port == "BRIGHTON":
        return 3
    elif port == "AMSTERDAM":
        return 4
    else:
        return -1


# defining what to do when a message is received


def callback(ch, method, properties, body):

    print(" [x] Received %r" % body)

    # decoding bytes into string and formatting into JSON
    inc_boat_str = body.decode('utf8').replace("'", '"')
    inc_boat_dict = json.loads(inc_boat_str)

    # gathering boat's information
    inc_boat_id = inc_boat_dict['boat_id']
    inc_boat_port = inc_boat_dict['boat_destination']

    with open('data/at_port_boat.json', 'r') as data_file:
        # load the json into a `list of dict`
        at_port_boat_list = json.load(data_file)

    with open('data/port_classifier.json', 'r') as data_file:
        # load the json into a `list of dict`
        port_classifier_list = json.load(data_file)

    inc_boat_is_present = False
    # we can lower the complexity of the search by sorting / boat_id
    # or using HashMap...
    # for docked_boat in at_port_boat_list:
    for i, docked_boat in enumerate(at_port_boat_list):
        if docked_boat["boat_id"] == inc_boat_id:
            print("IN")

            # ---- Teleportion from another port ----
            # --- down the count in port_classifier_list ---
            port_info = port_classifier_list[index_port(
                docked_boat["boat_destination"])]
            # port_info = { "port_name": "NAME", "boat_count": X }
            port_info['boat_count'] = port_info['boat_count'] - 1
            port_classifier_list[index_port(
                docked_boat["boat_destination"])] = port_info

            # update their value (destination, speed)
            at_port_boat_list[i] = inc_boat_dict
            inc_boat_is_present = True
            break

    if not inc_boat_is_present:
        print("NOT IN")
        # append the new boat into the list
        at_port_boat_list.append(inc_boat_dict)

    # --- up the count in port_classifier_list ---
    port_info = port_classifier_list[index_port(inc_boat_port)]
    # port_info = { "port_name": "NAME", "boat_count": X }
    port_info['boat_count'] = port_info['boat_count'] + 1
    port_classifier_list[index_port(inc_boat_port)] = port_info

    # TODO: If a boat enters a port:
    # - Check if its id exists in the at_sea_boat.json
    # - if so remove from it -------------------vvvvvv

    # FIXME: Two programs (avg-speed-estimator and classifier) writes into the same json
    # IDEA: ^^^^^^---- Build a new program which will manage these things ?

    # DEBUG: Dumping json with each message sometimes seems to cause the json to be completely deleted.
    with open('data/at_port_boat.json', 'w') as outfile:
        json.dump(at_port_boat_list, outfile, indent=4, sort_keys=True)
    with open('data/port_classifier.json', 'w') as outfile:
        json.dump(port_classifier_list, outfile, indent=4, sort_keys=True)
    # print(json.dumps(at_port_boat_list, indent=4, sort_keys=True))


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
