import threading
import time
import random

cruce = threading.Lock()
estadisticas = {
    'autos_pasaron': 0,
    'direcciones': {'Norte': 0, 'Sur': 0, 'Este': 0, 'Oeste': 0},
    'lock': threading.Lock()
}


def auto(auto_id, direccion):
    print(f"[Auto {auto_id}] ({direccion}) Acercándose al cruce...")
    time.sleep(random.uniform(0.1, 0.5))
    print(f"[Auto {auto_id}] ({direccion}) Esperando en el cruce...")
    cruce.acquire()
    try:
        print(f"[Auto {auto_id}] ({direccion}) ⚠ CRUZANDO el cruce...")
        tiempo_cruce = random.uniform(0.5, 1.5)
        time.sleep(tiempo_cruce)
        print(f"[Auto {auto_id}] ({direccion}) ✓ Cruzó exitosamente (tomó {tiempo_cruce:.2f}s)")
        with estadisticas['lock']:
            estadisticas['autos_pasaron'] += 1
            estadisticas['direcciones'][direccion] += 1
    finally:
        cruce.release()
        print(f"[Auto {auto_id}] ({direccion}) Liberó el cruce")


def generar_trafico(num_autos):
    direcciones = ['Norte', 'Sur', 'Este', 'Oeste']
    hilos = []
    for i in range(num_autos):
        direccion = random.choice(direcciones)
        hilo = threading.Thread(target=auto, args=(i+1, direccion))
        hilos.append(hilo)
        hilo.start()
        time.sleep(random.uniform(0.1, 0.3))
    for hilo in hilos:
        hilo.join()


def ejecutar():
    print("=" * 60)
    print("EJERCICIO 10: SIMULACIÓN DE TRÁFICO")
    print("=" * 60)
    print("Cruce: Una sola vía")
    print("Capacidad: 1 auto a la vez")
    print("Autos: 10\n")
    estadisticas['autos_pasaron'] = 0
    for direccion in estadisticas['direcciones']:
        estadisticas['direcciones'][direccion] = 0
    generar_trafico(10)
    print("\n" + "=" * 60)
    print("ESTADÍSTICAS:")
    print("=" * 60)
    print(f"Total de autos que cruzaron: {estadisticas['autos_pasaron']}")
    print("\nPor dirección:")
    for direccion, cantidad in estadisticas['direcciones'].items():
        print(f"  {direccion}: {cantidad} autos")
    print("\n✓ Simulación completada sin colisiones ni bloqueos\n")


if __name__ == "__main__":
    ejecutar()

