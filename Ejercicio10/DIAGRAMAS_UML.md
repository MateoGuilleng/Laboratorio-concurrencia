# Diagramas UML - Ejercicio 10: Simulación de Tráfico

## Diagrama de Clases

```uml
@startuml
class SistemaTrafico {
    - cruce: Lock
    - estadisticas: Dict
    + auto(auto_id: int, direccion: str)
    + generar_trafico(num_autos: int)
    + ejecutar()
}

class Auto {
    - auto_id: int
    - direccion: str
    + acercarse_al_cruce()
    + esperar_en_cruce()
    + cruzar()
    + liberar_cruce()
}

class Cruce {
    - lock: Lock
    - capacidad: int = 1
    + adquirir_acceso()
    + liberar_acceso()
    + esta_disponible(): bool
}

class Estadisticas {
    - autos_pasaron: int
    - direcciones: Dict[str, int]
    - lock: Lock
    + registrar_auto(direccion: str)
    + obtener_estadisticas(): Dict
}

class Lock {
    + acquire()
    + release()
}

SistemaTrafico --> Auto : "crea múltiples instancias"
SistemaTrafico --> Cruce : "gestiona"
SistemaTrafico --> Estadisticas : "registra datos"
Auto ..> Cruce : "usa para cruzar"
Auto ..> Estadisticas : "registra paso"

note right of SistemaTrafico
    Simula cruce de tráfico
    con exclusión mutua usando lock
end note

@enduml
```

## Diagrama de Uso (Casos de Uso)

```uml
@startuml
actor "Auto Norte 1" as AN1
actor "Auto Sur 1" as AS1
actor "Auto Este 1" as AE1
actor "Auto Oeste 1" as AO1
actor "Auto Norte 2" as AN2

rectangle "Sistema de Tráfico" {
    usecase "Acercarse al cruce" as UC1
    usecase "Esperar en cruce" as UC2
    usecase "Adquirir acceso al cruce" as UC3
    usecase "Cruzar el cruce" as UC4
    usecase "Registrar paso" as UC5
    usecase "Liberar acceso al cruce" as UC6
}

AN1 --> UC1
AN1 --> UC2
AN1 --> UC3
AN1 --> UC4
AN1 --> UC5
AN1 --> UC6

AS1 --> UC1
AS1 --> UC2
AS1 --> UC3
AS1 --> UC4
AE1 --> UC1
AE1 --> UC2
AE1 --> UC3
AO1 --> UC1
AO1 --> UC2
AO1 --> UC3
AN2 --> UC1
AN2 --> UC2

UC2 --> UC3 : "espera si ocupado"
UC3 --> UC4 : "adquiere acceso exclusivo"
UC4 --> UC5 : "registra estadísticas"
UC5 --> UC6 : "libera para siguiente auto"

note right of UC3
    Solo un auto puede
    adquirir acceso a la vez
end note

note bottom of UC4
    Tiempo variable de cruce
    (0.5-1.5 segundos)
end note

note left of UC5
    Registra dirección y
    contador total
end note

@enduml
```
