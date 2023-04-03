# Maritime flow

## data-generator.py

Generate randomly 100 boat signal
and send them in the `boat_stream` of the RabbitMQ server

ex:

```json
{
    "boat_destination": "PALERMO",
    "boat_id": 1,
    "boat_speed": 3
},
```

## dispatcher.py

Analyse the boat signal received in the `boat_stream`

if the `boat_speed` > 4, this signal is sent to the `at_sea_stream`
else it is sent `at_port_stream`

## avg_speed_estimator.py

Store any boat signal received in the at_sea_stream, into `at_sea_boat.json`.
It adds a new data to the boat dictionary `boat_list_speed`, which contains all the speed registered for this sailing_boat.
And it modify the `boat_speed` to match the average speed of this previous list.

ex:

```json
[
    {
        "boat_destination": "BREST",
        "boat_id": 86,
        "boat_list_speed": [
            18,
            10,
            8
        ],
        "boat_speed": 12.0
    }
]
```

## classifier.py

Store the boat signal received in the `at_port_stream` into the `at_port_boat.json`.
It updates/append the data in this json,
and keep track of how much boats are in each port in `port_classifier.json`

ex of `port_classifier.json`:

```json
[
    {
        "boat_count": 4,
        "port_name": "BREST"
    },
    {
        "boat_count": 1,
        "port_name": "VALENCIA"
    },
    {
        "boat_count": 5,
        "port_name": "PALERMO"
    },
    {
        "boat_count": 2,
        "port_name": "BRIGHTON"
    },
    {
        "boat_count": 7,
        "port_name": "AMSTERDAM"
    }
]
```

## Future Features

comming soon: || never ||

- Trackingthe average speed of boats for each destination
- When a boat previously stored in the `at_port_boat.json` file sends a signal,
which indicates that this boat is now sailing:
Update the database
- Keep track of the number of boats leaving  each port and the number of boats heading for each port.
