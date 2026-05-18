class MascotaMapper:

    @staticmethod
    def to_dict(row):

        if row is None:
            return None

        row = row._mapping

        return {
            "codmascota": row["codmascota"],
            "nombre": row["nombre"],
            "especie": row["especie"],
            "fechaingreso": row["fechaingreso"],
            "codtipomascota": row["codtipomascota"]
        }


class SolicitudMapper:

    @staticmethod
    def to_dict(row):

        if row is None:
            return None

        row = row._mapping

        return {
            "cedula": row["cedula"],
            "codmascota": row["codmascota"],
            "fechasolicitud": row["fechasolicitud"],
            "estado": row["estado"]
        }