# Contrato API — Capa de Aplicación (Persona 3)

**Base URL:** `http://localhost:8000/api/v1`

## Headers esperados desde API Gateway (Sofia)

- `X-User-Cedula: <string>` (mínimo requerido para identidad del adoptante autenticado)

## Endpoint 1: Verificar disponibilidad de mascota

**Método y ruta:** `GET /mascotas/{codmascota}/disponible`

**Body:** no aplica.

### 200 OK

```json
{
  "disponible": true,
  "codmascota": 12,
  "nombre": "Luna",
  "razon": null
}
```

```json
{
  "disponible": false,
  "codmascota": 12,
  "nombre": "Luna",
  "razon": "La mascota tiene una solicitud activa."
}
```

### 404 Not Found

```json
{
  "detail": "No existe la mascota con código 9999.",
  "code": "MASCOTA_NO_ENCONTRADA"
}
```

## Endpoint 2: Crear solicitud de adopción

**Método y ruta:** `POST /solicitudes`

**Body (JSON):**

```json
{
  "cedula": "1002003001",
  "codmascota": 12
}
```

### 201 Created

```json
{
  "cedula": "1002003001",
  "codmascota": 12,
  "fechasolicitud": "2026-05-18T20:00:00.123456Z",
  "estado": "pendiente"
}
```

### 400 Bad Request

```json
{
  "detail": "1 validation error for Request...",
  "code": "BAD_REQUEST"
}
```

### 404 Not Found

```json
{
  "detail": "No existe la mascota con código 9999.",
  "code": "MASCOTA_NO_ENCONTRADA"
}
```

### 409 Conflict

```json
{
  "detail": "El adoptante 1002003001 ya tiene una solicitud activa.",
  "code": "MAX_SOLICITUDES_EXCEDIDO"
}
```

### 422 Unprocessable Entity

```json
{
  "detail": "La mascota 12 no está disponible. Estado actual: en_proceso.",
  "code": "MASCOTA_NO_DISPONIBLE"
}
```

## Semántica de códigos de error

- `BAD_REQUEST`: payload inválido o incompleto.
- `MASCOTA_NO_ENCONTRADA`: la mascota solicitada no existe.
- `MAX_SOLICITUDES_EXCEDIDO`: el adoptante ya tiene una solicitud activa.
- `MASCOTA_NO_DISPONIBLE`: la mascota no puede iniciar una nueva solicitud.
