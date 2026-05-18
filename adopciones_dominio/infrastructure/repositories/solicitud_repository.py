from sqlalchemy import text


class SolicitudRepository:

    def __init__(self, engine):
        self.engine = engine

    # CREAR SOLICITUD (TRANSACCIONAL)
    def crear_solicitud(self, cedula: str, codmascota: int):

        query = text("""
            INSERT INTO solicitudes (
                cedula,
                codmascota,
                fechasolicitud,
                estado
            )
            VALUES (
                :cedula,
                :codmascota,
                NOW(),
                'pendiente'
            )
        """)

        try:
            with self.engine.begin() as conn:
                conn.execute(query, {
                    "cedula": cedula,
                    "codmascota": codmascota
                })

        except Exception as e:
            raise Exception(f"Error creando solicitud: {e}")

    # OBTENER SOLICITUDES ACTIVAS POR ADOPTANTE
    def obtener_activas_por_adoptante(self, cedula: str):

        query = text("""
            SELECT cedula,codmascota,fechasolicitud,
                estado
            FROM solicitudes
            WHERE cedula = :cedula
            AND estado IN ('pendiente', 'en_revision', 'aprobada')
        """)

        try:
            with self.engine.connect() as conn:
                result = conn.execute(query, {"cedula": cedula})
                return result.fetchall()

        except Exception as e:
            raise Exception(f"Error consultando solicitudes: {e}")