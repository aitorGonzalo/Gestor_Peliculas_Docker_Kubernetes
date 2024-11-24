from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)  

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

    query = "SELECT title, release_year AS releaseYear, genres, imdb_average_rating AS rating FROM movies WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE %s"
        params.append(f"%{title}%")
    if genre:
        query += " AND genres LIKE %s"
        params.append(f"%{genre}%")
    if year:
        query += " AND release_year = %s"
        params.append(year)

    query += " ORDER BY imdb_average_rating DESC LIMIT 10"
    cursor.execute(query, params)
    movies = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(movies)


# Ruta de registro
@app.route('/register', methods=['POST'])
def register():
    print("Ruta /register llamada")  
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

    
    start = int(request.args.get('start', 0))  # Valor por defecto: 0
    limit = int(request.args.get('limit', 5))  # Valor por defecto: 5

    
    query = """
        SELECT id, title, release_year AS releaseYear, genres, imdb_average_rating AS rating
        FROM movies
        LIMIT %s OFFSET %s
    """
    cursor.execute(query, (limit, start))
    movies = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(movies)

@app.route('/rate_movie', methods=['POST'])
def rate_movie():
    data = request.get_json()
    print("Datos recibidos en /rate_movie:", data)  

    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    rating = data.get('rating')
    comment = data.get('comment')

   
    if not user_id or not movie_id or rating is None or not comment:
        print("Datos incompletos:", data)  
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

@app.route('/add_movie', methods=['POST'])
def add_movie():
    data = request.get_json()

    
    required_fields = ["title", "type", "genres", "release_year", "imdb_id", "imdb_average_rating", "imdb_num_votes", "available_countries"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Datos incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO movies (title, type, genres, release_year, imdb_id, imdb_average_rating, imdb_num_votes, available_countries)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data["title"],
                data["type"],
                data["genres"],
                data["release_year"],
                data["imdb_id"],
                data["imdb_average_rating"],
                data["imdb_num_votes"],
                data["available_countries"]
            )
        )
        conn.commit()
        return jsonify({"message": "Película añadida exitosamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

