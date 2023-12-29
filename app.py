from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import hashlib
import mysql.connector
from mysql.connector import Error
import joblib
import os

app = Flask(__name__)

secret_key = os.urandom(24)
app.secret_key = secret_key

# Memuat model
model = joblib.load('model/knn_model.joblib')

# Konfigurasi database
db_config = {
    'host': 'localhost',
    'database': 'garam',
    'user': 'root',
    'password': ''
}

# Fungsi untuk membuat koneksi ke database
def create_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Error: {e}")
        return None
    return connection

def calculate_knn(kadar_garam, kadar_air):
    prediction = model.predict([[kadar_garam, kadar_air]])[0]
    return prediction

@app.route('/testpredict', methods=['GET', 'POST'])
def testpredict():
    kadar_garam = ""
    kadar_air = ""
    prediction = ""
    if request.method == 'POST':
        kadar_garam = float(request.form['kadar_garam'])
        kadar_air = float(request.form['kadar_air'])
        prediction = model.predict([[kadar_garam, kadar_air]])[0]
    return render_template('testpredict.html', prediction=prediction, kadar_garam=kadar_garam, kadar_air=kadar_air)

# Register account route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
         # Encrypt the password using MD5
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO user (nama, email, password) VALUES (%s, %s, %s)"
            try:
                cursor.execute(query, (name, email, hashed_password))
                conn.commit()
            except Error as e:
                flash(f"Error: {e}", 'error')
            finally:
                cursor.close()
                conn.close()
            return redirect(url_for('login'))
        else:
            flash("Database connection failed", 'error')
    return render_template("register.html")

# Login account route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        try:
            conn = create_db_connection()
            with conn.cursor(buffered=True) as cursor:
                query = "SELECT id_user, password, role FROM user WHERE email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                if user and user[1] == hashed_password:
                    session['user_id'] = user[0]  # id_user
                    session['role'] = user[2]    # role
                    if user[2] == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    else:
                        return redirect(url_for('dashboard'))
                else:
                    flash("Login failed. Please check your credentials.", 'error')
        except Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            if conn:
                conn.close()
    return render_template("login.html")

@app.route("/logout")
def logout():
    # Remove user data from session
    session.pop('user_id', None)
    # Redirect to login page or home page
    return redirect(url_for('index'))

# Route untuk menambahkan data ke tabel garam
@app.route('/add_garam', methods=['POST'])
def add_tambak():
    data = request.get_json()
    id_user = data['id_user']
    kadar_air = data['kadar_air']
    kadar_garam = data['kadar_garam']

    conn = create_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Menyimpan data ke tabel garam
            query_garam = "INSERT INTO garam (id_user, kadar_air, kadar_garam) VALUES (%s, %s, %s)"
            cursor.execute(query_garam, (id_user, kadar_air, kadar_garam))
            id_garam = cursor.lastrowid  # Mengambil ID garam yang baru dibuat

            # Menghitung KNN
            hasil_knn = calculate_knn(kadar_garam, kadar_air)

            # Menyimpan hasil KNN ke tabel hasil dengan id_garam
            query_hasil = "INSERT INTO hasil (id_garam, kualitas) VALUES (%s, %s)"
            cursor.execute(query_hasil, (id_garam, hasil_knn))

            conn.commit()
            return jsonify({'message': 'Data dan hasil KNN berhasil ditambahkan'}), 201
        except mysql.connector.Error as e:
            conn.rollback()
            return jsonify({'message': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'message': 'Koneksi database gagal'}), 500

@app.route("/dashboard")
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    data_dashboard = []  # Mendefinisikan variabel di luar blok try
    conn = create_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Pertama, mengambil data user
            query_user = "SELECT * FROM user WHERE id_user = %s"
            cursor.execute(query_user, (user_id,))
            user_data = cursor.fetchone()

            if not user_data:
                flash('Error retrieving user data', 'error')
                return redirect(url_for('login'))
            
            # Check the user's role
            if user_data[4] == 'admin':
                return redirect(url_for('admin_dashboard'))  # Redirect to the admin dashboard

            # Query untuk mendapatkan semua ID garam yang dimiliki oleh petani
            query_garam_ids = "SELECT id_garam FROM garam WHERE id_user = %s"
            cursor.execute(query_garam_ids, (user_id,))
            garam_ids = cursor.fetchall()  # This will be a list of tuples

            selected_garam_id = request.form.get('selected_garam_id') if request.method == 'POST' else garam_ids[0][0]

            query_garam = "SELECT * FROM garam_values WHERE id_garam = %s ORDER BY timestamp DESC LIMIT 1"
            cursor.execute(query_garam, (selected_garam_id,))
            garam_data = cursor.fetchone()

            if not garam_data:
              garam_data = (0,)  # Set garam_data to 0 if it's None

            garam_id = garam_data[0]

            query_hasil = "SELECT * FROM hasil WHERE id_garam = %s"
            cursor.execute(query_hasil, (selected_garam_id,))
            hasil_data = cursor.fetchone()

            if not hasil_data:
              hasil_data = (0,)  # Set hasil_data to 0 if it's None

        except mysql.connector.Error as e:
            flash(f'Error retrieving data: {str(e)}', 'error')
        finally:
            cursor.close()
            if conn.is_connected():
                conn.close()

        # Mengirim data user dan data dashboard ke template
        return render_template("dashboard.html", user_data=user_data, garam_data=garam_data, hasil_data=hasil_data, garam_ids=garam_ids)

    flash('Error establishing database connection', 'error')
    return redirect(url_for('login'))

@app.route('/process-selected-garam', methods=['POST'])
def process_selected_garam():
    data = request.json
    selected_garam_id = data.get('selectedGaramId')

    # Process the selected_garam_id
    # For example, retrieve relevant data from database

    return jsonify({'message': 'Data processed successfully', 'selectedGaramId': selected_garam_id})

@app.route("/history")
def history():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    conn = create_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query_user = "SELECT * FROM user WHERE id_user = %s"
            cursor.execute(query_user, (user_id,))
            user_data = cursor.fetchone()

            if not user_data:
                flash('Error retrieving user data', 'error')
                return redirect(url_for('login'))

            # Jalankan query untuk mengambil semua data
            query = """
                SELECT g.*, h.*
                FROM garam AS g
                INNER JOIN hasil AS h ON g.id_garam = h.id_garam
                WHERE g.id_user = %s
                ORDER BY g.timestamp DESC;
            """
            cursor.execute(query, (user_id,))
            data = cursor.fetchall()

        except mysql.connector.Error as e:
            flash(f'Error retrieving data: {str(e)}', 'error')
        finally:
            cursor.close()
            if conn.is_connected():
                conn.close()

        # Buat variabel nomor indeks
        index = 1

        return render_template("history.html", user_data=user_data, data=data, index=index)

    flash('Error establishing database connection', 'error')
    return redirect(url_for('login'))

@app.route("/documentation")
def documentation():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    conn = create_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query_user = "SELECT * FROM user WHERE id_user = %s"
            cursor.execute(query_user, (user_id,))
            user_data = cursor.fetchone()

            if not user_data:
                flash('Error retrieving user data', 'error')
                return redirect(url_for('login'))

        except mysql.connector.Error as e:
            flash(f'Error retrieving data: {str(e)}', 'error')
        finally:
            cursor.close()
            if conn.is_connected():
                conn.close()

        return render_template("documentation.html", user_data=user_data)

    flash('Error establishing database connection', 'error')
    return redirect(url_for('login'))

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/admin")
@app.route("/admin/index")
def admin():
    return render_template("index.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("index.html")

@app.route("/admin/user")
def admin_user():
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)