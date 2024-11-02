from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)  # Permitir solicitudes CORS desde cualquier origen

# Configuración de conexión a MySQL
db_config = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'aitor'),
    'password': os.getenv('DB_PASSWORD', '1234'),
    'database': os.getenv('DB_NAME', 'movie_db'),
    'charset': 'utf8mb4'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config, use_pure=True)
    print("Conexión exitosa a la base de datos")
    return conn

@app.route('/recommender', methods=['GET'])
def recommender():
    title = request.args.get('title', '')
    genre = request.args.get('genre', '')
    year = request.args.get('year', None)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Construcción dinámica de la consulta
    query = "SELECT title, releaseYear, genres, imdbAverageRating AS rating FROM movies WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE %s"
        params.append(f"%{title}%")
    if genre:
        query += " AND genres LIKE %s"
        params.append(f"%{genre}%")
    if year:
        query += " AND releaseYear = %s"
        params.append(year)

    query += " ORDER BY imdbAverageRating DESC LIMIT 10"
    cursor.execute(query, params)
    movies = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(movies)

# Ruta de registro
@app.route('/register', methods=['POST'])
def register():
    print("Ruta /register llamada")  # Añadir este mensaje
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, password))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            # Devuelve el user_id junto con el mensaje de éxito
            return jsonify({"message": "Login successful", "user_id": user['id']}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    finally:
        cursor.close()
        conn.close()

@app.route('/catalog', methods=['GET'])
def catalog():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id,title, releaseYear, genres, imdbAverageRating AS rating FROM movies")
    movies = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(movies)

@app.route('/rate_movie', methods=['POST'])
def rate_movie():
    data = request.get_json()
    print("Datos recibidos en /rate_movie:", data)  # Verificar los datos en el log

    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    rating = data.get('rating')
    comment = data.get('comment')

    # Verificar que todos los datos están presentes
    if not user_id or not movie_id or rating is None or not comment:
        print("Datos incompletos:", data)  # Imprime los datos incompletos
        return jsonify({"error": "Datos incompletos"}), 400

    if not (1 <= int(float(rating)) <= 10):
        return jsonify({"error": "Rating must be between 1 and 10"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO valoraciones (user_id, movie_id, rating, comment) VALUES (%s, %s, %s, %s)",
                       (user_id, movie_id, rating, comment))
        conn.commit()
        return jsonify({"message": "Review submitted successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()
