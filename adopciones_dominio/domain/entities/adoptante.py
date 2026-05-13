"""
Entidad de dominio: Adoptante.

Python puro — sin dependencias de framework ni base de datos.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


# Importación diferida para evitar ciclo entre entidades.
# SolicitudAdopcion referencia Adoptante y viceversa.
# Usamos TYPE_CHECKING para que solo exista en tiempo de análisis estático.
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .solicitud_adopcion import EstadoSolicitud


# Estados que se consideran "activos" para la regla del máx. 1 solicitud.
ESTADOS_ACTIVOS: frozenset[str] = frozenset(
    {"pendiente", "en_revision", "aprobada"}
)


@dataclass
class Adoptante:
    """
    Representa a una persona que desea adoptar una mascota.

    Atributos
    ---------
    id : str
        Identificador único (UUID como cadena).
    nombre : str
        Nombre completo del adoptante.
    email : str
        Correo electrónico registrado (único en el sistema).
    telefono : str
        Número de contacto.
    solicitudes_activas : list[str]
        Lista de IDs de SolicitudAdopcion en estados activos
        (pendiente, en_revision, aprobada).
        La capa de infraestructura es responsable de mantener
        esta lista actualizada al hidratar el objeto.
    """

    id: str
    nombre: str
    email: str
    telefono: str
    solicitudes_activas: List[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Reglas de negocio
    # ------------------------------------------------------------------

    def puede_solicitar(self) -> bool:
        """
        Retorna True si el adoptante puede crear una nueva solicitud.

        Regla: un adoptante solo puede tener 1 solicitud activa a la vez.
        Una solicitud activa es aquella cuyo estado es
        'pendiente', 'en_revision' o 'aprobada'.
        """
        return len(self.solicitudes_activas) < 1

    def agregar_solicitud_activa(self, solicitud_id: str) -> None:
        """
        Registra una nueva solicitud activa para este adoptante.

        Llamado por SolicitudAdopcion.crear() luego de validar
        que el adoptante puede solicitar.
        """
        self.solicitudes_activas.append(solicitud_id)

    def __repr__(self) -> str:
        return (
            f"Adoptante(id={self.id!r}, nombre={self.nombre!r}, "
            f"email={self.email!r}, solicitudes_activas={self.solicitudes_activas!r})"
        )
