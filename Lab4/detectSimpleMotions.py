import paho.mqtt.client as mqtt
import json
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import time

"""****************************************************************************"""
# Define global variables to store data
prev_acc = {"ACC_X": 0, "ACC_Y": 0, "ACC_Z": 0}
push_threshold = 0.7
lift_threshold = 0.5

# Initialize lists to store true and predicted labels
true_labels = [] # ouput determined by measurements
predicted_labels = [] # output determined by theoretical thresholding


# Define actions
ACTIONS = ["Forward Push", "Upward Lift", "No Action"]

# Define features and target variable
features = []
target = []

"""****************************************************************************"""
def classify_action(data):
    global prev_acc
    try:
        delta_x = abs(data["ACC_X"] - prev_acc["ACC_X"])
        delta_y = abs(data["ACC_Y"] - prev_acc["ACC_Y"])
        delta_z = abs(data["ACC_Z"] - prev_acc["ACC_Z"])
        prev_acc = data

        if delta_x > push_threshold:
            return ACTIONS[0]  # Forward Push
        elif delta_z > lift_threshold:
            return ACTIONS[1]  # Upward Lift
        else:
            return ACTIONS[2]  # No Action
    except Exception as e:
        print("Error checking acceleration:", e)
        return "UNKNOWN"
"""****************************************************************************"""
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180da/william/lab4/imu", qos=1)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        true_label = classify_action(data)
        predicted_label = true_label

        true_labels.append(true_label)
        predicted_labels.append(predicted_label)

        features.append([data["ACC_X"], data["ACC_Y"], data["ACC_Z"]])
        target.append(classify_action(data))

        print("True Label:", true_label)
    except Exception as e:
        print("Error processing message:", e)
"""****************************************************************************"""
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

time.sleep(60)

client.loop_stop()
"""****************************************************************************"""
# Train a Decision Tree classifier
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("Confusion Matrix:")
print(conf_matrix)
print("\nAccuracy:", accuracy)
