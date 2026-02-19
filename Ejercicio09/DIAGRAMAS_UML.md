# Diagramas UML - Ejercicio 09: Cola de Tareas Concurrente

## Diagrama de Clases

```uml
@startuml
class SistemaColaTareas {
    - cola_tareas: Queue
    - estadisticas: Dict
    - produccion_finalizada: Event
    + productor_tareas(productor_id: int, num_tareas: int)
    + consumidor_tareas(consumidor_id: int)
    + ejecutar()
}

class ProductorTareas {
    - productor_id: int
    - num_tareas: int
    + crear_tarea(): Tarea
    + agregar_tarea(tarea: Tarea)
    + finalizar_produccion()
}

class ConsumidorTareas {
    - consumidor_id: int
    - tareas_procesadas: int
    + obtener_tarea(): Tarea
    + procesar_tarea(tarea: Tarea)
    + verificar_finalizacion(): bool
}

class ColaTareas {
    - items: Queue
    + put(item: Tarea)
    + get(timeout: float): Tarea
    + task_done()
    + join()
    + empty(): bool
}

class Tarea {
    - id: str
    - productor: int
    - prioridad: int
    - tiempo_procesamiento: float
}

class Event {
    + set()
    + clear()
    + is_set(): bool
}

SistemaColaTareas --> ProductorTareas : "crea 3 instancias"
SistemaColaTareas --> ConsumidorTareas : "crea 2 instancias"
SistemaColaTareas --> ColaTareas : "gestiona"
SistemaColaTareas --> Event : "usa para sincronización"
ProductorTareas ..> ColaTareas : "agrega tareas"
ConsumidorTareas ..> ColaTareas : "obtiene tareas"
ConsumidorTareas ..> Tarea : "procesa"

note right of SistemaColaTareas
    Coordina productores y consumidores
    usando cola thread-safe y eventos
end note

@enduml
```

## Diagrama de Uso (Casos de Uso)

```uml
@startuml
actor "Productor 1" as P1
actor "Productor 2" as P2
actor "Productor 3" as P3
actor "Consumidor 1" as C1
actor "Consumidor 2" as C2

rectangle "Sistema Cola de Tareas" {
    usecase "Crear tarea" as UC1
    usecase "Agregar tarea a cola" as UC2
    usecase "Obtener tarea de cola" as UC3
    usecase "Procesar tarea" as UC4
    usecase "Marcar tarea completada" as UC5
    usecase "Verificar producción finalizada" as UC6
    usecase "Esperar timeout" as UC7
    usecase "Finalizar consumidor" as UC8
    usecase "Registrar estadísticas" as UC9
}

P1 --> UC1
P1 --> UC2
P1 --> UC9
P2 --> UC1
P2 --> UC2
P2 --> UC9
P3 --> UC1
P3 --> UC2
P3 --> UC9

C1 --> UC3
C1 --> UC4
C1 --> UC5
C1 --> UC6
C1 --> UC7
C1 --> UC8
C1 --> UC9

C2 --> UC3
C2 --> UC4
C2 --> UC5
C2 --> UC6
C2 --> UC7
C2 --> UC8

UC3 --> UC7 : "si cola vacía"
UC3 --> UC4 : "si hay tarea"
UC4 --> UC5 : "después de procesar"
UC6 --> UC8 : "si producción finalizada y cola vacía"
UC6 --> UC3 : "si producción continúa"

note right of UC2
    Operación thread-safe
    automática
end note

note bottom of UC3
    Timeout para evitar
    espera indefinida
end note

note left of UC6
    Verifica evento de
    finalización de producción
end note

@enduml
```
