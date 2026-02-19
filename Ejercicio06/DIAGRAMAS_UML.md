# Diagramas UML - Ejercicio 06: Deadlock Intencional

## Diagrama de Clases

```uml
@startuml
class SistemaDeadlock {
    - recurso_a: Lock
    - recurso_b: Lock
    + hilo_1()
    + hilo_2()
    + hilo_1_sin_deadlock()
    + hilo_2_sin_deadlock()
    + ejecutar_con_deadlock()
    + ejecutar_sin_deadlock()
}

class Hilo {
    - hilo_id: int
    + adquirir_recurso_a()
    + adquirir_recurso_b()
    + liberar_recursos()
    + trabajar_con_recursos()
}

class RecursoA {
    - lock: Lock
    + adquirir()
    + liberar()
}

class RecursoB {
    - lock: Lock
    + adquirir()
    + liberar()
}

class Lock {
    + acquire()
    + release()
}

SistemaDeadlock --> Hilo : "crea 2 instancias"
SistemaDeadlock --> RecursoA : "gestiona"
SistemaDeadlock --> RecursoB : "gestiona"
Hilo ..> RecursoA : "adquiere/libera"
Hilo ..> RecursoB : "adquiere/libera"

note right of SistemaDeadlock
    Demuestra deadlock y su prevención
    mediante orden consistente de recursos
end note

note bottom of Hilo
    Versión con deadlock:
    Hilo1: A->B, Hilo2: B->A
    Versión sin deadlock:
    Ambos: A->B
end note

@enduml
```

## Diagrama de Uso (Casos de Uso)

```uml
@startuml
actor "Hilo 1" as H1
actor "Hilo 2" as H2

rectangle "Sistema con Deadlock" {
    usecase "Adquirir Recurso A" as UC1
    usecase "Adquirir Recurso B" as UC2
    usecase "Trabajar con recursos" as UC3
    usecase "Liberar Recurso A" as UC4
    usecase "Liberar Recurso B" as UC5
    usecase "Esperar indefinidamente" as UC6
}

rectangle "Sistema sin Deadlock" {
    usecase "Adquirir Recurso A (ordenado)" as UC7
    usecase "Adquirir Recurso B (ordenado)" as UC8
    usecase "Trabajar con recursos" as UC9
    usecase "Liberar Recurso B" as UC10
    usecase "Liberar Recurso A" as UC11
}

H1 --> UC1 : "versión con deadlock"
H1 --> UC2
H1 --> UC3
H1 --> UC4
H1 --> UC5

H2 --> UC2 : "versión con deadlock"
H2 --> UC1
H2 --> UC3
H2 --> UC5
H2 --> UC4

H1 --> UC6 : "si deadlock ocurre"
H2 --> UC6 : "si deadlock ocurre"

H1 --> UC7 : "versión sin deadlock"
H1 --> UC8
H1 --> UC9
H1 --> UC10
H1 --> UC11

H2 --> UC7 : "versión sin deadlock"
H2 --> UC8
H2 --> UC9
H2 --> UC10
H2 --> UC11

UC1 ..> UC2 : "Hilo 1: orden A->B"
UC2 ..> UC1 : "Hilo 2: orden B->A (deadlock)"
UC7 ..> UC8 : "Ambos: orden A->B (sin deadlock)"

note right of UC6
    Deadlock: ambos hilos
    esperan indefinidamente
end note

note bottom of UC7
    Orden consistente previene
    el deadlock
end note

@enduml
```
