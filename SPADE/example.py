import paho.mqtt.client as mqtt


# Callback function for when a client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Client connected with result code: " + str(rc))

    # Publish a message when the client is connected (replace with your desired topic and message)
    client.publish("display_value", 5)


# Create an MQTT client instance
client = mqtt.Client()

# Set the callback function
client.on_connect = on_connect

# Connect to the MQTT broker (replace the broker address and port with your own)
client.connect("localhost", 1883)

# Start the MQTT loop to process incoming and outgoing messages
client.loop_start()

# Continue with your program logic or sleep to keep the script running
while True:
    pass

# Disconnect from the MQTT broker
client.loop_stop()
client.disconnect()
