"""
Tests unitarios para la entidad Adoptante.

Sin base de datos ni frameworks externos — solo Python puro y pytest.
"""
import pytest

from domain.entities.adoptante import Adoptante


def _adoptante_sin_solicitudes(**kwargs) -> Adoptante:
    defaults = dict(
        id="adoptante-001",
        nombre="Carlos Ramírez",
        email="carlos@ejemplo.com",
        telefono="3001234567",
        solicitudes_activas=[],
    )
    return Adoptante(**{**defaults, **kwargs})


class TestAdoptantePuedeSolicitar:
    def test_puede_solicitar_cuando_no_tiene_solicitudes(self):
        adoptante = _adoptante_sin_solicitudes()
        assert adoptante.puede_solicitar() is True

    def test_no_puede_solicitar_cuando_tiene_una_solicitud_activa(self):
        adoptante = _adoptante_sin_solicitudes(
            solicitudes_activas=["solicitud-abc"]
        )
        assert adoptante.puede_solicitar() is False

    def test_no_puede_solicitar_cuando_tiene_varias_solicitudes(self):
        adoptante = _adoptante_sin_solicitudes(
            solicitudes_activas=["sol-1", "sol-2"]
        )
        assert adoptante.puede_solicitar() is False


class TestAdoptanteAgregarSolicitud:
    def test_agregar_solicitud_activa(self):
        adoptante = _adoptante_sin_solicitudes()
        adoptante.agregar_solicitud_activa("solicitud-xyz")
        assert "solicitud-xyz" in adoptante.solicitudes_activas

    def test_despues_de_agregar_no_puede_solicitar(self):
        adoptante = _adoptante_sin_solicitudes()
        adoptante.agregar_solicitud_activa("solicitud-xyz")
        assert adoptante.puede_solicitar() is False

    def test_agregar_multiples_solicitudes(self):
        adoptante = _adoptante_sin_solicitudes()
        adoptante.agregar_solicitud_activa("sol-1")
        adoptante.agregar_solicitud_activa("sol-2")
        assert len(adoptante.solicitudes_activas) == 2


class TestAdoptanteRepresentacion:
    def test_repr_contiene_datos_clave(self):
        adoptante = _adoptante_sin_solicitudes()
        repr_str = repr(adoptante)
        assert "adoptante-001" in repr_str
        assert "carlos@ejemplo.com" in repr_str
