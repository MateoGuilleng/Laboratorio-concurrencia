# Diagramas UML - Ejercicio 05: Barrera de Sincronización

## Diagrama de Clases

```uml
@startuml
class SistemaBarrera {
    - NUM_HILOS: int = 5
    - NUM_FASES: int = 3
    - barrera: Barrier
    + tarea_fase(hilo_id: int, fase: int)
    + hilo_trabajador(hilo_id: int)
    + ejecutar()
}

class HiloTrabajador {
    - hilo_id: int
    + ejecutar_fase(fase: int)
    + esperar_en_barrera()
    + completar_todas_fases()
}

class Barrera {
    - participantes: int
    - esperando: int
    + wait(): bool
    + reset()
}

class Fase {
    - numero: int
    - tarea: str
    + ejecutar_tarea()
    + completar()
}

SistemaBarrera --> HiloTrabajador : "crea 5 instancias"
SistemaBarrera --> Barrera : "usa para sincronización"
SistemaBarrera --> Fase : "gestiona 3 fases"
HiloTrabajador ..> Barrera : "espera en barrera"
HiloTrabajador ..> Fase : "ejecuta tareas"

note right of SistemaBarrera
    Coordina múltiples hilos
    en puntos de sincronización
    usando barreras
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

rectangle "Sistema de Barrera" {
    usecase "Iniciar Fase 1" as UC1
    usecase "Completar Fase 1" as UC2
    usecase "Esperar en barrera Fase 1" as UC3
    usecase "Iniciar Fase 2" as UC4
    usecase "Completar Fase 2" as UC5
    usecase "Esperar en barrera Fase 2" as UC6
    usecase "Iniciar Fase 3" as UC7
    usecase "Completar Fase 3" as UC8
    usecase "Esperar en barrera Fase 3" as UC9
    usecase "Finalizar todas las fases" as UC10
}

H1 --> UC1
H1 --> UC2
H1 --> UC3
H1 --> UC4
H1 --> UC5
H1 --> UC6
H1 --> UC7
H1 --> UC8
H1 --> UC9
H1 --> UC10

H2 --> UC1
H2 --> UC2
H2 --> UC3
H3 --> UC1
H3 --> UC2
H3 --> UC3
H4 --> UC1
H4 --> UC2
H4 --> UC3
H5 --> UC1
H5 --> UC2
H5 --> UC3

UC2 --> UC3 : "después de completar"
UC3 ..> UC4 : "cuando todos llegan"
UC5 --> UC6 : "después de completar"
UC6 ..> UC7 : "cuando todos llegan"
UC8 --> UC9 : "después de completar"
UC9 ..> UC10 : "cuando todos llegan"

note right of UC3
    Todos los hilos deben llegar
    antes de continuar
end note

note bottom of UC6
    Sincronización colectiva
    en cada fase
end note

@enduml
```
