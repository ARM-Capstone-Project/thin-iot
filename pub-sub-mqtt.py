# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
import json
import os
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D4)

received_all_event = threading.Event()
target_ep = 'alylqcewl13i8-ats.iot.ap-southeast-1.amazonaws.com'
thing_name = 'ThinPi'
cert_filepath = './../certs/certificate.pem'
private_key_filepath = './../certs/privateKey.pem'
ca_filepath = './../certs/AmazonRootCA1.pem'

pub_topic = 'device/{}/data'.format(thing_name)
sub_topic = 'app/data'
                
# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

proxy_options = None

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=target_ep,
    port=8883,
    cert_filepath=cert_filepath,
    pri_key_filepath=private_key_filepath,
    client_bootstrap=client_bootstrap,
    ca_filepath=ca_filepath,
    client_id=thing_name,
    clean_session=True,
    keep_alive_secs=30,
    http_proxy_options=proxy_options)

print("Connecting to {} with client ID '{}'...".format(target_ep, thing_name))
info = os.uname()
#Connect to the gateway
while True:
  try:
    connect_future = mqtt_connection.connect()
    connect_future.result()
  except:
    print("Connection to IoT Core failed...  retrying in 5s.")
    time.sleep(5)
    continue
  else:
    print("Connected!")
    break

# Subscribe
print("Subscribing to topic " + sub_topic)
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=sub_topic,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received)

subscribe_result = subscribe_future.result()
print("Subscribed with {}".format(str(subscribe_result['qos'])))

while True:
    print ('Publishing message on topic {}'.format(pub_topic))
    print ("===============")

    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        data = ({
            "thing": thing_name,
            "data": {
                "temperature_f": round(temperature_f,1),
                "temperature_c": round(temperature_c,1),
                "humidity": humidity,
            },
            "status": "online",
        })
        
        mqtt_connection.publish(
        topic=pub_topic,
        payload=json.dumps(data),
        qos=mqtt.QoS.AT_LEAST_ONCE)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(15)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(15)