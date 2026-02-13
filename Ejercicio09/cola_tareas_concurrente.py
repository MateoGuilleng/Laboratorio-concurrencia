import threading
import time
import random
import queue

cola_tareas = queue.Queue()
estadisticas = {
    'tareas_agregadas': 0,
    'tareas_procesadas': 0,
    'lock': threading.Lock()
}
produccion_finalizada = threading.Event()


def productor_tareas(productor_id, num_tareas):
    for i in range(num_tareas):
        tarea = {
            'id': f"Tarea-{productor_id}-{i+1}",
            'productor': productor_id,
            'prioridad': random.randint(1, 5),
            'tiempo_procesamiento': random.uniform(0.5, 2.0)
        }
        cola_tareas.put(tarea)
        with estadisticas['lock']:
            estadisticas['tareas_agregadas'] += 1
        print(f"[Productor {productor_id}] Agregó: {tarea['id']} (prioridad: {tarea['prioridad']})")
        time.sleep(random.uniform(0.1, 0.3))
    print(f"[Productor {productor_id}] Finalizó (produjo {num_tareas} tareas)")


def consumidor_tareas(consumidor_id):
    tareas_procesadas = 0
    while True:
        try:
            tarea = cola_tareas.get(timeout=1.0)
            print(f"[Consumidor {consumidor_id}] Procesando: {tarea['id']} (prioridad: {tarea['prioridad']}, tiempo: {tarea['tiempo_procesamiento']:.2f}s)")
            time.sleep(tarea['tiempo_procesamiento'])
            print(f"[Consumidor {consumidor_id}] Completó: {tarea['id']}")
            with estadisticas['lock']:
                estadisticas['tareas_procesadas'] += 1
            tareas_procesadas += 1
            cola_tareas.task_done()
        except queue.Empty:
            if produccion_finalizada.is_set() and cola_tareas.empty():
                break
    print(f"[Consumidor {consumidor_id}] Finalizó (procesó {tareas_procesadas} tareas)")


def ejecutar():
    print("=" * 60)
    print("EJERCICIO 9: COLA DE TAREAS CONCURRENTE")
    print("=" * 60)
    print("Productores: 3")
    print("Consumidores: 2")
    print("Tareas por productor: 5\n")
    estadisticas['tareas_agregadas'] = 0
    estadisticas['tareas_procesadas'] = 0
    produccion_finalizada.clear()
    hilos = []
    for i in range(3):
        hilo = threading.Thread(target=productor_tareas, args=(i+1, 5))
        hilos.append(hilo)
        hilo.start()
    for i in range(2):
        hilo = threading.Thread(target=consumidor_tareas, args=(i+1,))
        hilos.append(hilo)
        hilo.start()
    for i in range(3):
        hilos[i].join()
    print("\n[Todos los productores finalizaron]")
    produccion_finalizada.set()
    for i in range(3, 5):
        hilos[i].join()
    cola_tareas.join()
    print("\n" + "=" * 60)
    print("ESTADÍSTICAS:")
    print("=" * 60)
    print(f"Tareas agregadas: {estadisticas['tareas_agregadas']}")
    print(f"Tareas procesadas: {estadisticas['tareas_procesadas']}")
    print(f"Tareas pendientes: {cola_tareas.qsize()}")
    if estadisticas['tareas_agregadas'] == estadisticas['tareas_procesadas']:
        print("✓ Todas las tareas fueron procesadas correctamente")
    else:
        print("✗ Hay tareas sin procesar")
    print("\n✓ Simulación completada\n")


if __name__ == "__main__":
    ejecutar()

