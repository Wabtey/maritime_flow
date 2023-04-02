# Semi Tutorial

[real tutorial](https://wiki.archlinux.org/title/RabbitMQ)

run

- `sudo pacman -S rabbitmq`
- `sudo systemctl enable rabbitmq.service`

open this file: rabbitmq-env.conf

- `code /etc/rabbitmq/rabbitmq-env.conf`
- Put your ip address into "NODE_IP_ADDRESS"

run

- `sudo rabbitmq-plugins enable rabbitmq_management`
- `sudo rabbitmq-plugins enable rabbitmq_shovel rabbitmq_shovel_management`

On your `/etc/hosts`, verify the name of the localhost

`127.0.0.1 localhost` or `127.0.0.1 rabbitmq`

in a browser

- `http://localhost:15672/#/`
- login with username=`guest` password=`guest`

Correct your code with the good credentials and connectionsParameters

```python
# vv-- code to edit --vv

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(
    'localhost', 5672, '/', credentials)

# vv-- normal code --vv

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
```
