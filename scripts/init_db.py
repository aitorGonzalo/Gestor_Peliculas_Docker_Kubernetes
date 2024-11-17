import mysql.connector
import time

# Espera unos segundos para asegurarse de que MySQL está en funcionamiento
time.sleep(10)

try:
   
    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="1234",
        database="movie_db",
        allow_local_infile=True
    )

    cursor = conn.cursor()

    
    with open('/var/lib/mysql-files/db_init.sql', 'r') as f:
        sql_statements = f.read().split(';')  

    for statement in sql_statements:
        statement = statement.strip()
        if statement:  # Ejecuta solo si la sentencia no está vacía
            cursor.execute(statement)
            print(f"Ejecutado: {statement}")

    conn.commit()
    print("Base de datos inicializada correctamente.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
