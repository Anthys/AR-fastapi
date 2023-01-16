import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO
import sys
# Read the CSV file into a list of strings
with open("exp1.csv", "r") as f:
    lines = f.readlines()

# Remove the lines that start with "//"
lines = [line for line in lines if not line.startswith("//")]

# Convert the list of strings into a single string
csv_data = "".join(lines)
# Read the CSV data into a DataFrame
df = pd.read_csv(StringIO(csv_data), skipinitialspace=True)

n_process = 0

def process_d(d, val):
    if pd.isna(val):
        return d
    if val not in d.keys():
        d[val] = 1
    else:
        d[val] += 1
    return d

if n_process == 0:
    d = {}
    for line in df.values:
        action1 = line[3]
        action2 = line[4]
        d = process_d(d, action1)
        d = process_d(d, action2)
    
    # Data to plot
    labels = []
    gestures = []

    for x, y in d.items():
        labels.append(x)
        gestures.append(y)
    plt.pie(gestures, labels=labels, autopct='%1.0f%%')
    plt.title("Proposed gestures for a file transfer between two devices")
    plt.savefig("exp1.png")
