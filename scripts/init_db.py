import mysql.connector
import time
time.sleep(10)
# Función para comprobar si MySQL está disponible
def wait_for_mysql():
    max_retries = 10
    delay = 10
    retries = 0

    while retries < max_retries:
        try:
            conn = mysql.connector.connect(
                host="db",
                user="root",
                password="1234",
                database="movie_db",
            )
            conn.close()
            print("MySQL está disponible.")
            return True
        except mysql.connector.Error as err:
            print(f"Esperando a MySQL... (Intento {retries + 1}/{max_retries})")
            time.sleep(delay)
            retries += 1

    print("MySQL no está disponible después de varios intentos.")
    return False

# Esperar a que MySQL esté disponible
if wait_for_mysql():
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
            if statement:  
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
else:
    print("No se pudo conectar a MySQL. Saliendo...")
