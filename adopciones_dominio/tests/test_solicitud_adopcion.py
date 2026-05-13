"""
Tests unitarios para SolicitudAdopcion y las reglas de negocio centrales.

Sin base de datos ni frameworks externos — solo Python puro y pytest.
"""
import pytest

from domain.entities.adoptante import Adoptante
from domain.entities.mascota import EstadoMascota, Mascota
from domain.entities.solicitud_adopcion import EstadoSolicitud, SolicitudAdopcion
from domain.exceptions import MaxSolicitudesExcedidoError, MascotaNoDisponibleError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mascota_disponible(mascota_id: str = "mascota-001") -> Mascota:
    return Mascota(
        id=mascota_id,
        nombre="Luna",
        estado=EstadoMascota.DISPONIBLE,
        especie="perro",
        raza="Labrador",
        edad_meses=18,
    )


def _adoptante_libre(adoptante_id: str = "adoptante-001") -> Adoptante:
    return Adoptante(
        id=adoptante_id,
        nombre="María García",
        email="maria@ejemplo.com",
        telefono="3109876543",
        solicitudes_activas=[],
    )


# ---------------------------------------------------------------------------
# Tests del flujo feliz (Happy Path)
# ---------------------------------------------------------------------------

class TestSolicitudAdopcionCrearHappyPath:
    def test_crear_retorna_solicitud_pendiente(self):
        adoptante = _adoptante_libre()
        mascota = _mascota_disponible()

        solicitud = SolicitudAdopcion.crear(adoptante, mascota)

        assert solicitud.estado == EstadoSolicitud.PENDIENTE
        assert solicitud.adoptante_id == adoptante.id
        assert solicitud.mascota_id == mascota.id

    def test_crear_genera_id_unico(self):
        adoptante1 = _adoptante_libre("a-001")
        mascota1 = _mascota_disponible("m-001")
        adoptante2 = _adoptante_libre("a-002")
        mascota2 = _mascota_disponible("m-002")

        solicitud1 = SolicitudAdopcion.crear(adoptante1, mascota1)
        solicitud2 = SolicitudAdopcion.crear(adoptante2, mascota2)

        assert solicitud1.id != solicitud2.id

    def test_crear_marca_mascota_en_proceso(self):
        adoptante = _adoptante_libre()
        mascota = _mascota_disponible()

        SolicitudAdopcion.crear(adoptante, mascota)

        assert mascota.estado == EstadoMascota.EN_PROCESO
        assert mascota.esta_disponible() is False

    def test_crear_registra_solicitud_en_adoptante(self):
        adoptante = _adoptante_libre()
        mascota = _mascota_disponible()

        solicitud = SolicitudAdopcion.crear(adoptante, mascota)

        assert solicitud.id in adoptante.solicitudes_activas
        assert adoptante.puede_solicitar() is False

    def test_crear_asigna_fecha_creacion(self):
        from datetime import datetime, timezone

        adoptante = _adoptante_libre()
        mascota = _mascota_disponible()
        antes = datetime.now(timezone.utc)

        solicitud = SolicitudAdopcion.crear(adoptante, mascota)

        despues = datetime.now(timezone.utc)
        assert antes <= solicitud.fecha_creacion <= despues


# ---------------------------------------------------------------------------
# Tests de reglas de negocio — deben lanzar excepciones
# ---------------------------------------------------------------------------

class TestReglaMaxSolicitudesExcedido:
    def test_adoptante_con_solicitud_activa_no_puede_crear_otra(self):
        adoptante = _adoptante_libre()
        adoptante.solicitudes_activas = ["solicitud-preexistente"]
        mascota = _mascota_disponible()

        with pytest.raises(MaxSolicitudesExcedidoError) as exc_info:
            SolicitudAdopcion.crear(adoptante, mascota)

        assert adoptante.id in str(exc_info.value)

    def test_mascota_permanece_disponible_si_adoptante_bloqueado(self):
        """La mascota no debe cambiar de estado si la excepción se lanza."""
        adoptante = _adoptante_libre()
        adoptante.solicitudes_activas = ["solicitud-preexistente"]
        mascota = _mascota_disponible()

        with pytest.raises(MaxSolicitudesExcedidoError):
            SolicitudAdopcion.crear(adoptante, mascota)

        # La mascota no debió verse afectada.
        assert mascota.esta_disponible() is True


class TestReglaMascotaNoDisponible:
    @pytest.mark.parametrize("estado", [
        EstadoMascota.EN_PROCESO,
        EstadoMascota.ADOPTADA,
    ])
    def test_mascota_no_disponible_lanza_error(self, estado: EstadoMascota):
        adoptante = _adoptante_libre()
        mascota = _mascota_disponible()
        mascota.estado = estado

        with pytest.raises(MascotaNoDisponibleError) as exc_info:
            SolicitudAdopcion.crear(adoptante, mascota)

        assert mascota.id in str(exc_info.value)
        assert estado.value in str(exc_info.value)

    def test_adoptante_no_cambia_si_mascota_bloqueada(self):
        """El adoptante no debe registrar solicitud si la mascota no está disponible."""
        adoptante = _adoptante_libre()
        mascota = _mascota_disponible()
        mascota.estado = EstadoMascota.EN_PROCESO

        with pytest.raises(MascotaNoDisponibleError):
            SolicitudAdopcion.crear(adoptante, mascota)

        assert adoptante.puede_solicitar() is True
        assert len(adoptante.solicitudes_activas) == 0


class TestReglaOrdenDeValidacion:
    def test_adoptante_bloqueado_tiene_prioridad_sobre_mascota_no_disponible(self):
        """
        Cuando ambas reglas fallan, MaxSolicitudesExcedidoError
        debe lanzarse primero (se valida antes).
        """
        adoptante = _adoptante_libre()
        adoptante.solicitudes_activas = ["sol-preexistente"]
        mascota = _mascota_disponible()
        mascota.estado = EstadoMascota.EN_PROCESO

        with pytest.raises(MaxSolicitudesExcedidoError):
            SolicitudAdopcion.crear(adoptante, mascota)


# ---------------------------------------------------------------------------
# Tests de métodos de consulta
# ---------------------------------------------------------------------------

class TestSolicitudEstaActiva:
    @pytest.mark.parametrize("estado,esperado", [
        (EstadoSolicitud.PENDIENTE, True),
        (EstadoSolicitud.EN_REVISION, True),
        (EstadoSolicitud.APROBADA, True),
        (EstadoSolicitud.RECHAZADA, False),
        (EstadoSolicitud.CANCELADA, False),
    ])
    def test_esta_activa_segun_estado(self, estado: EstadoSolicitud, esperado: bool):
        from datetime import datetime, timezone

        solicitud = SolicitudAdopcion(
            id="sol-test",
            adoptante_id="a-001",
            mascota_id="m-001",
            estado=estado,
            fecha_creacion=datetime.now(timezone.utc),
        )
        assert solicitud.esta_activa() is esperado


# ---------------------------------------------------------------------------
# Tests de excepciones de dominio
# ---------------------------------------------------------------------------

class TestExcepcionesMaxSolicitudes:
    def test_excepcion_contiene_adoptante_id(self):
        exc = MaxSolicitudesExcedidoError(adoptante_id="adoptante-999")
        assert "adoptante-999" in str(exc)
        assert exc.adoptante_id == "adoptante-999"

    def test_es_subclase_de_domain_error(self):
        from domain.exceptions import DomainError
        exc = MaxSolicitudesExcedidoError(adoptante_id="x")
        assert isinstance(exc, DomainError)


class TestExcepcionesMascotaNoDisponible:
    def test_excepcion_contiene_id_y_estado(self):
        exc = MascotaNoDisponibleError(mascota_id="m-777", estado_actual="en_proceso")
        assert "m-777" in str(exc)
        assert "en_proceso" in str(exc)
        assert exc.mascota_id == "m-777"
        assert exc.estado_actual == "en_proceso"
