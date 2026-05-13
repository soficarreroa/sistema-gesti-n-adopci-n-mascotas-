"""
Entidad de dominio: Mascota.

Python puro — sin dependencias de framework ni base de datos.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class EstadoMascota(str, Enum):
    """Estados posibles de una mascota en el sistema."""

    DISPONIBLE = "disponible"
    EN_PROCESO = "en_proceso"
    ADOPTADA = "adoptada"


@dataclass
class Mascota:
    """
    Representa una mascota disponible para adopción.

    Atributos
    ---------
    id : str
        Identificador único (UUID como cadena).
    nombre : str
        Nombre de la mascota.
    estado : EstadoMascota
        Estado actual dentro del flujo de adopción.
    especie : str
        Especie (ej. "perro", "gato").
    raza : str
        Raza de la mascota.
    edad_meses : int
        Edad en meses.
    fotos : list[str]
        URLs de las fotos de la mascota.
    """

    id: str
    nombre: str
    estado: EstadoMascota
    especie: str
    raza: str
    edad_meses: int
    fotos: List[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Reglas de negocio
    # ------------------------------------------------------------------

    def esta_disponible(self) -> bool:
        """
        Retorna True si la mascota puede ser solicitada en adopción.

        Regla: solo las mascotas con estado DISPONIBLE pueden ser
        solicitadas. Una mascota EN_PROCESO o ADOPTADA no puede
        recibir nuevas solicitudes.
        """
        return self.estado == EstadoMascota.DISPONIBLE

    def marcar_en_proceso(self) -> None:
        """
        Transiciona el estado de la mascota a EN_PROCESO.

        Se invoca cuando se acepta una solicitud de adopción.
        Precondición: la mascota debe estar DISPONIBLE.
        La validación de precondición la hace SolicitudAdopcion.crear().
        """
        self.estado = EstadoMascota.EN_PROCESO

    def marcar_adoptada(self) -> None:
        """Transiciona el estado de la mascota a ADOPTADA."""
        self.estado = EstadoMascota.ADOPTADA

    def marcar_disponible(self) -> None:
        """
        Retorna la mascota al estado DISPONIBLE.

        Se usa cuando una solicitud es rechazada o cancelada.
        """
        self.estado = EstadoMascota.DISPONIBLE

    def __repr__(self) -> str:
        return (
            f"Mascota(id={self.id!r}, nombre={self.nombre!r}, "
            f"estado={self.estado.value!r})"
        )
