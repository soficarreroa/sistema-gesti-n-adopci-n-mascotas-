"""
Tests unitarios para la entidad Mascota.

Sin base de datos ni frameworks externos — solo Python puro y pytest.
"""
import pytest

from domain.entities.mascota import EstadoMascota, Mascota


def _mascota_disponible(**kwargs) -> Mascota:
    """Fixture helper: crea una mascota en estado DISPONIBLE."""
    defaults = dict(
        id="mascota-001",
        nombre="Luna",
        estado=EstadoMascota.DISPONIBLE,
        especie="perro",
        raza="Labrador",
        edad_meses=18,
        fotos=["https://cdn.ejemplo.com/luna1.jpg"],
    )
    return Mascota(**{**defaults, **kwargs})


class TestEstadoMascota:
    def test_valores_enum(self):
        assert EstadoMascota.DISPONIBLE.value == "disponible"
        assert EstadoMascota.EN_PROCESO.value == "en_proceso"
        assert EstadoMascota.ADOPTADA.value == "adoptada"


class TestMascotaEstaDisponible:
    def test_disponible_cuando_estado_es_disponible(self):
        mascota = _mascota_disponible()
        assert mascota.esta_disponible() is True

    def test_no_disponible_cuando_en_proceso(self):
        mascota = _mascota_disponible(estado=EstadoMascota.EN_PROCESO)
        assert mascota.esta_disponible() is False

    def test_no_disponible_cuando_adoptada(self):
        mascota = _mascota_disponible(estado=EstadoMascota.ADOPTADA)
        assert mascota.esta_disponible() is False


class TestMascotaTransicionesDeEstado:
    def test_marcar_en_proceso(self):
        mascota = _mascota_disponible()
        mascota.marcar_en_proceso()
        assert mascota.estado == EstadoMascota.EN_PROCESO

    def test_marcar_adoptada(self):
        mascota = _mascota_disponible(estado=EstadoMascota.EN_PROCESO)
        mascota.marcar_adoptada()
        assert mascota.estado == EstadoMascota.ADOPTADA

    def test_marcar_disponible_desde_en_proceso(self):
        mascota = _mascota_disponible(estado=EstadoMascota.EN_PROCESO)
        mascota.marcar_disponible()
        assert mascota.estado == EstadoMascota.DISPONIBLE
        assert mascota.esta_disponible() is True

    def test_marcar_disponible_desde_adoptada(self):
        """Cubre el caso de corrección manual de datos."""
        mascota = _mascota_disponible(estado=EstadoMascota.ADOPTADA)
        mascota.marcar_disponible()
        assert mascota.esta_disponible() is True


class TestMascotaRepresentacion:
    def test_repr_contiene_datos_clave(self):
        mascota = _mascota_disponible()
        repr_str = repr(mascota)
        assert "mascota-001" in repr_str
        assert "Luna" in repr_str
        assert "disponible" in repr_str
