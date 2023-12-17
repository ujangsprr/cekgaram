import pandas as pd
import matplotlib.pyplot as plt

# Mengambil dataset dari file CSV
file_path = 'synthetic_salt_quality_dataset.csv'
df = pd.read_csv(file_path)

# Membuat scatter plot
qualities = df['Kualitas'].unique()
colors = ['blue', 'green', 'red']  # Warna untuk setiap kualitas
plt.figure(figsize=(8, 6))

for i, quality in enumerate(qualities):
    quality_data = df[df['Kualitas'] == quality]
    plt.scatter(
        quality_data['Kadar Air (%)'],
        quality_data['Kadar Garam (%)'],
        color=colors[i],
        label=quality
    )

plt.xlabel('Kadar Air (%)')
plt.ylabel('Kadar Garam (%)')
plt.title('Plot Kadar Garam dan Kadar Air Berdasarkan Kualitas')
plt.legend()
plt.grid(True)
plt.show()
