# Diagramas UML - Ejercicio 08: Recurso Limitado

## Diagrama de Clases

```uml
@startuml
class SistemaRecursoLimitado {
    - impresora: Semaphore
    - impresiones_activas: int
    - lock_contador: Lock
    + usar_impresora(hilo_id: int, documento: str)
    + trabajador(hilo_id: int, documentos: List[str])
    + ejecutar()
}

class Trabajador {
    - hilo_id: int
    - documentos: List[str]
    + imprimir_documentos()
    + solicitar_impresora(documento: str)
}

class Impresora {
    - capacidad: int = 2
    - semaphore: Semaphore
    - usuarios_activos: int
    + adquirir_acceso()
    + liberar_acceso()
    + imprimir(documento: str)
}

class Semaphore {
    - contador: int = 2
    + acquire()
    + release()
}

class Documento {
    - nombre: str
    - tiempo_impresion: float
}

SistemaRecursoLimitado --> Trabajador : "crea 5 instancias"
SistemaRecursoLimitado --> Impresora : "gestiona"
SistemaRecursoLimitado --> Semaphore : "usa para control"
Trabajador ..> Impresora : "usa para imprimir"
Trabajador ..> Documento : "procesa"

note right of SistemaRecursoLimitado
    Controla acceso a recurso
    con capacidad limitada usando
    semáforo contador
end note

@enduml
```

## Diagrama de Uso (Casos de Uso)

```uml
@startuml
actor "Trabajador 1" as T1
actor "Trabajador 2" as T2
actor "Trabajador 3" as T3
actor "Trabajador 4" as T4
actor "Trabajador 5" as T5

rectangle "Sistema de Impresora" {
    usecase "Solicitar acceso a impresora" as UC1
    usecase "Adquirir semáforo" as UC2
    usecase "Iniciar impresión" as UC3
    usecase "Imprimir documento" as UC4
    usecase "Completar impresión" as UC5
    usecase "Liberar semáforo" as UC6
    usecase "Esperar si capacidad llena" as UC7
}

T1 --> UC1
T1 --> UC2
T1 --> UC3
T1 --> UC4
T1 --> UC5
T1 --> UC6

T2 --> UC1
T2 --> UC2
T2 --> UC3
T2 --> UC4
T3 --> UC1
T3 --> UC2
T4 --> UC1
T4 --> UC2
T5 --> UC1
T5 --> UC2

UC1 --> UC2 : "solicita acceso"
UC2 --> UC7 : "si capacidad llena"
UC2 --> UC3 : "si hay espacio"
UC3 --> UC4 : "inicia trabajo"
UC4 --> UC5 : "completa trabajo"
UC5 --> UC6 : "libera recurso"

note right of UC2
    Máximo 2 trabajadores
    simultáneamente
end note

note bottom of UC7
    Espera automáticamente
    hasta que haya espacio
end note

@enduml
```
