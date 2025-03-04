import paho.mqtt.client as mqtt
import time
import os

host = "test.mosquitto.org"
port = 1883
file_path = "solve.txt"

def on_connect(client, userdata, flags, rc):
    print("MQTT Connected.")
    client.subscribe("iloveaut/rubik/command")

def on_message(client, userdata, msg):
    print(f"Received MQTT message: {msg.payload.decode('utf-8')}")

def publish_once_if_new(client):
    last_published_message = ""  # Store last published message to prevent re-publishing
    
    while True:
        try:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r') as f:
                    received_message = f.read().strip()

                if received_message and received_message != last_published_message:
                    client.publish("iloveaut/rubik/command", received_message)
                    last_published_message = received_message  # Store last published message

                    # Clear the file after publishing
                    open(file_path, 'w').close()
                    print("Published and cleared message.")

        except Exception as e:
            print(f"Error handling file: {e}")

        time.sleep(1)  # Check the file every 1 second

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(host, port, 60)

# Run the file-monitoring function in parallel
import threading
threading.Thread(target=publish_once_if_new, args=(client,), daemon=True).start()

client.loop_forever()
