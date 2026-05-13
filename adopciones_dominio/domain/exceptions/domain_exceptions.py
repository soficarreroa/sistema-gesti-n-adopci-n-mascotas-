"""
Excepciones de dominio del sistema de adopciones.

Estas excepciones representan violaciones a las reglas de negocio.
No dependen de ningún framework ni base de datos.
"""


class DomainError(Exception):
    """Clase base para todas las excepciones de dominio."""

    def __init__(self, mensaje: str) -> None:
        self.mensaje = mensaje
        super().__init__(mensaje)

    def __str__(self) -> str:
        return self.mensaje


class MaxSolicitudesExcedidoError(DomainError):
    """
    Se lanza cuando un adoptante intenta crear una solicitud
    pero ya tiene una solicitud activa (pendiente, en revisión o aprobada).

    Regla: un adoptante solo puede tener 1 solicitud activa a la vez.
    """

    def __init__(self, adoptante_id: str) -> None:
        super().__init__(
            f"El adoptante '{adoptante_id}' ya tiene una solicitud activa. "
            "Solo se permite 1 solicitud activa por adoptante."
        )
        self.adoptante_id = adoptante_id


class MascotaNoDisponibleError(DomainError):
    """
    Se lanza cuando se intenta solicitar una mascota cuyo estado
    no es 'disponible' (ej. ya está en proceso o fue adoptada).
    """

    def __init__(self, mascota_id: str, estado_actual: str) -> None:
        super().__init__(
            f"La mascota '{mascota_id}' no está disponible para adopción. "
            f"Estado actual: '{estado_actual}'."
        )
        self.mascota_id = mascota_id
        self.estado_actual = estado_actual


class AdoptanteNoRegistradoError(DomainError):
    """
    Se lanza cuando se intenta operar con un adoptante
    que no está registrado en el sistema.
    """

    def __init__(self, adoptante_id: str) -> None:
        super().__init__(
            f"El adoptante '{adoptante_id}' no está registrado en el sistema."
        )
        self.adoptante_id = adoptante_id
