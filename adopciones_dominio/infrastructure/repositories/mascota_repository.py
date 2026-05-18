from sqlalchemy import text

class MascotaRepository:

    def __init__(self, engine):
        self.engine = engine

    def obtener_por_id(self, codmascota: int):
        query = text("""
            SELECT codmascota, nombre, especie, fechaingreso, codtipomascota
            FROM mascotas
            WHERE codmascota = :id
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {"id": codmascota})
            return result.fetchone()

    def actualizar_estado(self, codmascota: int, estado: str):

        raise NotImplementedError(
            "La tabla mascotas no tiene campo estado en el esquema actual"
        )