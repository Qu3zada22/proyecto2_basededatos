# main.py
from simulador import simular_usuarios

if __name__ == "__main__":
    for cantidad in [5, 10, 20, 30]:
        print(f"\n>>> Simulando con {cantidad} usuarios simultáneos:\n")
        simular_usuarios(cantidad)
