# Semi Tutorial

[real tutorial 1](https://wiki.archlinux.org/title/RabbitMQ)
[real tutorial 2](https://citizix.com/how-to-install-and-configure-rabbitmq-in-archlinux/)

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

-----------------------------------

`rabbitmq-plugins enable rabbitmq_mqtt` ?

```text
sudo rabbitmq-server start -detached
sudo systemctl enable rabbitmq.service
sudo rabbitmq-plugins enable rabbitmq_management
sudo rabbitmq-plugins enable rabbitmq_shovel rabbitmq_shovel_management
sudo rabbitmqctl start_app
```

```text
sudo rabbitmq-server start -detached
sudo systemctl enable rabbitmq.service
sudo rabbitmqctl start_app
```

`sudo systemctl status rabbitmq.service`

Managing on Ubuntu / Debian Based Systems

```text
# To start the service:
service rabbitmq-server start

# To stop the service:
service rabbitmq-server stop

# To restart the service:
service rabbitmq-server restart
    
# To check the status:
service rabbitmq-server status
```
