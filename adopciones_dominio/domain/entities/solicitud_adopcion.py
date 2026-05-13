"""
Entidad de dominio: SolicitudAdopcion.

Python puro — sin dependencias de framework ni base de datos.
Contiene el método de fábrica crear() que centraliza las reglas
de negocio del flujo de adopción.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from domain.exceptions import MaxSolicitudesExcedidoError, MascotaNoDisponibleError

if TYPE_CHECKING:
    from .adoptante import Adoptante
    from .mascota import Mascota


class EstadoSolicitud(str, Enum):
    """Estados posibles de una solicitud de adopción."""

    PENDIENTE = "pendiente"
    EN_REVISION = "en_revision"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    CANCELADA = "cancelada"


@dataclass
class SolicitudAdopcion:
    """
    Representa la solicitud formal de adopción de una mascota.

    Atributos
    ---------
    id : str
        Identificador único (UUID como cadena).
    adoptante_id : str
        ID del adoptante que realiza la solicitud.
    mascota_id : str
        ID de la mascota solicitada.
    estado : EstadoSolicitud
        Estado actual de la solicitud.
    fecha_creacion : datetime
        Fecha y hora de creación (UTC).
    """

    id: str
    adoptante_id: str
    mascota_id: str
    estado: EstadoSolicitud
    fecha_creacion: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    # ------------------------------------------------------------------
    # Método de fábrica — punto central de las reglas de negocio
    # ------------------------------------------------------------------

    @classmethod
    def crear(cls, adoptante: "Adoptante", mascota: "Mascota") -> "SolicitudAdopcion":
        """
        Crea una nueva solicitud de adopción validando las reglas de negocio.

        Reglas que se verifican (en orden):
        1. El adoptante no debe tener solicitudes activas (máx. 1).
        2. La mascota debe estar en estado DISPONIBLE.

        Si ambas reglas se cumplen:
        - Se genera un nuevo ID único para la solicitud.
        - Se marca la mascota como EN_PROCESO.
        - Se registra la solicitud en la lista del adoptante.
        - Se retorna la nueva SolicitudAdopcion en estado PENDIENTE.

        Parameters
        ----------
        adoptante : Adoptante
            El adoptante que realiza la solicitud.
        mascota : Mascota
            La mascota que se desea adoptar.

        Returns
        -------
        SolicitudAdopcion
            Nueva solicitud en estado PENDIENTE.

        Raises
        ------
        MaxSolicitudesExcedidoError
            Si el adoptante ya tiene una solicitud activa.
        MascotaNoDisponibleError
            Si la mascota no está en estado DISPONIBLE.
        """
        # Regla 1: el adoptante no puede tener más de 1 solicitud activa.
        if not adoptante.puede_solicitar():
            raise MaxSolicitudesExcedidoError(adoptante_id=adoptante.id)

        # Regla 2: solo se pueden solicitar mascotas disponibles.
        if not mascota.esta_disponible():
            raise MascotaNoDisponibleError(
                mascota_id=mascota.id,
                estado_actual=mascota.estado.value,
            )

        # Ambas reglas OK — crear la solicitud.
        solicitud_id = str(uuid.uuid4())

        nueva_solicitud = cls(
            id=solicitud_id,
            adoptante_id=adoptante.id,
            mascota_id=mascota.id,
            estado=EstadoSolicitud.PENDIENTE,
        )

        # Efectos colaterales en el dominio (sin tocar DB):
        mascota.marcar_en_proceso()
        adoptante.agregar_solicitud_activa(solicitud_id)

        return nueva_solicitud

    # ------------------------------------------------------------------
    # Consultas de estado
    # ------------------------------------------------------------------

    def esta_activa(self) -> bool:
        """Retorna True si la solicitud se encuentra en un estado activo."""
        return self.estado in (
            EstadoSolicitud.PENDIENTE,
            EstadoSolicitud.EN_REVISION,
            EstadoSolicitud.APROBADA,
        )

    def __repr__(self) -> str:
        return (
            f"SolicitudAdopcion(id={self.id!r}, adoptante_id={self.adoptante_id!r}, "
            f"mascota_id={self.mascota_id!r}, estado={self.estado.value!r})"
        )
