# import paho.mqtt.client as mqtt
# import json

# # Define global variables to store data
# prev_acc = {"ACC_X": 0, "ACC_Y": 0, "ACC_Z": 0}
# threshold = 0.1  # You can adjust this threshold as needed

# '''*************************************************************************************
# //                               def is_idle()
# // This is a function, that when called, will determine if the IMU is idle or not.  
# // The way it achieves this is by taking the difference between the current data 
# // and the previous reading. This is simply a test, but for a game where our players
# // are constantly moving, we would need to adjust the treshold at which we detect a 
# // motion.  
# //*************************************************************************************'''
# def is_idle(data):
#     global prev_acc
#     try:
#         #we measure our data by taking the difference between 
#         #present and past readings
#         delta_x = abs(data["ACC_X"] - prev_acc["ACC_X"])
#         delta_y = abs(data["ACC_Y"] - prev_acc["ACC_Y"])
#         delta_z = abs(data["ACC_Z"] - prev_acc["ACC_Z"])
#         prev_acc = data  # Update previous acceleration values
#         if delta_x < threshold and delta_y < threshold and delta_z < threshold:
#             return True #i.e. is idle 
#         else:
#             return False
#     except Exception as e:
#         print("Error checking acceleration:", e)
#         return False

# '''//*************************************************************************************
# //                             Callback functions
# //*************************************************************************************'''
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))
#     client.subscribe("ece180da/william/lab4/imu")


# def on_message(client, userdata, msg):
#     try:
#         data = json.loads(msg.payload.decode())
#         if is_idle(data):
#             print("IDLE")
#         else:
#             print("NOT IDLE")
#     except Exception as e:
#         print("Error processing message:", e)


# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect_async('mqtt.eclipseprojects.io')
# client.loop_forever()
import paho.mqtt.client as mqtt
import json
from sklearn.metrics import confusion_matrix, accuracy_score
import time

# Define global variables to store data
prev_acc = {"ACC_X": 0, "ACC_Y": 0, "ACC_Z": 0}
threshold = 0.1  # You can adjust this threshold as needed

# Initialize lists to store true and predicted labels
true_labels = []
predicted_labels = []

def is_idle(data):
    global prev_acc
    try:
        delta_x = abs(data["ACC_X"] - prev_acc["ACC_X"])
        delta_y = abs(data["ACC_Y"] - prev_acc["ACC_Y"])
        delta_z = abs(data["ACC_Z"] - prev_acc["ACC_Z"])
        prev_acc = data  # Update previous acceleration values
        if delta_x < threshold and delta_y < threshold and delta_z < threshold:
            return True  # i.e. is idle
        else:
            return False
    except Exception as e:
        print("Error checking acceleration:", e)
        return False

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    
    # subscribe to the same topic as the IMU
    client.subscribe("ece180da/william/lab4/imu", qos=1)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        true_label = "IDLE" if is_idle(data) else "NOT IDLE"
        predicted_label = "IDLE" if true_label == "IDLE" else "NOT IDLE"

        # Append true and predicted labels to lists
        true_labels.append(true_label)
        predicted_labels.append(predicted_label)

        print(true_label)
    except Exception as e:
        print("Error processing message:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

# Run for a certain period of time or until you have enough data
time.sleep(60)  # Adjust the sleep duration as needed

# Stop the loop to calculate metrics
client.loop_stop()

# Print confusion matrix and accuracy
conf_matrix = confusion_matrix(true_labels, predicted_labels, labels=["IDLE", "NOT IDLE"])
accuracy = accuracy_score(true_labels, predicted_labels)

print("Confusion Matrix:")
print(conf_matrix)
print("\nAccuracy:", accuracy)
