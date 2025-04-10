import os
import time
import random
import threading
import psycopg2
from psycopg2 import sql

# Config db
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": 5432
}

def simular_usuario(isolation_level, usuario_id):
    conn = None
    intentos = 3
    for _ in range(intentos):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            break  # Si la conexión es exitosa, sal del bucle
        except psycopg2.OperationalError:
            time.sleep(2)  # Espera 2 segundos antes de reintentar
    if not conn:
        print(f"Usuario {usuario_id}: No se pudo conectar a la BD")
        return False

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(isolation_level)
        cursor = conn.cursor()

        # reservar asiento aleatorio disponible
        cursor.execute("SELECT id FROM asiento WHERE estado = 'disponible' ORDER BY RANDOM() LIMIT 1;")
        asiento = cursor.fetchone()

        if asiento:
            asiento_id = asiento[0]
            cursor.execute("UPDATE asiento SET estado = 'reservado' WHERE id = %s;", (asiento_id,))
            cursor.execute("INSERT INTO reserva (usuario_id, asiento_id) VALUES (%s, %s);", (usuario_id, asiento_id))
            conn.commit()
            print(f"Usuario {usuario_id}: Reserva exitosa (Asiento {asiento_id})")
            return True
        else:
            print(f"Usuario {usuario_id}: No hay asientos disponibles")
            return False

    except Exception as e:
        if conn:  # Verificar si existe antes de rollback
            conn.rollback()
        print(f"Usuario {usuario_id}: Error - {str(e)}")
        return False
    finally:
        if conn:  # Verificar si existe antes de cerrar
            conn.close()

def ejecutar_prueba(num_usuarios, isolation_level):

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reserva;")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error al limpiar tabla reserva: {str(e)}")


    start_time = time.time()
    threads = []
    exitos = 0

    # Crear y ejecutar hilos
    for i in range(num_usuarios):
        t = threading.Thread(target=simular_usuario, args=(isolation_level, i))
        threads.append(t)
        t.start()

    # Esperar a que todos los hilos terminen
    for t in threads:
        t.join()

    # Contar reservas exitosas
    try:
        
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM reserva;")
        total_reservas = cursor.fetchone()[0]
        exitos = total_reservas  # Simplificación para el ejemplo
    except Exception as e:
        print(f"Error al contar reservas: {str(e)}")
    finally:
        conn.close()

    tiempo_promedio = (time.time() - start_time) * 1000 / num_usuarios
    return exitos, num_usuarios - exitos, round(tiempo_promedio, 2)

if __name__ == "__main__":
    niveles_aislamiento = {
        "READ COMMITTED": psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
        "REPEATABLE READ": psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ,
        "SERIALIZABLE": psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
    }

    usuarios_prueba = [5, 10, 20, 30]

    print("| Usuarios | Aislamiento     | Exitosas | Fallidas | Tiempo Promedio |")
    print("|----------|-----------------|----------|----------|------------------|")

    for usuarios in usuarios_prueba:
        for nombre_nivel, nivel_codigo in niveles_aislamiento.items():
            exitos, fallidos, tiempo = ejecutar_prueba(usuarios, nivel_codigo)
            print(f"| {usuarios:<8} | {nombre_nivel:<15} | {exitos:<8} | {fallidos:<8} | {tiempo:<16}ms |")
