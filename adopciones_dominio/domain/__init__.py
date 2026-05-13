"""
Capa de dominio — Sistema de Gestión de Adopciones de Mascotas.

Este paquete contiene Python puro:
- Entidades: Mascota, Adoptante, SolicitudAdopcion
- Enums de estado: EstadoMascota, EstadoSolicitud
- Excepciones de dominio
- Interfaces abstractas de repositorios

Sin dependencias de FastAPI, SQLAlchemy, Supabase ni ningún framework.
"""
from domain.entities import (
    Adoptante,
    EstadoMascota,
    EstadoSolicitud,
    Mascota,
    SolicitudAdopcion,
)
from domain.exceptions import (
    AdoptanteNoRegistradoError,
    DomainError,
    MaxSolicitudesExcedidoError,
    MascotaNoDisponibleError,
)
from domain.repositories import AbstractMascotaRepository, AbstractSolicitudRepository

__all__ = [
    # Entidades
    "Mascota",
    "Adoptante",
    "SolicitudAdopcion",
    # Enums
    "EstadoMascota",
    "EstadoSolicitud",
    # Excepciones
    "DomainError",
    "MaxSolicitudesExcedidoError",
    "MascotaNoDisponibleError",
    "AdoptanteNoRegistradoError",
    # Repositorios abstractos
    "AbstractMascotaRepository",
    "AbstractSolicitudRepository",
]
