from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import time

# Membaca dataset dari file CSV
df = pd.read_csv('synthetic_salt_quality_dataset.csv')

# Memisahkan fitur dan label
X = df[['Kadar Garam (%)', 'Kadar Air (%)']]  # Fitur: Kadar Garam dan Kadar Air
y = df['Kualitas']  # Label: Kualitas

# Memisahkan data menjadi set pelatihan dan pengujian
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Membuat model KNN
knn = KNeighborsClassifier(n_neighbors=5)

# Inisialisasi list untuk menyimpan akurasi setiap iterasi training
accuracies = []

# Inisialisasi list untuk menyimpan waktu setiap iterasi training
training_times = []

# Jumlah iterasi training yang ingin dilakukan
num_iterations = 100

for i in range(num_iterations):
    start_time = time.time()
    
    # Melatih model dengan data pelatihan
    knn.fit(X_train, y_train)

    # Memprediksi label untuk data pengujian
    y_pred = knn.predict(X_test)

    # Menghitung akurasi
    accuracy = accuracy_score(y_test, y_pred)
    
    end_time = time.time()
    training_time = end_time - start_time
    
    accuracies.append(accuracy)
    training_times.append(training_time)
    
    print(f'Iterasi {i+1} - Akurasi model: {accuracy}, Waktu training: {training_time} detik')

# Menyimpan model ke file
model_file = 'knn_model.joblib'
joblib.dump(knn, model_file)
print(f'Model telah disimpan sebagai {model_file}')

# Membuat plot akurasi dan waktu training
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(range(1, num_iterations+1), accuracies, marker='o')
plt.xlabel('Iterasi')
plt.ylabel('Akurasi')
plt.title('Akurasi Model vs. Iterasi')

plt.subplot(1, 2, 2)
plt.plot(range(1, num_iterations+1), training_times, marker='o')
plt.xlabel('Iterasi')
plt.ylabel('Waktu Training (detik)')
plt.title('Waktu Training vs. Iterasi')

plt.tight_layout()
plt.show()
