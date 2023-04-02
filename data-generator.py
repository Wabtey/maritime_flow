#!/usr/bin/env python
import pika
import json
import random
from enum import Enum

NB_BOATS = 100


class Port(Enum):
    BREST = 1
    VALENCIA = 2
    PALERMO = 3
    BRIGHTON = 4
    AMSTERDAM = 5


class BoatSignal:

    def __init__(self, rnd):
        self.boatId = rnd.randint(0, NB_BOATS)
        self.destination = rnd.choice(list(Port))
        self.speed = rnd.randint(0, 20)

    def getBoatId(self):
        return self.boatId

    def getDestination(self):
        return self.destination.name

    def getSpeed(self):
        return self.speed

    def toDict(self):
        d = {}
        d["boat_id"] = self.getBoatId()
        d["boat_destination"] = self.getDestination()
        d["boat_speed"] = self.getSpeed()

        return d


if __name__ == "__main__":

    for count in range(100):
        rnd = random.Random()
        bs = BoatSignal(rnd)
        d = bs.toDict()
        # d["boat_id"] = 23

        # getting a connection to the broker
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters(
            'localhost', 5672, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # declaring the queue
        channel.queue_declare(queue='Olf-boat_stream')

        # send the message, through the exchange ''
        # which simply delivers to the queue having the key as name
        # + our name to have unique key
        channel.basic_publish(exchange='',
                              routing_key='Olf-boat_stream',
                              body=str(d))

        print(" [x] Sent: " + str(d))

        # gently close (flush)
        connection.close()
