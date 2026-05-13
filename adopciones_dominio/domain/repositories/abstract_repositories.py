"""
Interfaces abstractas de repositorios para la capa de dominio.

Define los contratos que debe cumplir la capa de infraestructura
(Persona 5). El dominio nunca implementa estos métodos — solo los
declara como ABC para garantizar el principio de inversión de dependencias.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.mascota import EstadoMascota, Mascota
from domain.entities.solicitud_adopcion import SolicitudAdopcion


class AbstractMascotaRepository(ABC):
    """
    Contrato de repositorio para la entidad Mascota.

    La capa de infraestructura (Persona 5) debe implementar
    esta clase con la tecnología de persistencia real (SQLAlchemy,
    asyncpg, etc. contra PostgreSQL/Supabase).
    """

    @abstractmethod
    def obtener_por_id(self, mascota_id: str) -> Optional[Mascota]:
        """
        Busca y retorna una mascota por su ID.

        Parameters
        ----------
        mascota_id : str
            Identificador único de la mascota.

        Returns
        -------
        Mascota | None
            La mascota encontrada, o None si no existe.
        """
        ...

    @abstractmethod
    def actualizar_estado(self, mascota_id: str, nuevo_estado: EstadoMascota) -> None:
        """
        Actualiza el estado de una mascota en la persistencia.

        Parameters
        ----------
        mascota_id : str
            ID de la mascota a actualizar.
        nuevo_estado : EstadoMascota
            Nuevo estado a asignar.
        """
        ...

    @abstractmethod
    def listar_disponibles(self) -> List[Mascota]:
        """
        Retorna todas las mascotas con estado DISPONIBLE.

        Returns
        -------
        list[Mascota]
            Lista de mascotas disponibles (puede ser vacía).
        """
        ...


class AbstractSolicitudRepository(ABC):
    """
    Contrato de repositorio para la entidad SolicitudAdopcion.

    La capa de infraestructura (Persona 5) debe implementar
    esta clase con la tecnología de persistencia real.
    """

    @abstractmethod
    def guardar(self, solicitud: SolicitudAdopcion) -> SolicitudAdopcion:
        """
        Persiste una nueva solicitud de adopción.

        Parameters
        ----------
        solicitud : SolicitudAdopcion
            Solicitud a guardar.

        Returns
        -------
        SolicitudAdopcion
            La solicitud persistida (con ID confirmado).
        """
        ...

    @abstractmethod
    def obtener_activas_por_adoptante(
        self, adoptante_id: str
    ) -> List[SolicitudAdopcion]:
        """
        Retorna las solicitudes activas de un adoptante.

        Una solicitud activa es aquella en estado:
        PENDIENTE, EN_REVISION o APROBADA.

        Parameters
        ----------
        adoptante_id : str
            ID del adoptante.

        Returns
        -------
        list[SolicitudAdopcion]
            Lista de solicitudes activas (puede ser vacía).
        """
        ...

    @abstractmethod
    def obtener_por_id(self, solicitud_id: str) -> Optional[SolicitudAdopcion]:
        """
        Busca y retorna una solicitud por su ID.

        Parameters
        ----------
        solicitud_id : str
            Identificador único de la solicitud.

        Returns
        -------
        SolicitudAdopcion | None
            La solicitud encontrada, o None si no existe.
        """
        ...
