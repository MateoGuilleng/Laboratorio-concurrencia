import threading
import time
import random

BUFFER_SIZE = 5
buffer = []
buffer_lock = threading.Lock()
espacios_disponibles = threading.Semaphore(BUFFER_SIZE)
items_disponibles = threading.Semaphore(0)
buffer_condition = threading.Condition(buffer_lock)


def productor(productor_id):
    global buffer
    for i in range(10):
        item = f"Item-{productor_id}-{i+1}"
        espacios_disponibles.acquire()
        with buffer_lock:
            buffer.append(item)
            print(f"[Productor {productor_id}] Produjo: {item} | Buffer: {len(buffer)}/{BUFFER_SIZE}")
        items_disponibles.release()
        time.sleep(random.uniform(0.1, 0.3))
    print(f"[Productor {productor_id}] Finalizó su trabajo")


def consumidor(consumidor_id):
    global buffer
    items_consumidos = 0
    while items_consumidos < 10:
        items_disponibles.acquire()
        with buffer_lock:
            if buffer:
                item = buffer.pop(0)
                print(f"[Consumidor {consumidor_id}] Consumió: {item} | Buffer: {len(buffer)}/{BUFFER_SIZE}")
                items_consumidos += 1
        espacios_disponibles.release()
        time.sleep(random.uniform(0.1, 0.3))
    print(f"[Consumidor {consumidor_id}] Finalizó su trabajo")


def ejecutar():
    print("=" * 60)
    print("EJERCICIO 3: PRODUCTOR-CONSUMIDOR CON BUFFER LIMITADO")
    print("=" * 60)
    print(f"Buffer size: {BUFFER_SIZE}")
    print(f"Productores: 2")
    print(f"Consumidores: 2\n")
    global buffer
    buffer.clear()
    hilos = []
    for i in range(2):
        hilo = threading.Thread(target=productor, args=(i+1,))
        hilos.append(hilo)
        hilo.start()
    for i in range(2):
        hilo = threading.Thread(target=consumidor, args=(i+1,))
        hilos.append(hilo)
        hilo.start()
    for hilo in hilos:
        hilo.join()
    print(f"\nBuffer final: {buffer}")
    print(f"Estado: {'✓ Correcto' if len(buffer) == 0 else '✗ Hay items sin consumir'}\n")


if __name__ == "__main__":
    ejecutar()

