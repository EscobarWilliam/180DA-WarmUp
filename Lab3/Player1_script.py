import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    
    # Subscribe to the shared results topic
    client.subscribe("game/results")

    # Display the game rules before the game begins
    print('''               RULES: 
          1. You will be asked to enter a letter
                R - Rock
                P - Paper
                S - Scissors
          2. Once your choice is selected, other player makes a choice
          3. The results of the choices will be displayed
          
                        Good Luck!!  ''')

def getUserChoice():
    while True:
        user_input = input("Enter your choice (R, P, or S): ").upper()
        if user_input in ['R', 'P', 'S']:
            return user_input
        else:
            print("Invalid input. Please enter R, P, or S.")

################################################
client = mqtt.Client()
client.on_connect = on_connect

# Connect to the MQTT broker asynchronously
client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

# Game loop
while True:
    user_choice = getUserChoice()
    client.publish("game/choices/player1", user_choice)

    # Wait for the results
    # result_received = False
    # while not result_received:
    #     client.loop()  # Allow the client to process incoming messages
        # Add logic to handle the results when received and set result_received to True
client.loop_stop()
client.disconnect()