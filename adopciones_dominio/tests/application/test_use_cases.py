import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from application.use_cases.crear_solicitud_adopcion import CrearSolicitudAdopcion
from application.use_cases.verificar_mascota_disponible import VerificarMascotaDisponible
from domain.entities import Mascota, SolicitudAdopcion


def test_crear_solicitud_falla_si_adoptante_tiene_solicitud_activa() -> None:
    solicitud_repo = AsyncMock()
    solicitud_repo.obtener_activas_por_adoptante.return_value = [
        SolicitudAdopcion(
            cedula="1001",
            codmascota=10,
            fechasolicitud=datetime.now(timezone.utc),
            estado="pendiente",
        )
    ]
    mascota_repo = AsyncMock()

    use_case = CrearSolicitudAdopcion(solicitud_repo, mascota_repo)

    async def _execute() -> None:
        await use_case.execute(cedula="1001", codmascota=11)

    with pytest.raises(HTTPException) as error:
        asyncio.run(_execute())

    assert error.value.status_code == 409
    assert error.value.detail["code"] == "MAX_SOLICITUDES_EXCEDIDO"


def test_crear_solicitud_falla_si_mascota_no_disponible() -> None:
    solicitud_repo = AsyncMock()
    solicitud_repo.obtener_activas_por_adoptante.return_value = []
    mascota_repo = AsyncMock()
    mascota_repo.obtener_por_id.return_value = Mascota(
        codmascota=12,
        nombre="Luna",
        estado="en_proceso",
    )

    use_case = CrearSolicitudAdopcion(solicitud_repo, mascota_repo)

    async def _execute() -> None:
        await use_case.execute(cedula="1001", codmascota=12)

    with pytest.raises(HTTPException) as error:
        asyncio.run(_execute())

    assert error.value.status_code == 422
    assert error.value.detail["code"] == "MASCOTA_NO_DISPONIBLE"


def test_crear_solicitud_exitosa() -> None:
    solicitud_repo = AsyncMock()
    solicitud_repo.obtener_activas_por_adoptante.return_value = []
    solicitud_repo.guardar.return_value = None
    mascota_repo = AsyncMock()
    mascota_repo.obtener_por_id.return_value = Mascota(
        codmascota=12,
        nombre="Luna",
        estado="disponible",
    )

    use_case = CrearSolicitudAdopcion(solicitud_repo, mascota_repo)
    response = asyncio.run(use_case.execute(cedula="1001", codmascota=12))

    assert response.cedula == "1001"
    assert response.codmascota == 12
    assert response.estado == "pendiente"


def test_verificar_mascota_disponible_retorna_false_si_en_proceso() -> None:
    mascota_repo = AsyncMock()
    mascota_repo.obtener_por_id.return_value = Mascota(
        codmascota=25,
        nombre="Toby",
        estado="en_proceso",
    )

    use_case = VerificarMascotaDisponible(mascota_repo)
    response = asyncio.run(use_case.execute(codmascota=25))

    assert response.disponible is False
    assert response.codmascota == 25
