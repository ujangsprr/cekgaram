from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

# Membaca dataset dari file CSV
df = pd.read_csv('synthetic_salt_quality_dataset.csv')

# Memisahkan fitur dan label
X = df[['Kadar Garam (%)', 'Kadar Air (%)']]  # Fitur: Kadar Garam dan Kadar Air
y = df['Kualitas']  # Label: Kualitas

# Memisahkan data menjadi set pelatihan dan pengujian
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Membuat model KNN
knn = KNeighborsClassifier(n_neighbors=5)

# Melatih model dengan data pelatihan
knn.fit(X_train, y_train)

# Memprediksi label untuk data pengujian
y_pred = knn.predict(X_test)

# Menghitung akurasi
accuracy = accuracy_score(y_test, y_pred)
print(f'Akurasi model: {accuracy}')

# Menyimpan model ke file
model_file = 'knn_model.joblib'
joblib.dump(knn, model_file)
print(f'Model telah disimpan sebagai {model_file}')