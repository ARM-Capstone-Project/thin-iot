import time
import json
from awsiot.greengrasscoreipc.model import (
    SubscribeToIoTCoreRequest,
    IoTCoreMessage
)
from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2


class StreamHandler(IoTCoreMessage):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: IoTCoreMessage) -> None:
        try:
            # Decode the payload and print the received message
            message = event.message.payload.decode('utf-8')
            print(f"Received message: {message}")
        except Exception as e:
            print(f"Failed to process the message: {e}")

    def on_stream_error(self, error: Exception) -> bool:
        print(f"Stream error: {error}")
        return True  # Returning True to keep the subscription active

    def on_stream_closed(self) -> None:
        print("Stream closed")


def subscribe_to_topic(topic: str):
    try:
        # Initialize IPC client
        ipc_client = GreengrassCoreIPCClientV2()

        # Create subscription request
        request = SubscribeToIoTCoreRequest()
        request.topic_name = topic
        request.qos = 0  # QoS 0 (At most once delivery)

        # Create stream handler to handle incoming messages
        handler = StreamHandler()

        # Subscribe to the topic
        print(f"Subscribing to topic '{topic}'...")
        operation = ipc_client.subscribe_to_iot_core(request, handler)
        operation.activate()

        # Keep the script running to listen for messages
        while True:
            time.sleep(1)  # Keep the main thread alive for receiving messages

    except Exception as e:
        print(f"Error subscribing to topic '{topic}': {e}")


if __name__ == "__main__":
    # Replace 'app/data' with the topic you want to subscribe to
    subscribe_to_topic("app/data")
