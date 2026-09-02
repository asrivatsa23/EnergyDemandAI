import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/AEP_hourly.csv")

df["Datetime"] = pd.to_datetime(df["Datetime"])

df.set_index("Datetime", inplace=True)

# Plot first 500 records
plt.figure(figsize=(12,5))

plt.plot(df.index[:500], df["AEP_MW"][:500])

plt.title("Energy Consumption Over Time")

plt.xlabel("Time")

plt.ylabel("Energy (MW)")
plt.savefig("../graphs/energy_consumption.png")
plt.show()