# Diagramas UML - Ejercicio 02: Cajeros Automáticos

## Diagrama de Clases

```uml
@startuml
class SistemaBancario {
    - saldo: float
    - lock_cuenta: Lock
    + retirar(cajero_id: int, monto: float, usar_lock: bool): bool
    + cajero_automatico(cajero_id: int, num_retiros: int, usar_lock: bool)
    + ejecutar_sin_sincronizacion()
    + ejecutar_con_sincronizacion()
}

class CajeroAutomatico {
    - cajero_id: int
    - retiros_exitosos: int
    - retiros_rechazados: int
    + realizar_retiros()
}

class CuentaBancaria {
    - saldo: float
    + verificar_saldo(monto: float): bool
    + retirar(monto: float): bool
}

class Lock {
    + acquire()
    + release()
}

SistemaBancario --> CajeroAutomatico : "crea 3 instancias"
SistemaBancario --> CuentaBancaria : "gestiona"
SistemaBancario --> Lock : "usa para sincronización"
CajeroAutomatico ..> CuentaBancaria : "realiza retiros"

note right of SistemaBancario
    Protege operaciones bancarias
    para evitar saldo negativo
end note

@enduml
```

## Diagrama de Uso (Casos de Uso)

```uml
@startuml
actor "Cajero 1" as C1
actor "Cajero 2" as C2
actor "Cajero 3" as C3

rectangle "Sistema Bancario" {
    usecase "Verificar saldo" as UC1
    usecase "Realizar retiro" as UC2
    usecase "Adquirir lock" as UC3
    usecase "Liberar lock" as UC4
    usecase "Actualizar saldo" as UC5
}

C1 --> UC1
C1 --> UC2
C2 --> UC1
C2 --> UC2
C3 --> UC1
C3 --> UC2

UC2 --> UC3 : "con sincronización"
UC2 --> UC1
UC2 --> UC5
UC2 --> UC4 : "con sincronización"

note right of UC2
    Operación crítica que debe
    ser atómica para evitar
    saldo negativo
end note

note bottom of UC3
    Garantiza acceso exclusivo
    a la cuenta bancaria
end note

@enduml
```
