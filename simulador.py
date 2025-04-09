# simulador.py
import threading
import time
import random

# Asientos simulados (solo hay 1 asiento disponible para el ejemplo)
asiento_disponible = {"A1"}
lock = threading.Lock()

def intentar_reservar(usuario_id):
    global asiento_disponible
    print(f"[Usuario {usuario_id}] Intentando reservar...")

    with lock:  # simula una transacción
        if asiento_disponible:
            asiento = asiento_disponible.pop()
            print(f"[Usuario {usuario_id}] ¡Reserva exitosa del asiento {asiento}!")
        else:
            print(f"[Usuario {usuario_id}] El asiento ya fue reservado por otro.")

def simular_usuarios(numero_usuarios):
    hilos = []

    for i in range(numero_usuarios):
        hilo = threading.Thread(target=intentar_reservar, args=(i+1,))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()
