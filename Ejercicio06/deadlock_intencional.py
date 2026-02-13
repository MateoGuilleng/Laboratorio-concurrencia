import threading
import time

recurso_a = threading.Lock()
recurso_b = threading.Lock()


def hilo_1():
    print("[Hilo 1] Iniciado")
    print("[Hilo 1] Intentando adquirir Recurso A...")
    recurso_a.acquire()
    print("[Hilo 1] Adquirió Recurso A")
    time.sleep(0.5)
    print("[Hilo 1] Intentando adquirir Recurso B...")
    recurso_b.acquire()
    print("[Hilo 1] Adquirió Recurso B")
    print("[Hilo 1] Trabajando con Recursos A y B...")
    time.sleep(1)
    recurso_b.release()
    recurso_a.release()
    print("[Hilo 1] Liberó ambos recursos y finalizó")


def hilo_2():
    print("[Hilo 2] Iniciado")
    print("[Hilo 2] Intentando adquirir Recurso B...")
    recurso_b.acquire()
    print("[Hilo 2] Adquirió Recurso B")
    time.sleep(0.5)
    print("[Hilo 2] Intentando adquirir Recurso A...")
    recurso_a.acquire()
    print("[Hilo 2] Adquirió Recurso A")
    print("[Hilo 2] Trabajando con Recursos A y B...")
    time.sleep(1)
    recurso_a.release()
    recurso_b.release()
    print("[Hilo 2] Liberó ambos recursos y finalizó")


def hilo_1_sin_deadlock():
    print("[Hilo 1] Iniciado (sin deadlock)")
    print("[Hilo 1] Intentando adquirir Recurso A...")
    recurso_a.acquire()
    print("[Hilo 1] Adquirió Recurso A")
    time.sleep(0.5)
    print("[Hilo 1] Intentando adquirir Recurso B...")
    recurso_b.acquire()
    print("[Hilo 1] Adquirió Recurso B")
    print("[Hilo 1] Trabajando con Recursos A y B...")
    time.sleep(1)
    recurso_b.release()
    recurso_a.release()
    print("[Hilo 1] Liberó ambos recursos y finalizó")


def hilo_2_sin_deadlock():
    print("[Hilo 2] Iniciado (sin deadlock)")
    print("[Hilo 2] Intentando adquirir Recurso A...")
    recurso_a.acquire()
    print("[Hilo 2] Adquirió Recurso A")
    time.sleep(0.5)
    print("[Hilo 2] Intentando adquirir Recurso B...")
    recurso_b.acquire()
    print("[Hilo 2] Adquirió Recurso B")
    print("[Hilo 2] Trabajando con Recursos A y B...")
    time.sleep(1)
    recurso_b.release()
    recurso_a.release()
    print("[Hilo 2] Liberó ambos recursos y finalizó")


def ejecutar_con_deadlock():
    print("=" * 60)
    print("EJECUTANDO CON DEADLOCK")
    print("=" * 60)
    h1 = threading.Thread(target=hilo_1)
    h2 = threading.Thread(target=hilo_2)
    h1.start()
    h2.start()
    h1.join(timeout=5)
    h2.join(timeout=5)
    if h1.is_alive() or h2.is_alive():
        print("\n✗ DEADLOCK DETECTADO: Los hilos están bloqueados permanentemente")
    else:
        print("\n✓ Los hilos completaron (deadlock no ocurrió en esta ejecución)\n")


def ejecutar_sin_deadlock():
    print("=" * 60)
    print("EJECUTANDO SIN DEADLOCK (SOLUCIÓN)")
    print("=" * 60)
    h1 = threading.Thread(target=hilo_1_sin_deadlock)
    h2 = threading.Thread(target=hilo_2_sin_deadlock)
    h1.start()
    h2.start()
    h1.join()
    h2.join()
    print("\n✓ Todos los hilos completaron correctamente\n")


if __name__ == "__main__":
    ejecutar_con_deadlock()
    time.sleep(2)
    ejecutar_sin_deadlock()

