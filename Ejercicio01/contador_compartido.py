import threading
import time

contador = 0
contador_sincronizado = 0
lock = threading.Lock()


def incrementar_sin_sincronizacion():
    global contador
    for _ in range(1000):
        temp = contador
        time.sleep(0.0001)
        contador = temp + 1


def incrementar_con_sincronizacion():
    global contador_sincronizado
    for _ in range(1000):
        with lock:
            temp = contador_sincronizado
            time.sleep(0.0001)
            contador_sincronizado = temp + 1


def ejecutar_sin_sincronizacion():
    global contador
    contador = 0
    hilos = []
    print("=" * 60)
    print("SIN SINCRONIZACIÓN (Condición de carrera)")
    print("=" * 60)
    for i in range(5):
        hilo = threading.Thread(target=incrementar_sin_sincronizacion)
        hilos.append(hilo)
        hilo.start()
    for hilo in hilos:
        hilo.join()
    print(f"Valor esperado: 5,000")
    print(f"Valor obtenido: {contador}")
    print(f"Diferencia: {5000 - contador}")


def ejecutar_con_sincronizacion():
    global contador_sincronizado
    contador_sincronizado = 0
    hilos = []
    print("=" * 60)
    print("CON SINCRONIZACIÓN (Mutex/Lock)")
    print("=" * 60)
    for i in range(5):
        hilo = threading.Thread(target=incrementar_con_sincronizacion)
        hilos.append(hilo)
        hilo.start()
    for hilo in hilos:
        hilo.join()
    print(f"Valor esperado: 5,000")
    print(f"Valor obtenido: {contador_sincronizado}")
    print(f"Resultado: {'✓ CORRECTO' if contador_sincronizado == 5000 else '✗ INCORRECTO'}")


if __name__ == "__main__":
    ejecutar_sin_sincronizacion()
    ejecutar_con_sincronizacion()


