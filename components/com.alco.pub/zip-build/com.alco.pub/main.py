import time
import json
import random
from awsiot.greengrasscoreipc.model import PublishToIoTCoreRequest
from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from datetime import datetime
# Create an IPC client instance
ipc_client = GreengrassCoreIPCClientV2()

def publish_data():
    while True:
        try:
            # Simulate temperature and humidity data
            temperature_c = round(random.uniform(20.0, 30.0), 1)  # Temperature between 20°C and 30°C
            temperature_f = round(temperature_c * (9 / 5) + 32, 1)  # Convert to Fahrenheit
            humidity = round(random.uniform(40.0, 70.0), 1)  # Humidity between 40% and 70%

            # Prepare the JSON payload

            payload = {
                "deviceId": "DHT22-002",
                "timestamp": datetime.utcnow().isoformat() + "Z",  # UTC timestamp
                "readings": [
                    {
                        "sensor": "temperature",
                        "unit": "celsius",
                        "value": temperature_c
                    },
                    {
                        "sensor": "temperature",
                        "unit": "fahrenheit",
                        "value": temperature_f
                    },
                    {
                        "sensor": "humidity",
                        "unit": "percentage",
                        "value": humidity
                    }
                ]
            }
            # Convert payload to JSON string
            message = json.dumps(payload)

            # Create the PublishToIoTCoreRequest
            request = PublishToIoTCoreRequest()
            request.topic_name = "raspi/data"
            request.payload = bytes(message, "utf-8")
            request.qos = 0  # QoS 0 (At most once delivery)

            # Publish the message to the topic
            ipc_client.publish_to_iot_core(request)

            print(f"Published to topic 'raspi/data': {message}")
        
        except Exception as e:
            print(f"Error publishing message: {str(e)}")
        
        # Sleep for a few seconds before publishing again
        time.sleep(5)

# Run the publish function
if __name__ == "__main__":
    publish_data()
