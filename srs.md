# Especificación de Requisitos de Software (SRS)
## API REST de CRM - Proyecto Académico

**Versión:** 1.0  
**Fecha:** 16 de Noviembre de 2025  
**Proyecto:** API REST para Sistema CRM Educativo  
**Tipo:** Proyecto Académico de Instituto

---

## 1. Introducción

### 1.1 Propósito

Este documento describe los requisitos para desarrollar una API REST (Interfaz de Programación de Aplicaciones) de un Sistema de Gestión de Relaciones con Clientes (CRM) como proyecto académico. La API será el backend completo del sistema, proporcionando todos los servicios necesarios para que aplicaciones cliente (web, móvil, o desktop) puedan interactuar con los datos del CRM.

El proyecto permitirá a los estudiantes aprender desarrollo de APIs modernas, arquitectura de software, bases de datos relacionales, y tecnologías de containerización.

### 1.2 Alcance del Proyecto

La API REST del CRM proporcionará endpoints (puntos de acceso) para:
- Autenticación y gestión de usuarios mediante tokens JWT
- Operaciones CRUD sobre clientes, empresas, oportunidades y actividades
- Consultas y filtrado de datos
- Generación de reportes y estadísticas
- Validación robusta de datos de entrada
- Documentación automática de la API

**Stack Tecnológico Obligatorio:**
- **Django 4.x:** Framework web de Python para el backend
- **Django REST Framework (DRF):** Para construir la API REST
- **Pydantic:** Para validación de esquemas de datos
- **MySQL 8.x:** Base de datos relacional
- **Docker & Docker Compose:** Para containerización y orquestación

**Lo que NO incluye este proyecto:**
- Frontend/Interfaz de usuario (la API puede ser consumida por cualquier cliente)
- Integraciones con servicios externos
- Procesamiento en tiempo real o WebSockets
- Funcionalidades de mensajería o notificaciones push
- Sistema de permisos granular complejo

### 1.3 Definiciones y Abreviaturas

**API:** Interfaz de Programación de Aplicaciones (Application Programming Interface)

**REST:** Transferencia de Estado Representacional (Representational State Transfer) - Estilo arquitectónico para APIs

**Endpoint:** URL específica en la API que responde a peticiones HTTP

**CRUD:** Operaciones básicas - Crear (POST), Leer (GET), Actualizar (PUT/PATCH), Eliminar (DELETE)

**JWT:** JSON Web Token - Estándar para tokens de autenticación

**JSON:** JavaScript Object Notation - Formato de intercambio de datos

**HTTP:** Protocolo de Transferencia de Hipertexto

**Métodos HTTP:** GET (obtener), POST (crear), PUT (actualizar completo), PATCH (actualizar parcial), DELETE (eliminar)

**Código de Estado HTTP:** Número que indica el resultado de una petición (200 OK, 404 Not Found, etc.)

**Docker:** Plataforma de containerización que empaqueta aplicaciones con sus dependencias

**Container:** Paquete ejecutable ligero que incluye todo lo necesario para ejecutar una aplicación

**Django ORM:** Object-Relational Mapping - Sistema de Django para interactuar con bases de datos usando Python

**Pydantic:** Librería de Python para validación de datos usando type hints

**Serializer:** Componente que convierte datos entre formatos (Python ↔ JSON)

### 1.4 Audiencia del Documento

Este documento está dirigido a:
- Estudiantes desarrolladores del proyecto
- Profesores supervisores
- Evaluadores del proyecto
- Futuros desarrolladores de clientes que consumirán la API

---

## 2. Descripción General del Sistema

### 2.1 Arquitectura del Sistema

El sistema seguirá una arquitectura de tres capas containerizada:

```
┌─────────────────────────────────────┐
│   Cliente (Frontend - No incluido)  │
│  (Puede ser Web, Mobile, Desktop)   │
└──────────────┬──────────────────────┘
               │ HTTP/HTTPS
               │ JSON
               ▼
┌─────────────────────────────────────┐
│      Container: Django API          │
│  ┌───────────────────────────────┐  │
│  │    Django REST Framework      │  │
│  │    + Pydantic Validation      │  │
│  └───────────────────────────────┘  │
│                                     │
│  Endpoints REST                     │
│  Autenticación JWT                  │
│  Serialización JSON                 │
│  Lógica de Negocio                  │
└──────────────┬──────────────────────┘
               │ ORM
               │ SQL
               ▼
┌─────────────────────────────────────┐
│      Container: MySQL Database      │
│                                     │
│  Tablas:                            │
│  - usuarios                         │
│  - empresas                         │
│  - clientes                         │
│  - oportunidades                    │
│  - actividades                      │
└─────────────────────────────────────┘
```

### 2.2 Componentes Principales

**Container Django API:**
- Framework: Django 4.2+ con Django REST Framework 3.14+
- Validación: Pydantic 2.x integrado con DRF
- Autenticación: JWT usando djangorestframework-simplejwt
- Documentación: drf-spectacular para OpenAPI/Swagger
- Puerto expuesto: 8000

**Container MySQL:**
- MySQL 8.0
- Puerto expuesto: 3306
- Volumen persistente para datos

**Docker Compose:**
- Orquestación de ambos containers
- Red privada entre containers
- Variables de entorno para configuración

### 2.3 Flujo de Trabajo de la API

1. **Cliente hace petición HTTP** → Ejemplo: `POST /api/clientes/`
2. **API recibe petición** → Django Router identifica el endpoint
3. **Autenticación** → Valida token JWT en header
4. **Validación** → Pydantic valida estructura y tipos de datos
5. **Procesamiento** → View ejecuta lógica de negocio
6. **Base de Datos** → Django ORM interactúa con MySQL
7. **Serialización** → Convierte datos Python a JSON
8. **Respuesta HTTP** → Devuelve JSON con código de estado apropiado

### 2.4 Formato de Respuestas

Todas las respuestas de la API seguirán un formato JSON consistente:

**Respuesta Exitosa:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Operación realizada exitosamente"
}
```

**Respuesta con Lista:**
```json
{
  "success": true,
  "data": [ ... ],
  "count": 25,
  "message": "Listado obtenido exitosamente"
}
```

**Respuesta de Error:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Los datos proporcionados no son válidos",
    "details": {
      "email": ["El formato del email no es válido"]
    }
  }
}
```

---

## 3. Requisitos Funcionales - Endpoints de la API

### 3.1 Módulo de Autenticación

**RF-001: Registro de Usuario**

**Endpoint:** `POST /api/auth/register/`

**Descripción:** Permite al administrador crear nuevas cuentas de usuario.

**Request Body:**
```json
{
  "nombre_completo": "Juan Pérez",
  "username": "jperez",
  "email": "juan.perez@example.com",
  "password": "contraseña123",
  "password_confirm": "contraseña123",
  "tipo": "regular"
}
```

**Validaciones Pydantic:**
- `nombre_completo`: string, obligatorio, min 3 caracteres, max 100
- `username`: string, obligatorio, único, min 3 caracteres, max 30, alfanumérico
- `email`: string, obligatorio, formato email válido, único
- `password`: string, obligatorio, min 6 caracteres
- `password_confirm`: debe coincidir con password
- `tipo`: enum ["admin", "regular"], obligatorio

**Response 201 Created:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "nombre_completo": "Juan Pérez",
    "username": "jperez",
    "email": "juan.perez@example.com",
    "tipo": "regular",
    "fecha_creacion": "2025-11-16T10:30:00Z"
  },
  "message": "Usuario creado exitosamente"
}
```

**Response 400 Bad Request:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Datos inválidos",
    "details": {
      "username": ["Este nombre de usuario ya existe"],
      "password": ["La contraseña debe tener al menos 6 caracteres"]
    }
  }
}
```

---

**RF-002: Login / Obtener Token**

**Endpoint:** `POST /api/auth/login/`

**Descripción:** Autentica un usuario y devuelve tokens JWT.

**Request Body:**
```json
{
  "username": "jperez",
  "password": "contraseña123"
}
```

**Response 200 OK:**
```json
{
  "success": true,
  "data": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 1,
      "username": "jperez",
      "nombre_completo": "Juan Pérez",
      "tipo": "regular"
    }
  },
  "message": "Login exitoso"
}
```

**Response 401 Unauthorized:**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Usuario o contraseña incorrectos"
  }
}
```

---

**RF-003: Refrescar Token**

**Endpoint:** `POST /api/auth/refresh/`

**Descripción:** Obtiene un nuevo access token usando el refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response 200 OK:**
```json
{
  "success": true,
  "data": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "Token refrescado exitosamente"
}
```

---

**RF-004: Listar Usuarios (Solo Admin)**

**Endpoint:** `GET /api/auth/usuarios/`

**Headers:** `Authorization: Bearer {access_token}`

**Query Parameters Opcionales:**
- `tipo`: Filtrar por tipo (admin/regular)
- `activo`: Filtrar por estado (true/false)
- `search`: Buscar por nombre o username

**Response 200 OK:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "username": "jperez",
      "nombre_completo": "Juan Pérez",
      "email": "juan.perez@example.com",
      "tipo": "regular",
      "activo": true,
      "fecha_creacion": "2025-11-16T10:30:00Z"
    },
    {
      "id": 2,
      "username": "admin",
      "nombre_completo": "Administrador",
      "email": "admin@example.com",
      "tipo": "admin",
      "activo": true,
      "fecha_creacion": "2025-11-15T08:00:00Z"
    }
  ],
  "count": 2,
  "message": "Usuarios obtenidos exitosamente"
}
```

**Response 403 Forbidden:**
```json
{
  "success": false,
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "No tienes permisos para acceder a este recurso"
  }
}
```

---

### 3.2 Módulo de Empresas

**RF-005: Crear Empresa**

**Endpoint:** `POST /api/empresas/`

**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "nombre": "Tech Solutions SAC",
  "industria": "tecnologia",
  "num_empleados": 50,
  "sitio_web": "https://techsolutions.com",
  "telefono": "+51 987654321",
  "direccion": "Av. Tecnología 123, Lima",
  "notas": "Cliente potencial importante"
}
```

**Validaciones Pydantic:**
- `nombre`: string, obligatorio, único, min 2, max 200
- `industria`: enum opcional ["tecnologia", "servicios", "manufactura", "comercio", "salud", "educacion", "otros"]
- `num_empleados`: integer opcional, min 1
- `sitio_web`: string opcional, formato URL válido
- `telefono`: string opcional, max 20
- `direccion`: string opcional, max 300
- `notas`: string opcional, max 1000

**Response 201 Created:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "nombre": "Tech Solutions SAC",
    "industria": "tecnologia",
    "num_empleados": 50,
    "sitio_web": "https://techsolutions.com",
    "telefono": "+51 987654321",
    "direccion": "Av. Tecnología 123, Lima",
    "notas": "Cliente potencial importante",
    "fecha_creacion": "2025-11-16T11:00:00Z"
  },
  "message": "Empresa creada exitosamente"
}
```

---

**RF-006: Listar Empresas**

**Endpoint:** `GET /api/empresas/`

**Headers:** `Authorization: Bearer {access_token}`

**Query Parameters Opcionales:**
- `search`: Buscar por nombre
- `industria`: Filtrar por industria
- `ordering`: Ordenar por campo (ej: `nombre`, `-fecha_creacion`)
- `page`: Número de página (paginación)
- `page_size`: Tamaño de página (default: 20)

**Response 200 OK:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Tech Solutions SAC",
      "industria": "tecnologia",
      "num_empleados": 50,
      "num_clientes": 5,
      "num_oportunidades": 3,
      "fecha_creacion": "2025-11-16T11:00:00Z"
    }
  ],
  "count": 1,
  "next": null,
  "previous": null,
  "message": "Empresas obtenidas exitosamente"
}
```

---

**RF-007: Obtener Detalle de Empresa**

**Endpoint:** `GET /api/empresas/{id}/`

**Headers:** `Authorization: Bearer {access_token}`

**Response 200 OK:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "nombre": "Tech Solutions SAC",
    "industria": "tecnologia",
    "num_empleados": 50,
    "sitio_web": "https://techsolutions.com",
    "telefono": "+51 987654321",
    "direccion": "Av. Tecnología 123, Lima",
    "notas": "Cliente potencial importante",
    "fecha_creacion": "2025-11-16T11:00:00Z",
    "clientes": [
      {
        "id": 1,
        "nombre_completo": "María García",
        "cargo": "CEO",
        "email": "maria@techsolutions.com"
      }
    ],
    "oportunidades": [
      {
        "id": 1,
        "nombre": "Proyecto ERP",
        "valor": 50000.00,
        "etapa": "propuesta"
      }
    ]
  },
  "message": "Empresa obtenida exitosamente"
}
```

**Response 404 Not Found:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Empresa no encontrada"
  }
}
```

---

**RF-008: Actualizar Empresa**

**Endpoint:** `PUT /api/empresas/{id}/` o `PATCH /api/empresas/{id}/`

**Headers:** `Authorization: Bearer {access_token}`

**Nota:** PUT requiere todos los campos, PATCH permite actualización parcial.

**Request Body (PATCH ejemplo):**
```json
{
  "num_empleados": 60,
  "notas": "Actualizaron su plantilla"
}
```

**Response 200 OK:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "nombre": "Tech Solutions SAC",
    "num_empleados": 60,
    "notas": "Actualizaron su plantilla",
    ...
  },
  "message": "Empresa actualizada exitosamente"
}
```

---

**RF-009: Eliminar Empresa**

**Endpoint:** `DELETE /api/empresas/{id}/`

**Headers:** `Authorization: Bearer {access_token}`

**Response 200 OK:**
```json
{
  "success": true,
  "message": "Empresa eliminada exitosamente"
}
```

**Response 409 Conflict:**
```json
{
  "success": false,
  "error": {
    "code": "CONSTRAINT_ERROR",
    "message": "No se puede eliminar la empresa porque tiene clientes u oportunidades asociadas"
  }
}
```

---

### 3.3 Módulo de Clientes

**RF-010: Crear Cliente**

**Endpoint:** `POST /api/clientes/`

**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "nombre_completo": "María García López",
  "empresa_id": 1,
  "cargo": "CEO",
  "telefono": "+51 999888777",
  "email": "maria.garcia@techsolutions.com",
  "direccion": "Av. Principal 456, Lima",
  "notas": "Muy interesada en nuestros servicios"
}
```

**Validaciones Pydantic:**
- `nombre_completo`: string, obligatorio, min 3, max 150
- `empresa_id`: integer, obligatorio, debe existir en tabla empresas
- `cargo`: string opcional, max 100
- `telefono`: string, obligatorio, max 20
- `email`: string, obligatorio, formato email válido
- `direccion`: string opcional, max 300
- `notas`: string opcional, max 1000

**Response 201 Created:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "nombre_completo": "María García López",
    "empresa": {
      "id": 1,
      "nombre": "Tech Solutions SAC"
    },
    "cargo": "CEO",
    "telefono": "+51 999888777",
    "email": "maria.garcia@techsolutions.com",
    "direccion": "Av. Principal 456, Lima",
    "notas": "Muy interesada en nuestros servicios",
    "fecha_creacion": "2025-11-16T11:30:00Z"
  },
  "message": "Cliente creado exitosamente"
}
```

---

**RF-011: Listar Clientes**

**Endpoint:** `GET /api/clientes/`

**Headers:** `Authorization: Bearer {access_token}`

**Query Parameters:**
- `search`: Buscar por nombre o email
- `empresa_id`: Filtrar por empresa
- `ordering`: Ordenar (ej: `nombre_completo`, `-fecha_creacion`)
- `page`, `page_size`: Paginación

**Response 200 OK:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre_completo": "María García López",
      "empresa": {
        "id": 1,
        "nombre": "Tech Solutions SAC"
      },
      "cargo": "CEO",
      "telefono": "+51 999888777",
      "email": "maria.garcia@techsolutions.com",
      "num_oportunidades": 2,
      "num_actividades": 5
    }
  ],
  "count": 1,
  "message": "Clientes obtenidos exitosamente"
}
```

---

**RF-012: Obtener, Actualizar y Eliminar Cliente**

Endpoints similares a empresas:
- `GET /api/clientes/{id}/` - Obtener detalle
- `PUT/PATCH /api/clientes/{id}/` - Actualizar
- `DELETE /api/clientes/{id}/` - Eliminar

---

### 3.4 Módulo de Oportunidades

**RF-013: Crear Oportunidad**

**Endpoint:** `POST /api/oportunidades/`

**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "nombre": "Implementación Sistema ERP",
  "cliente_id": 1,
  "empresa_id": 1,
  "valor": 50000.00,
  "moneda": "PEN",
  "probabilidad": 70,
  "fecha_cierre_estimada": "2025-12-31",
  "etapa": "propuesta",
  "notas": "Propuesta enviada el 15/11/2025"
}
```

**Validaciones Pydantic:**
- `nombre`: string, obligatorio, min 5, max 200
- `cliente_id`: integer, obligatorio, debe existir
- `empresa_id`: integer, obligatorio, debe existir
- `valor`: decimal, obligatorio, min 0.01, max 2 decimales
- `moneda`: enum, obligatorio ["PEN", "USD", "EUR"]
- `probabilidad`: integer, obligatorio, min 0, max 100
- `fecha_cierre_estimada`: date, obligatorio, debe ser fecha futura
- `etapa`: enum, obligatorio ["prospeccion", "calificacion", "propuesta", "negociacion", "cerrado_ganado", "cerrado_perdido"]
- `notas`: string opcional, max 1000

**Response 201 Created:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "nombre": "Implementación Sistema ERP",
    "cliente": {
      "id": 1,
      "nombre_completo": "María García López"
    },
    "empresa": {
      "id": 1,
      "nombre": "Tech Solutions SAC"
    },
    "valor": 50000.00,
    "moneda": "PEN",
    "probabilidad": 70,
    "valor_ponderado": 35000.00,
    "fecha_cierre_estimada": "2025-12-31",
    "etapa": "propuesta",
    "estado": "abierta",
    "resultado": null,
    "notas": "Propuesta enviada el 15/11/2025",
    "fecha_creacion": "2025-11-16T12:00:00Z",
    "fecha_cierre_real": null
  },
  "message": "Oportunidad creada exitosamente"
}
```

---

**RF-014: Listar Oportunidades con Filtros**

**Endpoint:** `GET /api/oportunidades/`

**Headers:** `Authorization: Bearer {access_token}`

**Query Parameters:**
- `estado`: Filtrar por estado ("abierta" / "cerrada")
- `etapa`: Filtrar por etapa
- `cliente_id`: Filtrar por cliente
- `empresa_id`: Filtrar por empresa
- `moneda`: Filtrar por moneda
- `valor_min`, `valor_max`: Rango de valores
- `fecha_desde`, `fecha_hasta`: Rango de fechas
- `ordering`: Ordenar
- `page`, `page_size`: Paginación

**Response 200 OK:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Implementación Sistema ERP",
      "cliente": {
        "id": 1,
        "nombre_completo": "María García López"
      },
      "empresa": {
        "id": 1,
        "nombre": "Tech Solutions SAC"
      },
      "valor": 50000.00,
      "moneda": "PEN",
      "probabilidad": 70,
      "valor_ponderado": 35000.00,
      "etapa": "propuesta",
      "estado": "abierta",
      "fecha_cierre_estimada": "2025-12-31"
    }
  ],
  "count": 1,
  "total_valor": 50000.00,
  "total_valor_ponderado": 35000.00,
  "message": "Oportunidades obtenidas exitosamente"
}
```

---

**RF-015: Pipeline de Oportunidades**

**Endpoint:** `GET /api/oportunidades/pipeline/`

**Headers:** `Authorization: Bearer {access_token}`

**Descripción:** Devuelve oportunidades agrupadas por etapa.

**Response 200 OK:**
```json
{
  "success": true,
  "data": {
    "prospeccion": {
      "count": 3,
      "valor_total": 120000.00,
      "oportunidades": [ ... ]
    },
    "calificacion": {
      "count": 2,
      "valor_total": 80000.00,
      "oportunidades": [ ... ]
    },
    "propuesta": {
      "count": 1,
      "valor_total": 50000.00,
      "oportunidades": [ ... ]
    },
    "negociacion": {
      "count": 1,
      "valor_total": 75000.00,
      "oportunidades": [ ... ]
    }
  },
  "total_oportunidades": 7,
  "total_valor": 325000.00,
  "message": "Pipeline obtenido exitosamente"
}
```

---

**RF-016: Actualizar Etapa de Oportunidad**

**Endpoint:** `PATCH /api/oportunidades/{id}/actualizar-etapa/`

**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "etapa": "negociacion",
  "notas": "Cliente mostró interés, pasamos a negociación"
}
```

**Response 200 OK:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "etapa": "negociacion",
    "estado": "abierta",
    ...
  },
  "message": "Etapa actualizada exitosamente"
}
```

**Nota:** Si la etapa es "cerrado_ganado" o "cerrado_perdido", automáticamente:
- Cambiar `estado` a "cerrada"
- Establecer `resultado` a "ganada" o "perdida"
- Registrar `fecha_cierre_real` con timestamp actual

---

**RF-017: Obtener, Actualizar Completo y Eliminar Oportunidad**

Endpoints similares:
- `GET /api/oportunidades/{id}/` - Detalle completo
- `PUT/PATCH /api/oportunidades/{id}/` - Actualizar
- `DELETE /api/oportunidades/{id}/` - Eliminar

---

### 3.5 Módulo de Actividades

**RF-018: Crear Actividad**

**Endpoint:** `POST /api/actividades/`

**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "tipo": "reunion",
  "asunto": "Presentación de propuesta comercial",
  "descripcion": "Reunión para presentar solución ERP propuesta",
  "fecha_hora": "2025-11-20T15:00:00",
  "estado": "pendiente",
  "cliente_id": 1,
  "oportunidad_id": 1
}
```

**Validaciones Pydantic:**
- `tipo`: enum, obligatorio ["llamada", "reunion", "email", "tarea"]
- `asunto`: string, obligatorio, min 5, max 200
- `descripcion`: string opcional, max 1000
- `fecha_hora`: datetime, obligatorio
- `estado`: enum, obligatorio ["pendiente", "completada", "cancelada"]
- `cliente_id`: integer opcional, debe existir si se proporciona
- `oportunidad_id`: integer opcional, debe existir si se proporciona
- `resultado`: string opcional, max 500

**Response 201 Created:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "tipo": "reunion",
    "asunto": "Presentación de propuesta comercial",
    "descripcion": "Reunión para presentar solución ERP propuesta",
    "fecha_hora": "2025-11-20T15:00:00Z",
    "estado": "pendiente",
    "cliente": {
      "id": 1,
      "nombre_completo": "María García López"
    },
    "oportunidad": {
      "id": 1,
      "nombre": "Implementación Sistema ERP"
    },
    "usuario": {
      "id": 1,
      "nombre_completo": "Juan Pérez"
    },
    "resultado": null,
    "fecha_creacion": "2025-11-16T13:00:00Z"
  },
  "message": "Actividad creada exitosamente"
}
```

---

**RF-019: Listar Actividades**

**Endpoint:** `GET /api/actividades/`

**Headers:** `Authorization: Bearer {access_token}`

**Query Parameters:**
- `tipo`: Filtrar por tipo
- `estado`: Filtrar por estado
- `cliente_id`: Filtrar por cliente
- `oportunidad_id`: Filtrar por oportunidad
- `fecha_desde`, `fecha_hasta`: Rango de fechas
- `ordering`: Ordenar (default: `-fecha_hora`)
- `page`, `page_size`: Paginación

**Response 200 OK:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "tipo": "reunion",
      "asunto": "Presentación de propuesta comercial",
      "fecha_hora": "2025-11-20T15:00:00Z",
      "estado": "pendiente",
      "cliente": {
        "id": 1,
        "nombre_completo": "María García López"
      },
      "oportunidad": {
        "id": 1,
        "nombre": "Implementación Sistema ERP"
      }
    }
  ],
  "count": 1,
  "message": "Actividades obtenidas exitosamente"
}
```

---

**RF-020: Marcar Actividad como Completada**

**Endpoint:** `PATCH /api/actividades/{id}/completar/`

**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "resultado": "Reunión exitosa. Cliente aprobó la propuesta. Pasamos a negociación de contrato."
}
```

**Response 200 OK:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "estado": "completada",
    "resultado": "Reunión exitosa. Cliente aprobó la propuesta. Pasamos a negociación de contrato.",
    ...
  },
  "message": "Actividad marcada como completada"
}
```

---

**RF-021: Obtener, Actualizar y Eliminar Actividad**

Endpoints estándar:
- `GET /api/actividades/{id}/`
- `PUT/PATCH /api/actividades/{id}/`
- `DELETE /api/actividades/{id}/`

---

### 3.6 Módulo de Reportes y Estadísticas

**RF-022: Dashboard - Estadísticas Generales**

**Endpoint:** `GET /api/reportes/dashboard/`

**Headers:** `Authorization: Bearer {access_token}`

**Response 200 OK:**
```json
{
  "success": true,
  "data": {
    "totales": {
      "clientes": 15,
      "empresas": 8,
      "oportunidades_abiertas": 12,
      "oportunidades_cerradas": 5,
      "actividades_pendientes": 8,
      "actividades_completadas": 25
    },
    "valores": {
      "valor_total_pipeline": 450000.00,
      "valor_ponderado_pipeline": 315000.00,
      "ventas_cerradas_mes_actual": 120000.00,
      "ventas_cerradas_mes_anterior": 80000.00
    },
    "oportunidades_por_etapa": {
      "prospeccion": 3,
      "calificacion": 2,
      "propuesta": 4,
      "negociacion": 3
    },
    "actividades_por_tipo": {
      "llamada": 10,
      "reunion": 8,
      "email": 12,
      "tarea": 3
    }
  },
  "message": "Dashboard obtenido exitosamente"
}
```

---

**RF-023: Reporte de Ventas por Período**

**Endpoint:** `GET /api/reportes/ventas/`

**Headers:** `Authorization: Bearer {access_token}`

**Query Parameters:**
- `fecha_inicio`: Fecha de inicio (formato: YYYY-MM-DD)
- `fecha_fin`: Fecha de fin
- `agrupar_por`: "dia", "semana", "mes" (default: "mes")
- `moneda`: Filtrar por moneda (opcional)

**Response 200 OK:**
```json
{
  "success": true,
  "data": {
    "periodo": {
      "fecha_inicio": "2025-01-01",
      "fecha_fin": "2025-11-30"
    },
    "resumen": {
      "total_ventas": 12,
      "valor_total": 580000.00,
      "ticket_promedio": 48333.33
    },
    "ventas_por_periodo": [
      {
        "periodo": "2025-01",
        "cantidad": 2,
        "valor_total": 95000.00
      },
      {
        "periodo": "2025-02",
        "cantidad": 1,
        "valor_total": 45000.00
      },
      {
        "periodo": "2025-03",
        "cantidad": 3,
        "valor_total": 120000.00
      }
    ]
  },
  "message": "Reporte de ventas generado exitosamente"
}
```

---

**RF-024: Reporte de Conversión del Pipeline**

**Endpoint:** `GET /api/reportes/conversion/`

**Headers:** `Authorization: Bearer {access_token}`

**Response 200 OK:**
```json
{
  "success": true,
  "data": {
    "total_oportunidades_creadas": 50,
    "total_cerradas_ganadas": 12,
    "total_cerradas_perdidas": 8,
    "tasa_conversion_general": 24.0,
    "conversion_por_etapa": {
      "prospeccion_a_calificacion": 75.0,
      "calificacion_a_propuesta": 60.0,
      "propuesta_a_negociacion": 55.0,
      "negociacion_a_cierre": 45.0
    },
    "tiempo_promedio_cierre_dias": 45
  },
  "message": "Reporte de conversión generado exitosamente"
}
```

---

**RF-025: Reporte de Clientes por Empresa**

**Endpoint:** `GET /api/reportes/clientes-por-empresa/`

**Headers:** `Authorization: Bearer {access_token}`

**Response 200 OK:**
```json
{
  "success": true,
  "data": [
    {
      "empresa_id": 1,
      "empresa_nombre": "Tech Solutions SAC",
      "num_clientes": 5,
      "num_oportunidades": 8,
      "valor_total_oportunidades": 250000.00
    },
    {
      "empresa_id": 2,
      "empresa_nombre": "Innovate Corp",
      "num_clientes": 3,
      "num_oportunidades": 4,
      "valor_total_oportunidades": 180000.00
    }
  ],
  "message": "Reporte generado exitosamente"
}
```

---

**RF-026: Exportar Datos a CSV**

**Endpoint:** `GET /api/{recurso}/export/`

Donde `{recurso}` puede ser: `clientes`, `empresas`, `oportunidades`, `actividades`

**Headers:** `Authorization: Bearer {access_token}`

**Query Parameters:** Mismos filtros que el endpoint de listado

**Response 200 OK:**

Content-Type: `text/csv`

Devuelve archivo CSV descargable con los datos solicitados.

**Ejemplo para clientes:**
```csv
id,nombre_completo,empresa,cargo,telefono,email,fecha_creacion
1,"María García López","Tech Solutions SAC","CEO","+51 999888777","maria@techsolutions.com","2025-11-16T11:30:00Z"
2,"Carlos Rodríguez","Innovate Corp","CTO","+51 988777666","carlos@innovate.com","2025-11-15T10:00:00Z"
```

---

## 4. Requisitos No Funcionales

### 4.1 Rendimiento

**RNF-001: Tiempo de Respuesta de Endpoints**

- Endpoints de consulta simple (GET por ID): < 200ms
- Endpoints de listado con filtros: < 500ms
- Endpoints de creación/actualización: < 300ms
- Endpoints de reportes complejos: < 2 segundos
- Exportaciones CSV: < 5 segundos para hasta 10,000 registros

**RNF-002: Throughput de la API**

La API debe soportar al menos 50 requests por segundo sin degradación significativa del rendimiento cuando se ejecuta en hardware modesto (2 CPU cores, 4GB RAM).

**RNF-003: Paginación Obligatoria**

Todos los endpoints de listado deben implementar paginación automática con tamaño de página por defecto de 20 items. El tamaño máximo de página permitido es 100 items para prevenir respuestas excesivamente grandes.

**RNF-004: Optimización de Consultas**

- Usar `select_related()` y `prefetch_related()` de Django ORM para evitar N+1 queries
- Implementar índices en campos frecuentemente filtrados (email, username, nombres)
- Evitar consultas dentro de loops

### 4.2 Seguridad

**RNF-005: Autenticación JWT Obligatoria**

Todos los endpoints excepto `/api/auth/login/` y `/api/auth/register/` deben requerir un token JWT válido en el header `Authorization: Bearer {token}`.

Los tokens deben tener:
- Access token: expiración de 1 hora
- Refresh token: expiración de 7 días

**RNF-006: Encriptación de Contraseñas**

Las contraseñas deben ser hasheadas usando el algoritmo por defecto de Django (PBKDF2 con SHA256) antes de almacenarse. NUNCA almacenar contraseñas en texto plano.

**RNF-007: Validación de Entrada Robusta**

- Toda entrada de usuario debe ser validada usando schemas Pydantic
- Validación debe ocurrir ANTES de procesar la lógica de negocio
- Rechazar requests con datos inválidos con código 400 y mensaje descriptivo

**RNF-008: Protección contra Inyección SQL**

- SIEMPRE usar Django ORM o consultas parametrizadas
- NUNCA construir SQL dinámico concatenando strings con input de usuario
- Sanitizar cualquier input que se use en búsquedas o filtros

**RNF-009: HTTPS en Producción**

En ambiente de producción, la API debe servirse exclusivamente sobre HTTPS. HTTP debe redirigir automáticamente a HTTPS.

**RNF-010: CORS Configurado Apropiadamente**

- En desarrollo: permitir CORS de localhost
- En producción: permitir CORS solo de dominios específicos autorizados
- No usar `CORS_ALLOW_ALL_ORIGINS = True` en producción

**RNF-011: Rate Limiting**

Implementar limitación de tasa para prevenir abuso:
- Anónimo (sin auth): 10 requests/minuto
- Autenticado: 100 requests/minuto
- Endpoint de login: 5 intentos/minuto por IP

**RNF-012: Logging de Seguridad**

Registrar eventos de seguridad en logs:
- Intentos de login fallidos
- Acceso a recursos sin autorización (403)
- Tokens JWT inválidos o expirados
- Intentos de acceso a recursos inexistentes (404)

### 4.3 Usabilidad de la API

**RNF-013: Documentación Automática**

La API debe incluir documentación interactiva generada automáticamente:
- Swagger UI en `/api/docs/`
- ReDoc en `/api/redoc/`
- Schema OpenAPI 3.0 en `/api/schema/`

La documentación debe incluir:
- Descripción de cada endpoint
- Parámetros requeridos y opcionales
- Ejemplos de request y response
- Códigos de estado HTTP posibles
- Modelos de datos con sus campos

**RNF-014: Versionado de API**

La API debe incluir versión en la URL: `/api/v1/...`

Esto permite evolución futura sin romper clientes existentes.

**RNF-015: Códigos de Estado HTTP Semánticos**

Usar códigos HTTP apropiados:
- `200 OK`: Operación exitosa (GET, PUT, PATCH)
- `201 Created`: Recurso creado exitosamente (POST)
- `204 No Content`: Eliminación exitosa (DELETE)
- `400 Bad Request`: Datos de entrada inválidos
- `401 Unauthorized`: No autenticado o token inválido
- `403 Forbidden`: No autorizado para esta acción
- `404 Not Found`: Recurso no existe
- `409 Conflict`: Conflicto (ej: username duplicado)
- `500 Internal Server Error`: Error del servidor

**RNF-016: Mensajes de Error Descriptivos**

Los mensajes de error deben ser claros y útiles en español:

❌ MAL: `{"detail": "Invalid input"}`

✅ BIEN:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Los datos proporcionados no son válidos",
    "details": {
      "email": ["El formato del email no es válido"],
      "telefono": ["Este campo es obligatorio"]
    }
  }
}
```

**RNF-017: Formato de Respuesta Consistente**

Todas las respuestas deben seguir el formato estándar definido en la sección 2.4, manteniendo consistencia en toda la API.

### 4.4 Confiabilidad

**RNF-018: Manejo Graceful de Errores**

- La API nunca debe devolver stack traces o errores de Python al cliente
- Errores inesperados deben retornar 500 con mensaje genérico al cliente
- Detalles técnicos deben loggearse internamente para debugging

**RNF-019: Transaccionalidad de Base de Datos**

Operaciones que modifican múltiples tablas deben ejecutarse en transacciones atómicas. Si una parte falla, toda la operación debe revertirse (rollback).

**RNF-020: Validación de Integridad Referencial**

Antes de eliminar registros, verificar que no tengan dependencias:
- No permitir eliminar empresa si tiene clientes u oportunidades
- No permitir eliminar cliente si tiene oportunidades activas
- Ofrecer opción de eliminación en cascada solo cuando sea seguro

**RNF-021: Logs Completos**

Implementar logging comprehensivo:
- **INFO**: Operaciones exitosas importantes
- **WARNING**: Situaciones anómalas pero no errores
- **ERROR**: Errores que requieren atención
- **DEBUG**: Información detallada para desarrollo

Logs deben incluir:
- Timestamp
- Nivel de log
- Usuario que realizó la acción (si aplica)
- Endpoint accedido
- Mensaje descriptivo

### 4.5 Mantenibilidad

**RNF-022: Código Modular y Organizado**

Estructura de proyecto Django:
```
crm_api/
├── config/                 # Configuración Django
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── authentication/     # App de autenticación
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── schemas.py      # Schemas Pydantic
│   ├── empresas/
│   ├── clientes/
│   ├── oportunidades/
│   ├── actividades/
│   └── reportes/
├── common/                 # Código compartido
│   ├── validators.py
│   ├── permissions.py
│   └── pagination.py
├── requirements.txt
├── manage.py
└── README.md
```

**RNF-023: Código Documentado**

- Cada vista (view) debe tener docstring explicando qué hace
- Funciones complejas deben incluir comentarios
- README debe explicar cómo ejecutar el proyecto
- Incluir docstrings en modelos y serializers

**RNF-024: Tests Unitarios**

El proyecto debe incluir tests unitarios para:
- Modelos (validaciones, métodos custom)
- Serializers (validación de datos)
- Vistas principales (crear, listar, actualizar, eliminar)
- Autenticación (login, permisos)

Mínimo 50% de cobertura de código.

**RNF-025: Variables de Entorno**

Configuración sensible debe estar en variables de entorno:
- `SECRET_KEY`: Secret key de Django
- `DEBUG`: True/False
- `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`
- `DATABASE_USER`, `DATABASE_PASSWORD`
- `ALLOWED_HOSTS`

Usar archivo `.env` (NO commitear al repositorio) y `python-decouple` o `django-environ`.

### 4.6 Portabilidad y Despliegue

**RNF-026: Containerización con Docker**

El proyecto debe incluir:

**Dockerfile para Django:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: crm_db
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_USER: crm_user
      MYSQL_PASSWORD: crm_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  api:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_HOST: db
      DATABASE_PORT: 3306
      DATABASE_NAME: crm_db
      DATABASE_USER: crm_user
      DATABASE_PASSWORD: crm_password

volumes:
  mysql_data:
```

**RNF-027: Comandos de Inicialización**

Incluir scripts para inicialización fácil:

```bash
# Iniciar containers
docker-compose up -d

# Ejecutar migraciones
docker-compose exec api python manage.py migrate

# Crear superusuario
docker-compose exec api python manage.py createsuperuser

# Cargar datos de prueba
docker-compose exec api python manage.py loaddata fixtures/initial_data.json
```

**RNF-028: Independencia de Plataforma**

El proyecto debe ejecutarse en:
- Windows con Docker Desktop
- macOS con Docker Desktop
- Linux con Docker CE

No debe requerir configuración específica del sistema operativo.

### 4.7 Compatibilidad

**RNF-029: Versiones de Dependencias**

Versiones específicas requeridas:
- Python: 3.10 o 3.11
- Django: 4.2.x (LTS)
- Django REST Framework: 3.14.x
- Pydantic: 2.x
- MySQL: 8.0.x
- mysqlclient: 2.2.x

**RNF-030: Compatibilidad de Clientes**

La API debe ser consumible por:
- Aplicaciones web (JavaScript/TypeScript)
- Aplicaciones móviles (iOS/Android)
- Aplicaciones desktop (Electron, etc.)
- Scripts Python
- Herramientas de testing (Postman, curl, httpie)

---

## 5. Modelo de Datos

### 5.1 Diagrama ER Simplificado

```
┌─────────────┐         ┌──────────────┐
│  Usuario    │         │   Empresa    │
├─────────────┤         ├──────────────┤
│ id (PK)     │         │ id (PK)      │
│ username    │         │ nombre       │
│ password    │         │ industria    │
│ email       │         │ num_empleados│
│ tipo        │         │ ...          │
└──────┬──────┘         └──────┬───────┘
       │                       │
       │ crea                  │ tiene
       │                       │
       ▼                       ▼
┌─────────────┐         ┌──────────────┐
│  Actividad  │◄────┐   │   Cliente    │
├─────────────┤     │   ├──────────────┤
│ id (PK)     │     │   │ id (PK)      │
│ tipo        │     │   │ nombre       │
│ asunto      │     │   │ empresa_id(FK)│
│ fecha_hora  │     │   │ email        │
│ estado      │     │   │ telefono     │
│ usuario_id  │     │   │ ...          │
│ cliente_id  │     │   └──────┬───────┘
│ oport_id    │     │          │
└─────────────┘     │          │ tiene
                    │          │
                    │          ▼
                    │   ┌──────────────┐
                    └───┤ Oportunidad  │
                        ├──────────────┤
                        │ id (PK)      │
                        │ nombre       │
                        │ cliente_id(FK)│
                        │ empresa_id(FK)│
                        │ valor        │
                        │ etapa        │
                        │ estado       │
                        │ ...          │
                        └──────────────┘
```

### 5.2 Modelos Django

**Usuario (users.User):**
```python
class User(AbstractUser):
    nombre_completo = models.CharField(max_length=150)
    tipo = models.CharField(max_length=10, choices=[
        ('admin', 'Administrador'),
        ('regular', 'Regular')
    ])
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

**Empresa (empresas.Empresa):**
```python
class Empresa(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    industria = models.CharField(max_length=50, null=True, blank=True)
    num_empleados = models.IntegerField(null=True, blank=True)
    sitio_web = models.URLField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=300, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

**Cliente (clientes.Cliente):**
```python
class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=150)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.CharField(max_length=300, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

**Oportunidad (oportunidades.Oportunidad):**
```python
class Oportunidad(models.Model):
    ETAPAS = [
        ('prospeccion', 'Prospección'),
        ('calificacion', 'Calificación'),
        ('propuesta', 'Propuesta'),
        ('negociacion', 'Negociación'),
        ('cerrado_ganado', 'Cerrado Ganado'),
        ('cerrado_perdido', 'Cerrado Perdido'),
    ]
    
    nombre = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.CharField(max_length=3, default='PEN')
    probabilidad = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    fecha_cierre_estimada = models.DateField()
    etapa = models.CharField(max_length=20, choices=ETAPAS)
    estado = models.CharField(max_length=10, default='abierta')
    resultado = models.CharField(max_length=10, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre_real = models.DateTimeField(null=True, blank=True)
    
    @property
    def valor_ponderado(self):
        return self.valor * (self.probabilidad / 100)
```

**Actividad (actividades.Actividad):**
```python
class Actividad(models.Model):
    TIPOS = [
        ('llamada', 'Llamada'),
        ('reunion', 'Reunión'),
        ('email', 'Email'),
        ('tarea', 'Tarea'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPOS)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=15, default='pendiente')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    oportunidad = models.ForeignKey(Oportunidad, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    resultado = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

---

## 6. Integración de Pydantic con Django

### 6.1 Propósito de Pydantic en el Proyecto

Pydantic se usará para validación de datos de entrada más robusta que los serializers estándar de DRF. Proporciona:
- Type hints y validación automática de tipos
- Validaciones personalizadas complejas
- Mensajes de error claros y detallados
- Mejor experiencia de desarrollo con IDE autocompletion

### 6.2 Ejemplo de Integración

**Schema Pydantic (schemas.py):**
```python
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import date

class ClienteCreateSchema(BaseModel):
    nombre_completo: str = Field(..., min_length=3, max_length=150)
    empresa_id: int = Field(..., gt=0)
    cargo: Optional[str] = Field(None, max_length=100)
    telefono: str = Field(..., min_length=7, max_length=20)
    email: EmailStr
    direccion: Optional[str] = Field(None, max_length=300)
    notas: Optional[str] = Field(None, max_length=1000)
    
    @validator('telefono')
    def validar_telefono(cls, v):
        # Validación personalizada de formato de teléfono
        if not v.startswith('+') and not v.startswith('0'):
            raise ValueError('El teléfono debe comenzar con + o 0')
        return v

class OportunidadCreateSchema(BaseModel):
    nombre: str = Field(..., min_length=5, max_length=200)
    cliente_id: int = Field(..., gt=0)
    empresa_id: int = Field(..., gt=0)
    valor: float = Field(..., gt=0)
    moneda: str = Field(..., regex='^(PEN|USD|EUR)$')
    probabilidad: int = Field(..., ge=0, le=100)
    fecha_cierre_estimada: date
    etapa: str
    notas: Optional[str] = None
    
    @validator('fecha_cierre_estimada')
    def validar_fecha_futura(cls, v):
        from datetime import date
        if v < date.today():
            raise ValueError('La fecha de cierre debe ser futura')
        return v
```

**Vista usando Pydantic (views.py):**
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .schemas import ClienteCreateSchema
from .models import Cliente
from pydantic import ValidationError

class ClienteCreateView(APIView):
    def post(self, request):
        try:
            # Validar con Pydantic
            schema = ClienteCreateSchema(**request.data)
            
            # Crear el cliente si la validación pasa
            cliente = Cliente.objects.create(
                nombre_completo=schema.nombre_completo,
                empresa_id=schema.empresa_id,
                cargo=schema.cargo,
                telefono=schema.telefono,
                email=schema.email,
                direccion=schema.direccion,
                notas=schema.notas
            )
            
            return Response({
                'success': True,
                'data': ClienteSerializer(cliente).data,
                'message': 'Cliente creado exitosamente'
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Datos inválidos',
                    'details': e.errors()
                }
            }, status=status.HTTP_400_BAD_REQUEST)
```

---

## 7. Configuración del Proyecto

### 7.1 Archivo requirements.txt

```txt
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
drf-spectacular==0.26.5
pydantic==2.5.0
pydantic[email]==2.5.0
mysqlclient==2.2.0
python-decouple==3.8
django-cors-headers==4.3.0
django-filter==23.3
gunicorn==21.2.0
```

### 7.2 Configuración Django (settings.py)

```python
# INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'corsheaders',
    'django_filters',
    
    # Local apps
    'apps.authentication',
    'apps.empresas',
    'apps.clientes',
    'apps.oportunidades',
    'apps.actividades',
    'apps.reportes',
]

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT', default='3306'),
    }
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Spectacular (OpenAPI/Swagger)
SPECTACULAR_SETTINGS = {
    'TITLE': 'CRM API',
    'DESCRIPTION': 'API REST para Sistema de Gestión de Relaciones con Clientes',
    'VERSION': '1.0.0',
}
```

---

## 8. Criterios de Aceptación

### 8.1 Criterios Funcionales

✅ Todos los endpoints especificados (RF-001 a RF-026) están implementados  
✅ La autenticación JWT funciona correctamente  
✅ Los filtros y búsquedas funcionan en todos los listados  
✅ La paginación está implementada en todos los endpoints de listado  
✅ Los reportes generan datos correctos  
✅ La exportación CSV funciona  

### 8.2 Criterios Técnicos

✅ El proyecto se ejecuta sin errores en Docker  
✅ Las validaciones Pydantic están implementadas  
✅ Los modelos Django tienen las relaciones correctas  
✅ La documentación Swagger está accesible y completa  
✅ Los códigos de estado HTTP son apropiados  
✅ El formato de respuestas es consistente  

### 8.3 Criterios de Calidad

✅ El código está organizado según la estructura especificada  
✅ Hay comentarios en código complejo  
✅ Las variables de entorno están configuradas  
✅ El README incluye instrucciones de instalación y uso  
✅ Hay al menos 10 tests unitarios funcionando  

### 8.4 Criterios de Documentación

✅ README completo con instalación y ejecución  
✅ Diagrama de base de datos  
✅ Colección de Postman o ejemplos de curl  
✅ Documentación de endpoints en Swagger/OpenAPI  

---

## 9. Plan de Implementación

### Fase 1 - Setup Inicial (Semana 1-2)
- ✅ Configurar entorno Docker
- ✅ Crear proyecto Django con estructura de apps
- ✅ Configurar MySQL y conexión
- ✅ Implementar modelos de base de datos
- ✅ Crear migraciones
- ✅ Configurar JWT authentication

### Fase 2 - CRUD Básico (Semana 3-5)
- ✅ Implementar app de empresas (endpoints + schemas)
- ✅ Implementar app de clientes
- ✅ Implementar validaciones Pydantic
- ✅ Probar endpoints con Postman

### Fase 3 - Oportunidades y Actividades (Semana 6-8)
- ✅ Implementar app de oportunidades
- ✅ Implementar endpoint de pipeline
- ✅ Implementar app de actividades
- ✅ Implementar filtros avanzados

### Fase 4 - Reportes (Semana 9-10)
- ✅ Implementar dashboard
- ✅ Implementar reportes de ventas
- ✅ Implementar reporte de conversión
- ✅ Implementar exportación CSV

### Fase 5 - Testing y Documentación (Semana 11-12)
- ✅ Escribir tests unitarios
- ✅ Generar documentación Swagger
- ✅ Crear colección Postman
- ✅ Completar README

### Fase 6 - Refinamiento (Semana 13-14)
- ✅ Corregir bugs encontrados
- ✅ Optimizar queries lentas
- ✅ Mejorar mensajes de error
- ✅ Preparar presentación final

---

## 10. Guía de Testing con Postman

### 10.1 Colección de Endpoints

Crear una colección de Postman con los siguientes requests:

**Carpeta: Authentication**
- POST Login
- POST Register
- POST Refresh Token
- GET List Users (admin)

**Carpeta: Empresas**
- POST Create Empresa
- GET List Empresas
- GET Get Empresa by ID
- PATCH Update Empresa
- DELETE Delete Empresa

**Carpeta: Clientes**
- POST Create Cliente
- GET List Clientes
- GET Get Cliente by ID
- PATCH Update Cliente
- DELETE Delete Cliente

**Carpeta: Oportunidades**
- POST Create Oportunidad
- GET List Oportunidades
- GET Pipeline
- PATCH Update Etapa
- DELETE Delete Oportunidad

**Carpeta: Actividades**
- POST Create Actividad
- GET List Actividades
- PATCH Completar Actividad

**Carpeta: Reportes**
- GET Dashboard
- GET Reporte Ventas
- GET Reporte Conversión

### 10.2 Variables de Entorno Postman

```json
{
  "api_url": "http://localhost:8000/api/v1",
  "access_token": "{{access_token}}",
  "refresh_token": "{{refresh_token}}"
}
```

### 10.3 Scripts Postman

**Guardar token automáticamente después de login:**
```javascript
// En el tab "Tests" del request de login
let jsonData = pm.response.json();
pm.environment.set("access_token", jsonData.data.access);
pm.environment.set("refresh_token", jsonData.data.refresh);
```

---

## Anexo A: Comandos Docker Útiles

```bash
# Construir y levantar containers
docker-compose up --build

# Ver logs de la API
docker-compose logs -f api

# Acceder a shell del container de API
docker-compose exec api bash

# Ejecutar migraciones
docker-compose exec api python manage.py migrate

# Crear superusuario
docker-compose exec api python manage.py createsuperuser

# Ejecutar tests
docker-compose exec api python manage.py test

# Detener containers
docker-compose down

# Detener y eliminar volúmenes (BORRA DATOS)
docker-compose down -v
```

---

## Anexo B: Ejemplos de Curl

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Crear Cliente:**
```bash
curl -X POST http://localhost:8000/api/v1/clientes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "nombre_completo": "Juan Pérez",
    "empresa_id": 1,
    "cargo": "Gerente",
    "telefono": "+51987654321",
    "email": "juan@example.com"
  }'
```

**Listar Oportunidades con Filtros:**
```bash
curl -X GET "http://localhost:8000/api/v1/oportunidades/?estado=abierta&etapa=propuesta" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

**Fin del Documento SRS - API REST CRM**

Este documento proporciona especificaciones completas para desarrollar una API REST profesional y funcional usando Django, Pydantic, MySQL y Docker como proyecto académico.