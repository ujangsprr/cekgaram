import pandas as pd
import numpy as np

# Membuat dataset sintetis
qualities = {
    "K1": {"salt_range": (95, 100), "moisture_range": (0, 2)},
    "K2": {"salt_range": (90, 95), "moisture_range": (2, 5)},
    "K3": {"salt_range": (85, 90), "moisture_range": (5, 10)}
}

samples_per_quality = 1000 // len(qualities)
data = []

for quality, ranges in qualities.items():
    for _ in range(samples_per_quality):
        salt_content = np.random.uniform(*ranges["salt_range"])
        moisture_content = np.random.uniform(*ranges["moisture_range"])
        data.append([salt_content, moisture_content, quality])

df = pd.DataFrame(data, columns=["Kadar Garam (%)", "Kadar Air (%)", "Kualitas"])

# Menyimpan dataset ke file CSV
file_path = 'synthetic_salt_quality_dataset.csv'
df.to_csv(file_path, index=False)

print(f"Dataset telah disimpan sebagai {file_path}")