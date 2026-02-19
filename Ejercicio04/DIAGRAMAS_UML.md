# Diagramas UML - Ejercicio 04: Lectores y Escritores

## Diagrama de Clases

```uml
@startuml
class SistemaLectoresEscritores {
    - recurso: str
    - lectores_activos: int
    - escritor_activo: bool
    - lectores_sem: Semaphore
    - escritores_sem: Semaphore
    + lector(lector_id: int)
    + escritor(escritor_id: int)
    + ejecutar()
}

class Lector {
    - lector_id: int
    + leer_recurso(): str
    + incrementar_contador()
    + decrementar_contador()
}

class Escritor {
    - escritor_id: int
    + escribir_recurso(nuevo_valor: str)
    + adquirir_acceso_exclusivo()
    + liberar_acceso_exclusivo()
}

class RecursoCompartido {
    - datos: str
    + leer(): str
    + escribir(valor: str)
}

class Semaphore {
    - contador: int
    + acquire()
    + release()
}

SistemaLectoresEscritores --> Lector : "crea múltiples instancias"
SistemaLectoresEscritores --> Escritor : "crea múltiples instancias"
SistemaLectoresEscritores --> RecursoCompartido : "gestiona"
SistemaLectoresEscritores --> Semaphore : "usa 2 semáforos"
Lector ..> RecursoCompartido : "lee"
Escritor ..> RecursoCompartido : "escribe"

note right of SistemaLectoresEscritores
    Prioridad a lectores:
    múltiples lectores simultáneos,
    escritores exclusivos
end note

@enduml
```

## Diagrama de Uso (Casos de Uso)

```uml
@startuml
actor "Lector 1" as L1
actor "Lector 2" as L2
actor "Lector 3" as L3
actor "Escritor 1" as E1
actor "Escritor 2" as E2

rectangle "Sistema Lectores-Escritores" {
    usecase "Leer recurso" as UC1
    usecase "Escribir recurso" as UC2
    usecase "Incrementar contador lectores" as UC3
    usecase "Decrementar contador lectores" as UC4
    usecase "Adquirir acceso exclusivo" as UC5
    usecase "Liberar acceso exclusivo" as UC6
    usecase "Bloquear escritores" as UC7
    usecase "Permitir escritores" as UC8
}

L1 --> UC1
L1 --> UC3
L1 --> UC4
L2 --> UC1
L2 --> UC3
L2 --> UC4
L3 --> UC1
L3 --> UC3
L3 --> UC4

E1 --> UC2
E1 --> UC5
E1 --> UC6
E2 --> UC2
E2 --> UC5
E2 --> UC6

UC3 --> UC7 : "si es primer lector"
UC4 --> UC8 : "si es último lector"
UC5 --> UC2 : "debe adquirir primero"
UC1 --> UC3 : "antes de leer"
UC1 --> UC4 : "después de leer"

note right of UC1
    Múltiples lectores
    pueden leer simultáneamente
end note

note right of UC2
    Solo un escritor
    puede escribir a la vez
end note

note bottom of UC7
    Los lectores bloquean
    a los escritores
end note

@enduml
```
