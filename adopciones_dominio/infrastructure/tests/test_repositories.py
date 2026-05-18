from sqlalchemy import create_engine

from adopciones_dominio.infrastructure.database.config import DATABASE_URL

from adopciones_dominio.infrastructure.repositories.mascota_repository import MascotaRepository


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

repo = MascotaRepository(engine)


def test_obtener_mascota():

    try:
        mascota = repo.obtener_por_id(1)

        print("Mascota encontrada:")
        print(mascota)

    except Exception as e:
        print("Error obteniendo mascota:")
        print(e)


def test_update_estado():

    try:
        repo.actualizar_estado(1, "adoptado")

        print("Estado actualizado correctamente")

    except Exception as e:
        print("Error actualizando estado:")
        print(e)


if __name__ == "__main__":
    test_obtener_mascota()
    test_update_estado()