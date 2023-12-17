import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

# Mengambil dataset dari file CSV
file_path = 'synthetic_salt_quality_dataset.csv'  # Ganti dengan path file Anda
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

# Encode 'Kualitas' column numerically
label_encoder = LabelEncoder()
df['Kualitas'] = label_encoder.fit_transform(df['Kualitas'])

# Separate features (X) and label (y) for KNN model
X = df[['Kadar Air (%)', 'Kadar Garam (%)']]
y = df['Kualitas']

# Initialize KNN model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X, y)

# Meshgrid for KNN value plot
x_min, x_max = X['Kadar Air (%)'].min() - 1, X['Kadar Air (%)'].max() + 1
y_min, y_max = X['Kadar Garam (%)'].min() - 1, X['Kadar Garam (%)'].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))

# Predictions on meshgrid
Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Contour plot with KNN decision boundaries
plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, alpha=0.4, cmap='viridis')
plt.scatter(X['Kadar Air (%)'], X['Kadar Garam (%)'], c=y, s=20, edgecolor='k')
plt.xlabel('Kadar Air (%)')
plt.ylabel('Kadar Garam (%)')
plt.title('Batas Keputusan KNN untuk Kualitas Garam')
plt.grid(True)
plt.show()
