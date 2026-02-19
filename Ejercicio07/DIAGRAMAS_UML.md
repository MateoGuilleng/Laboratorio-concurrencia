# Diagramas UML - Ejercicio 07: Filósofos Comensales

## Diagrama de Clases

```uml
@startuml
class SistemaFilosofosComensales {
    - NUM_FILOSOFOS: int = 5
    - tenedores: List[Lock]
    - mesa: Semaphore
    - estadisticas: Dict
    + filosofo(filosofo_id: int)
    + ejecutar()
}

class Filosofo {
    - filosofo_id: int
    - tenedor_izq: int
    - tenedor_der: int
    - comidas: int
    + pensar()
    + adquirir_acceso_mesa()
    + adquirir_tenedores()
    + comer()
    + liberar_tenedores()
    + liberar_acceso_mesa()
}

class Tenedor {
    - tenedor_id: int
    - lock: Lock
    + adquirir()
    + liberar()
}

class Mesa {
    - capacidad: int = 4
    - semaphore: Semaphore
    + adquirir_acceso()
    + liberar_acceso()
}

class Estadisticas {
    - comidas: List[int]
    - tiempo_espera: List[float]
    - lock: Lock
    + registrar_comida(filosofo_id: int)
    + registrar_tiempo_espera(filosofo_id: int, tiempo: float)
    + analizar_inanicion(): bool
}

SistemaFilosofosComensales --> Filosofo : "crea 5 instancias"
SistemaFilosofosComensales --> Tenedor : "gestiona 5 tenedores"
SistemaFilosofosComensales --> Mesa : "gestiona acceso"
SistemaFilosofosComensales --> Estadisticas : "registra datos"
Filosofo ..> Tenedor : "usa 2 tenedores"
Filosofo ..> Mesa : "solicita acceso"
Filosofo ..> Estadisticas : "registra actividad"

note right of SistemaFilosofosComensales
    Resuelve deadlock e inanición
    usando semáforo de mesa y
    ordenamiento de tenedores
end note

@enduml
```

## Diagrama de Uso (Casos de Uso)

```uml
@startuml
actor "Filósofo 1" as F1
actor "Filósofo 2" as F2
actor "Filósofo 3" as F3
actor "Filósofo 4" as F4
actor "Filósofo 5" as F5

rectangle "Sistema Filósofos Comensales" {
    usecase "Pensar" as UC1
    usecase "Adquirir acceso a mesa" as UC2
    usecase "Adquirir tenedor izquierdo" as UC3
    usecase "Adquirir tenedor derecho" as UC4
    usecase "Comer" as UC5
    usecase "Liberar tenedor derecho" as UC6
    usecase "Liberar tenedor izquierdo" as UC7
    usecase "Liberar acceso a mesa" as UC8
    usecase "Registrar estadísticas" as UC9
}

F1 --> UC1
F1 --> UC2
F1 --> UC3
F1 --> UC4
F1 --> UC5
F1 --> UC6
F1 --> UC7
F1 --> UC8
F1 --> UC9

F2 --> UC1
F2 --> UC2
F2 --> UC3
F2 --> UC4
F2 --> UC5
F3 --> UC1
F3 --> UC2
F4 --> UC1
F4 --> UC2
F5 --> UC1
F5 --> UC2

UC2 --> UC3 : "debe adquirir primero"
UC3 --> UC4 : "orden consistente"
UC4 --> UC5 : "tiene ambos tenedores"
UC5 --> UC6 : "después de comer"
UC6 --> UC7 : "orden inverso"
UC7 --> UC8 : "libera acceso"
UC5 --> UC9 : "registra actividad"

note right of UC2
    Máximo 4 filósofos
    simultáneamente (previene deadlock)
end note

note bottom of UC3
    Ordenamiento consistente
    de tenedores previene deadlock
end note

note left of UC9
    Detecta inanición comparando
    tiempos de espera
end note

@enduml
```
