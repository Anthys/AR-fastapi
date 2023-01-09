import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO
import sys
# Read the CSV file into a list of strings
with open("oui.csv", "r") as f:
    lines = f.readlines()

# Remove the lines that start with "//"
lines = [line for line in lines if not line.startswith("//")]

# Convert the list of strings into a single string
csv_data = "".join(lines)
# Read the CSV data into a DataFrame
df = pd.read_csv(StringIO(csv_data), skipinitialspace=True)


n_process = 1

if n_process == 0:
    time_blueotooth = df[(df['Method'] == "A1") & (df["Failure/Success"] == "S")]["Duration"]
    time_gesture = df[(df['Method'] == "A3") & (df["Failure/Success"] == "S")]["Duration"]

    plt.hist(time_blueotooth, density=True,fc=(1,0,1,.7), lw=2, ec="k")
    plt.hist(time_gesture, density=True, fc=(0,1,1,.7), lw=2, ec="k")
    #time_gesture.hist(density=True, fc=(0,1,1,.7), lw=2)
    plt.ylabel("Percentage of durations")
    plt.xlabel("Time to execute the action (s)")
    plt.title("Histogram for the durations of the action execution")
    plt.legend(["Bluetooth", "In-air P&D"])
    plt.show()
elif n_process == 1:
    labels = ["Success", "Failure"]
    bluetooth_data = df[df['Method'] == "A1"]['Failure/Success']
    in_air_data = df[df['Method'] == "A3"]['Failure/Success']
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("Proportion of successful actions per technique")
    ax1.pie([sum(bluetooth_data == "S"), sum(bluetooth_data == "F")], labels=labels, autopct=lambda x:'{:.0f}'.format(x*bluetooth_data.value_counts().sum()/100))
    ax1.title.set_text("Bluetooth")
    ax2.pie([sum(in_air_data == "S"), sum(in_air_data == "F")], labels=labels, autopct=lambda x:'{:.0f}'.format(x*in_air_data.value_counts().sum()/100))
    ax2.title.set_text("In-air")
    plt.show()