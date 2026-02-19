# Diagramas UML - Ejercicio 01: Contador Compartido

## Diagrama de Clases

```uml
@startuml
class ContadorCompartido {
    - contador: int
    - contador_sincronizado: int
    - lock: Lock
    + incrementar_sin_sincronizacion()
    + incrementar_con_sincronizacion()
    + ejecutar_sin_sincronizacion()
    + ejecutar_con_sincronizacion()
}

class Thread {
    + start()
    + join()
    + is_alive()
}

class Lock {
    + acquire()
    + release()
}

ContadorCompartido --> Thread : "crea 5 instancias"
ContadorCompartido --> Lock : "usa para sincronización"
Thread ..> ContadorCompartido : "ejecuta métodos"

note right of ContadorCompartido
    Demuestra condiciones de carrera
    y su solución con locks
end note

@enduml
```

## Diagrama de Uso (Casos de Uso)

```uml
@startuml
actor "Hilo 1" as H1
actor "Hilo 2" as H2
actor "Hilo 3" as H3
actor "Hilo 4" as H4
actor "Hilo 5" as H5

rectangle "Sistema de Contador" {
    usecase "Incrementar sin sincronización" as UC1
    usecase "Incrementar con sincronización" as UC2
    usecase "Adquirir lock" as UC3
    usecase "Liberar lock" as UC4
    usecase "Leer contador" as UC5
    usecase "Escribir contador" as UC6
}

H1 --> UC1
H2 --> UC1
H3 --> UC1
H4 --> UC1
H5 --> UC1

H1 --> UC2
H2 --> UC2
H3 --> UC2
H4 --> UC2
H5 --> UC2

UC2 --> UC3
UC2 --> UC5
UC2 --> UC6
UC2 --> UC4

UC1 --> UC5
UC1 --> UC6

note right of UC1
    Puede causar condiciones
    de carrera
end note

note right of UC2
    Protegido con lock,
    garantiza atomicidad
end note

@enduml
```
