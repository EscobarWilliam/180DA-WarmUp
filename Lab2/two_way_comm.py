#In this code, we create a 2-way communication where we utalize two 
#files under the same server. This allows to receive data only from the
#other user and not from ourselves. There was no way to read the other 
#users id, so we embedded the users name into the message that they send


import paho.mqtt.client as mqtt

myClientId = "William"

# define callbacks - functions that run when events happen.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("fromuser2touser1")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, msg):
    message_payload = msg.payload.decode()
    print('\n')
    print("Received message " + message_payload)
    

# create an instance of a client with a specific client ID
client = mqtt.Client(client_id=myClientId)

# bind the client to the callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connect the client to the server
client.connect_async("mqtt.eclipseprojects.io")

client.loop_start()

while True:
    message = input("Enter your message: ")
    print('\n')
    client.publish("user1touser2", "from " + myClientId + ": " + message)

client.loop_stop()   # Stop the loop to avoid blocking the main thread
client.disconnect()
