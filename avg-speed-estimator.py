# vitesse moyenne pour tous les bateaux (bof)
# créer un dictionnaire pour catégorier chq bateaux et leur vitesse moyenne
# (si on reçoit le meme signal)

#!/usr/bin/env python
import pika
import json

# defining what to do when a message is received


def callback(ch, method, properties, body):

    print(" [x] Received %r" % body)

    # decoding bytes into string and formatting into JSON
    inc_boat_str = body.decode('utf8').replace("'", '"')
    inc_boat_dict = json.loads(inc_boat_str)
    inc_boat_id = inc_boat_dict['boat_id']

    with open('data/at_sea_boat.json', 'r') as data_file:
        # load the json into a `list of dict`
        at_sea_boat_list = json.load(data_file)

    inc_boat_is_present = False
    # for sailing_boat in at_sea_boat_list:
    for i, sailing_boat in enumerate(at_sea_boat_list):
        if sailing_boat["boat_id"] == inc_boat_id:
            print("IN")
            # --- update their value ---
            inc_boat_dict['boat_list_speed'] = sailing_boat['boat_list_speed']
            # add the new input speed
            inc_boat_dict['boat_list_speed'].append(
                inc_boat_dict['boat_speed'])
            # update the speed avg
            inc_boat_dict['boat_speed'] = sum(
                inc_boat_dict['boat_list_speed'])/len(inc_boat_dict['boat_list_speed'])
            at_sea_boat_list[i] = inc_boat_dict
            inc_boat_is_present = True
            break

    if not inc_boat_is_present:
        print("NOT IN")
        # append the new boat into the list
        # add the list of speed
        inc_boat_dict['boat_list_speed'] = [inc_boat_dict['boat_speed']]
        at_sea_boat_list.append(inc_boat_dict)

    # TODO: If a boat enters the sea:
    # - Check if its id exists in the at_port_boat.json
    # - if so remove from it

    with open('data/at_sea_boat.json', 'w') as outfile:
        json.dump(at_sea_boat_list, outfile, indent=4, sort_keys=True)

    # print(json.dumps(at_sea_boat_list, indent=4, sort_keys=True))

    # TODO: feature - with avg_speed.json calculate boat speed for each destination


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
