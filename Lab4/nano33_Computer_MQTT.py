
import paho.mqtt.client as mqtt
import json 

# Define a global variable to hold the data from the IMU
imu_data = {}

#define the callback functions
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    
    #subscribe to the same topic as the IMU
    client.subscribe("ece180da/william/lab4/imu", qos=1)
  
def on_disconnect(client, userdata, rc):
  if rc != 0:
    print("Unexpected Disconnect")
  else:
    print('Expected Disconnect') 
    
# this callback will receive the data and print it to the screen
def on_message(client, userdata, message):
    global imu_data
    try:
        data = json.loads(message.payload.decode())
        imu_data = {
            "ACC_X": data["ACC_X"],
            "ACC_Y": data["ACC_Y"],
            "ACC_Z": data["ACC_Z"],
            "GYR_X": data["GYR_X"],
            "GYR_Y": data["GYR_Y"],
            "GYR_Z": data["GYR_Z"]
        }

        # Print ACC data
        acc_data_str = "ACC Data: {:.6f}, {:.6f}, {:.6f}".format(imu_data["ACC_X"], imu_data["ACC_Y"], imu_data["ACC_Z"])
        print(acc_data_str)

        # Print a separator line
        print("-" * 30)

        # Print GYR data
        gyr_data_str = "GYR Data: {:.6f}, {:.6f}, {:.6f}".format(imu_data["GYR_X"], imu_data["GYR_Y"], imu_data["GYR_Z"])
        print(gyr_data_str)

        # Print a separator line
        print("-" * 30)

        # Print Direction labels
        direction_labels = "Direction:   X       Y       Z"
        print(direction_labels)

    except Exception as e: 
        print("Error processing message:", e)

#create client         
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#begin client loop 
client.connect_async('mqtt.eclipseprojects.io')
client.loop_forever()