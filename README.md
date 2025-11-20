## Contrato de la API CRM (Editado)

### 1. Autenticación (`/api/v1/auth/`)

| Método | Endpoint | Body | Respuesta exitosa | Errores |
|--------|----------|------|-------------------|---------|
| `POST` | `register/` | `{ "nombre_completo": string, "username": string, "email": string, "password": string, "password_confirm": string, "tipo": "admin" \| "regular" }` | `201` → `{ "success": true, "data": { "id": int, "username": string, "nombre_completo": string, "email": string, "tipo": string, "activo": bool, "fecha_creacion": ISO8601 }, "message": "Usuario creado exitosamente" }` | `400 VALIDATION_ERROR` (campos inválidos o duplicados), `403` (rol sin permisos) |
| `POST` | `login/` | `{ "username": string, "password": string }` | `200` → `{ "success": true, "data": { "access": token, "refresh": token, "user": {...} }, "message": "Login exitoso" }` | `401 INVALID_CREDENTIALS`, `403` usuario desactivado |
| `POST` | `refresh/` | `{ "refresh": token }` | `200` → `{ "success": true, "data": { "access": token }, "message": "Token refrescado exitosamente" }` | `401` token inválido/expirado |
| `GET` | `usuarios/` | `Headers: Authorization` | `200` → `{ "count": int, "next": url, "previous": url, "success": true, "data": [usuarios], "message": "Listado obtenido exitosamente" }` | `403 PERMISSION_DENIED` |

### 2. Empresas (`/api/v1/empresas/`)

| Método | Endpoint | Body | Respuesta exitosa | Errores |
|--------|----------|------|-------------------|---------|
| `POST` | `` | `{ "nombre": string, "industria": enum?, "num_empleados": int?, "sitio_web": url?, "telefono": string?, "direccion": string?, "notas": string? }` | `201` → `{ "success": true, "data": empresa, "message": "Empresa creada exitosamente" }` | `400 VALIDATION_ERROR`, `409` nombre duplicado |
| `GET` | `` | Query: `search`, `industria`, `ordering`, `page`, `page_size` | `200` paginado estándar | `401/403` |
| `GET` | `{id}/` | — | `200` → detalle + listas de clientes y oportunidades | `404 NOT_FOUND` |
| `PATCH` | `{id}/` | Campos parciales | `200` | `400`, `404` |
| `DELETE` | `{id}/` | — | `200` → `{ "success": true, "message": "Empresa eliminada exitosamente" }` | `409 CONSTRAINT_ERROR` si tiene dependencias |
| `GET` | `export/` | Mismos filtros | `200` CSV | — |

### 3. Clientes (`/api/v1/clientes/`)

| Método | Endpoint | Body | Respuesta exitosa | Errores |
|--------|----------|------|-------------------|---------|
| `POST` | `` | `{ "nombre_completo": string, "empresa_id": int, "cargo": string?, "telefono": string, "email": string, "direccion": string?, "notas": string? }` | `201` | `400`, `404` empresa |
| `GET` | `` | Query: `search`, `empresa_id`, `ordering`, `page` | `200` paginado | — |
| `GET` | `{id}/` | — | `200` | `404` |
| `PATCH` | `{id}/` | Campos parciales | `200` | `400`, `404` |
| `DELETE` | `{id}/` | — | `200` | `409 CONSTRAINT_ERROR` si tiene oportunidades abiertas |
| `GET` | `export/` | Filtros | `200` CSV | — |

### 4. Oportunidades (`/api/v1/oportunidades/`)

| Método | Endpoint | Body | Respuesta exitosa | Errores |
|--------|----------|------|-------------------|---------|
| `POST` | `` | `{ "nombre": string, "cliente_id": int, "empresa_id": int, "valor": decimal, "moneda": "PEN"/"USD"/"EUR", "probabilidad": int 0-100, "fecha_cierre_estimada": date, "etapa": enum, "notas": string? }` | `201` | `400`, `404` cliente/empresa |
| `GET` | `` | Query: `estado`, `etapa`, `cliente_id`, `empresa_id`, `moneda`, `valor_min`, `valor_max`, `fecha_desde`, `fecha_hasta`, `ordering`, `page` | `200` → listado + `total_valor`, `total_valor_ponderado` | — |
| `GET` | `{id}/` | — | `200` | `404` |
| `PATCH` | `{id}/` | Parcial (incluye `estado`, `resultado`) | `200` | `400`, `404` |
| `DELETE` | `{id}/` | — | `200` | `404` |
| `GET` | `pipeline/` | Filtros opcionales | `200` → `{ "success": true, "data": { etapa: { count, valor_total, oportunidades[...] } }, "total_oportunidades": int, "total_valor": float }` | — |
| `PATCH` | `{id}/actualizar-etapa/` | `{ "etapa": enum, "notas": string? }` | `200` → oportunidad actualizada con reglas de estado/resultado | `400`, `404` |
| `GET` | `export/` | Filtros | `200` CSV | — |

### 5. Actividades (`/api/v1/actividades/`)

| Método | Endpoint | Body | Respuesta exitosa | Errores |
|--------|----------|------|-------------------|---------|
| `POST` | `` | `{ "tipo": enum, "asunto": string, "descripcion": string?, "fecha_hora": datetime, "estado": enum?, "cliente_id": int?, "oportunidad_id": int?, "resultado": string? }` | `201` (usuario se infiere de `request.user`) | `400`, `404` |
| `GET` | `` | Query: `tipo`, `estado`, `cliente_id`, `oportunidad_id`, `fecha_desde`, `fecha_hasta`, `ordering`, `page` | `200` paginado | — |
| `GET` | `{id}/` | — | `200` | `404` |
| `PATCH` | `{id}/` | Parcial | `200` | `400`, `404` |
| `DELETE` | `{id}/` | — | `200` | `404` |
| `PATCH` | `{id}/completar/` | `{ "resultado": string }` | `200` → `{ "success": true, "data": actividad_actualizada, "message": "Actividad marcada como completada" }` | `400`, `404` |
| `GET` | `export/` | Filtros | `200` CSV | — |

### 6. Reportes (`/api/v1/reportes/`)

| Método | Endpoint | Body/Query | Respuesta exitosa | Errores |
|--------|----------|------------|-------------------|---------|
| `GET` | `dashboard/` | — | `200` → métricas generales (`totales`, `valores`, `oportunidades_por_etapa`, `actividades_por_tipo`) | — |
| `GET` | `ventas/` | Query: `fecha_inicio` (YYYY-MM-DD), `fecha_fin`, `agrupar_por` (`dia`/`semana`/`mes`), `moneda`? | `200` → `{ periodo, resumen, ventas_por_periodo[] }` | `400 VALIDATION_ERROR` |
| `GET` | `conversion/` | — | `200` → `{ total_oportunidades_creadas, total_cerradas_ganadas, total_cerradas_perdidas, tasa_conversion_general, conversion_por_etapa, tiempo_promedio_cierre_dias }` | — |
| `GET` | `clientes-por-empresa/` | — | `200` → lista con `empresa_id`, `empresa_nombre`, `num_clientes`, `num_oportunidades`, `valor_total_oportunidades` | — |

### 7. Errores comunes (formato estándar)

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Los datos proporcionados no son válidos",
    "details": { "campo": ["motivo"] }
  }
}
```

| Código | Situación |
|--------|-----------|
| `VALIDATION_ERROR (400)` | Datos inválidos o faltantes |
| `INVALID_CREDENTIALS (401)` | Login fallido |
| `UNAUTHORIZED (401)` | Falta token JWT o caducó |
| `PERMISSION_DENIED (403)` | Usuario sin permisos |
| `NOT_FOUND (404)` | Recurso inexistente |
| `CONSTRAINT_ERROR (409)` | Eliminación bloqueada por dependencias |
| `SERVER_ERROR (500)` | Error inesperado |


