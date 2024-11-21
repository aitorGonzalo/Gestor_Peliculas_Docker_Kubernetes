from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os

app = FastAPI()

# Middleware para permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen (puedes especificar dominios aquí)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Configuración de conexión a la base de datos MySQL
db_config = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'aitor'),
    'password': os.getenv('DB_PASSWORD', '1234'),
    'database': os.getenv('DB_NAME', 'movie_db'),
    'charset': 'utf8mb4'
}

def get_db_connection():
    return mysql.connector.connect(**db_config, use_pure=True)

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI Movie Service!"}

@app.get("/similar_movies")
def get_similar_movies(title: str, rating_tolerance: float = Query(0.5, ge=0.1, le=2.0)):
    """
    Busca películas similares basadas en el género y la valoración de una película dada.
    
    Parámetros:
    - `title`: El título de la película de referencia.
    - `rating_tolerance`: Tolerancia para la valoración (por defecto 0.5).
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Buscar la película de referencia
        query_ref = """
        SELECT genres, imdb_average_rating
        FROM movies
        WHERE title LIKE %s
        LIMIT 1
        """
        cursor.execute(query_ref, (f"%{title}%",))
        ref_movie = cursor.fetchone()

        if not ref_movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        genre = ref_movie['genres']
        rating = ref_movie['imdb_average_rating']

        # Buscar películas similares
        query_similar = """
        SELECT title, genres, imdb_average_rating AS rating, release_year
        FROM movies
        WHERE genres LIKE %s
          AND ABS(imdb_average_rating - %s) <= %s
          AND title NOT LIKE %s
        ORDER BY ABS(imdb_average_rating - %s), release_year DESC
        LIMIT 10
        """
        cursor.execute(query_similar, (f"%{genre}%", rating, rating_tolerance, f"%{title}%", rating))
        similar_movies = cursor.fetchall()

        return {
            "reference_movie": {"title": title, "genres": genre, "rating": rating},
            "similar_movies": similar_movies
        }
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
    finally:
        cursor.close()
        conn.close()
