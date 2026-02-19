# Diagramas UML - Ejercicio 03: Productor-Consumidor

## Diagrama de Clases

```uml
@startuml
class SistemaProductorConsumidor {
    - buffer: List[str]
    - BUFFER_SIZE: int = 5
    - buffer_lock: Lock
    - espacios_disponibles: Semaphore
    - items_disponibles: Semaphore
    + productor(productor_id: int)
    + consumidor(consumidor_id: int)
    + ejecutar()
}

class Productor {
    - productor_id: int
    + producir_item(): str
    + agregar_al_buffer(item: str)
}

class Consumidor {
    - consumidor_id: int
    - items_consumidos: int
    + consumir_del_buffer(): str
    + procesar_item(item: str)
}

class Buffer {
    - items: List[str]
    - capacidad: int
    + agregar(item: str)
    + remover(): str
    + esta_lleno(): bool
    + esta_vacio(): bool
}

class Semaphore {
    - contador: int
    + acquire()
    + release()
}

class Lock {
    + acquire()
    + release()
}

SistemaProductorConsumidor --> Productor : "crea 2 instancias"
SistemaProductorConsumidor --> Consumidor : "crea 2 instancias"
SistemaProductorConsumidor --> Buffer : "gestiona"
SistemaProductorConsumidor --> Semaphore : "usa 2 semáforos"
SistemaProductorConsumidor --> Lock : "usa para buffer"
Productor ..> Buffer : "agrega items"
Consumidor ..> Buffer : "remueve items"

note right of SistemaProductorConsumidor
    Coordina productores y consumidores
    usando semáforos y locks
end note

@enduml
```

## Diagrama de Uso (Casos de Uso)

```uml
@startuml
actor "Productor 1" as P1
actor "Productor 2" as P2
actor "Consumidor 1" as C1
actor "Consumidor 2" as C2

rectangle "Sistema Productor-Consumidor" {
    usecase "Producir item" as UC1
    usecase "Adquirir espacio disponible" as UC2
    usecase "Agregar al buffer" as UC3
    usecase "Señalar item disponible" as UC4
    usecase "Adquirir item disponible" as UC5
    usecase "Remover del buffer" as UC6
    usecase "Consumir item" as UC7
    usecase "Señalar espacio disponible" as UC8
    usecase "Proteger buffer con lock" as UC9
}

P1 --> UC1
P1 --> UC2
P1 --> UC3
P1 --> UC4
P2 --> UC1
P2 --> UC2
P2 --> UC3
P2 --> UC4

C1 --> UC5
C1 --> UC6
C1 --> UC7
C1 --> UC8
C2 --> UC5
C2 --> UC6
C2 --> UC7
C2 --> UC8

UC3 --> UC9
UC6 --> UC9

UC2 ..> UC3 : "debe adquirir primero"
UC5 ..> UC6 : "debe adquirir primero"

note right of UC2
    Espera si buffer está lleno
end note

note right of UC5
    Espera si buffer está vacío
end note

@enduml
```
