import tkinter as tk
from paho.mqtt import client as mqtt_client

# MQTT setup
broker = 'your_broker_address'
port = 1883
topic = "car/control"
client_id = 'tkinter-mqtt-client'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Sent `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

client = connect_mqtt()

# Tkinter GUI
def send_command(command):
    publish(client, command)

root = tk.Tk()
root.title("Robotic Car Controller")

# Create buttons for each command
tk.Button(root, text="Forward", command=lambda: send_command("F")).pack(pady=10)
tk.Button(root, text="Backward", command=lambda: send_command("B")).pack(pady=10)
tk.Button(root, text="Left", command=lambda: send_command("L")).pack(pady=10)
tk.Button(root, text="Right", command=lambda: send_command("R")).pack(pady=10)
tk.Button(root, text="Stop", command=lambda: send_command("S")).pack(pady=10)
tk.Button(root, text="Manual Mode", command=lambda: send_command("M")).pack(pady=10)
tk.Button(root, text="Auto Mode", command=lambda: send_command("A")).pack(pady=10)

root.mainloop()
