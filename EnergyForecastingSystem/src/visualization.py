import os
import matplotlib.pyplot as plt
from src.config import SAMPLE_DATA_PATH, TARGET_COLUMN, GRAPHS_DIR
from src.data_loader import load_dataset

df, _ = load_dataset(SAMPLE_DATA_PATH)
df.set_index("Datetime", inplace=True)

plt.figure(figsize=(12, 5))
plt.plot(df.index[:500], df[TARGET_COLUMN][:500], color="#06b6d4")
plt.title("Indian Electricity Demand Over Time")
plt.xlabel("Time")
plt.ylabel(TARGET_COLUMN)

os.makedirs(GRAPHS_DIR, exist_ok=True)
out_graph = os.path.join(GRAPHS_DIR, "energy_consumption.png")
plt.savefig(out_graph, dpi=300)
plt.close()
print(f"Saved visualization graph to: {out_graph}")