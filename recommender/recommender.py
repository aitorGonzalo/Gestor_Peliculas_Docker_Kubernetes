from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

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

@app.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        conn = get_db_connection()
        conn.close()
        return "Conexión a la base de datos exitosa", 200
    except Exception as e:
        return f"Error de conexión: {e}", 500

# Ruta de búsqueda de películas
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
