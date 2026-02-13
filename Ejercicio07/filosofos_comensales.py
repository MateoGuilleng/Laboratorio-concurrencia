import threading
import time
import random

NUM_FILOSOFOS = 5
tenedores = [threading.Lock() for _ in range(NUM_FILOSOFOS)]
mesa = threading.Semaphore(NUM_FILOSOFOS - 1)
estadisticas = {
    'comidas': [0] * NUM_FILOSOFOS,
    'tiempo_espera': [0.0] * NUM_FILOSOFOS,
    'lock': threading.Lock()
}


def filosofo(filosofo_id):
    tenedor_izq = filosofo_id
    tenedor_der = (filosofo_id + 1) % NUM_FILOSOFOS
    for comida in range(3):
        tiempo_pensar = random.uniform(0.5, 2.0)
        print(f"[Filósofo {filosofo_id}] Pensando... ({tiempo_pensar:.2f}s)")
        time.sleep(tiempo_pensar)
        inicio_espera = time.time()
        print(f"[Filósofo {filosofo_id}] Tiene hambre, intentando comer...")
        mesa.acquire()
        try:
            if tenedor_izq < tenedor_der:
                primero, segundo = tenedor_izq, tenedor_der
            else:
                primero, segundo = tenedor_der, tenedor_izq
            print(f"[Filósofo {filosofo_id}] Adquiriendo tenedor {primero}...")
            tenedores[primero].acquire()
            print(f"[Filósofo {filosofo_id}] Adquiriendo tenedor {segundo}...")
            tenedores[segundo].acquire()
            tiempo_espera = time.time() - inicio_espera
            tiempo_comer = random.uniform(0.5, 1.5)
            print(f"[Filósofo {filosofo_id}] ¡Comiendo! (esperó {tiempo_espera:.2f}s, comerá {tiempo_comer:.2f}s)")
            time.sleep(tiempo_comer)
            with estadisticas['lock']:
                estadisticas['comidas'][filosofo_id] += 1
                estadisticas['tiempo_espera'][filosofo_id] += tiempo_espera
            tenedores[segundo].release()
            tenedores[primero].release()
            print(f"[Filósofo {filosofo_id}] Terminó de comer, liberó tenedores")
        finally:
            mesa.release()
    print(f"[Filósofo {filosofo_id}] Finalizó (comió {estadisticas['comidas'][filosofo_id]} veces)")


def ejecutar():
    print("=" * 60)
    print("EJERCICIO 7: FILÓSOFOS COMENSALES")
    print("=" * 60)
    print(f"Filósofos: {NUM_FILOSOFOS}")
    print(f"Tenedores: {NUM_FILOSOFOS}")
    print("Cada filósofo necesita 2 tenedores para comer\n")
    for i in range(NUM_FILOSOFOS):
        estadisticas['comidas'][i] = 0
        estadisticas['tiempo_espera'][i] = 0.0
    hilos = []
    for i in range(NUM_FILOSOFOS):
        hilo = threading.Thread(target=filosofo, args=(i,))
        hilos.append(hilo)
        hilo.start()
    for hilo in hilos:
        hilo.join()
    print("\n" + "=" * 60)
    print("ESTADÍSTICAS:")
    print("=" * 60)
    for i in range(NUM_FILOSOFOS):
        comidas = estadisticas['comidas'][i]
        tiempo_promedio = (estadisticas['tiempo_espera'][i] / comidas if comidas > 0 else 0)
        print(f"Filósofo {i}: {comidas} comidas, tiempo promedio de espera: {tiempo_promedio:.2f}s")
    tiempos = estadisticas['tiempo_espera']
    max_tiempo = max(tiempos)
    min_tiempo = min([t for t in tiempos if t > 0])
    diferencia = max_tiempo - min_tiempo
    print(f"\nAnálisis de inanición:")
    print(f"  Diferencia máxima de tiempo de espera: {diferencia:.2f}s")
    if diferencia > 5.0:
        print(f"  ⚠ Posible inanición detectada (diferencia > 5s)")
    else:
        print(f"  ✓ No se detectó inanición significativa")
    print("\n✓ Simulación completada\n")


if __name__ == "__main__":
    ejecutar()

