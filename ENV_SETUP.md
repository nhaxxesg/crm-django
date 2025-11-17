# Configuración de Variables de Entorno

Este documento explica cómo configurar las variables de entorno necesarias para el CRM API.

## 📋 Variables Requeridas

El proyecto utiliza `django-environ` para gestionar las variables de entorno. Todas las variables se leen desde un archivo `.env` en la raíz del proyecto.

### Variables Obligatorias

| Variable | Descripción | Ejemplo | Default |
|----------|-------------|---------|---------|
| `SECRET_KEY` | Clave secreta de Django (obligatoria en producción) | `django-insecure-...` | `changeme-insecure-key` |
| `DEBUG` | Modo debug (True/False) | `True` | `False` |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por comas) | `localhost,127.0.0.1` | `localhost,127.0.0.1` |
| `DATABASE_NAME` | Nombre de la base de datos MySQL | `crm_db` | `crm_db` |
| `DATABASE_USER` | Usuario de MySQL | `crm_user` | `crm_user` |
| `DATABASE_PASSWORD` | Contraseña de MySQL | `mi_password_seguro` | `crm_password` |
| `DATABASE_HOST` | Host de MySQL | `localhost` o `db` (Docker) | `localhost` |
| `DATABASE_PORT` | Puerto de MySQL | `3306` | `3306` |

## 🚀 Configuración Rápida

### 1. Crear archivo `.env`

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

### 2. Editar `.env`

Abre el archivo `.env` y ajusta los valores según tu entorno:

```bash
# Desarrollo local
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=crm_db
DATABASE_USER=crm_user
DATABASE_PASSWORD=tu_password
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

### 3. Generar SECRET_KEY (Recomendado)

Para generar una clave secreta segura:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y pégalo en `SECRET_KEY` de tu archivo `.env`.

## 🐳 Configuración para Docker

Si usas Docker Compose, las variables pueden definirse en el archivo `docker-compose.yml` o en un `.env` compartido:

```yaml
# docker-compose.yml
services:
  api:
    environment:
      DATABASE_HOST: db
      DATABASE_NAME: crm_db
      DATABASE_USER: crm_user
      DATABASE_PASSWORD: crm_password
```

O en el archivo `.env`:

```bash
DATABASE_HOST=db  # Nombre del servicio en docker-compose
DATABASE_NAME=crm_db
DATABASE_USER=crm_user
DATABASE_PASSWORD=crm_password
```

## 🔒 Seguridad

### ⚠️ IMPORTANTE

- **NUNCA** commitees el archivo `.env` al repositorio
- El archivo `.env` ya está en `.gitignore`
- Usa valores diferentes para desarrollo y producción
- En producción, usa una `SECRET_KEY` fuerte y única
- No compartas tus credenciales de base de datos

### Variables Sensibles

Las siguientes variables contienen información sensible:
- `SECRET_KEY`
- `DATABASE_PASSWORD`
- Cualquier token o API key que agregues en el futuro

## 📝 Ejemplos por Ambiente

### Desarrollo Local

```bash
SECRET_KEY=django-insecure-dev-key-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,*
DATABASE_NAME=crm_dev
DATABASE_USER=root
DATABASE_PASSWORD=
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

### Producción

```bash
SECRET_KEY=tu-clave-secreta-super-segura-generada-aleatoriamente
DEBUG=False
ALLOWED_HOSTS=api.tudominio.com,www.tudominio.com
DATABASE_NAME=crm_prod
DATABASE_USER=crm_prod_user
DATABASE_PASSWORD=password-super-seguro-y-complejo
DATABASE_HOST=db.production.server
DATABASE_PORT=3306
```

## ✅ Verificar Configuración

Para verificar que las variables se están leyendo correctamente:

```bash
python manage.py check
```

Si hay errores de configuración, Django los mostrará.

## 🔍 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'environ'"

Instala `django-environ`:

```bash
pip install django-environ
```

### Error: "ImproperlyConfigured: Error loading MySQLdb module"

El proyecto usa `PyMySQL` como alternativa a `mysqlclient`. Asegúrate de que esté instalado:

```bash
pip install PyMySQL
```

Y que el archivo `config/__init__.py` tenga la configuración de PyMySQL (ya está incluida).

### Variables no se leen

1. Verifica que el archivo `.env` esté en la raíz del proyecto (mismo nivel que `manage.py`)
2. Verifica que no haya espacios alrededor del `=` en las variables
3. Verifica que las comillas no sean necesarias (solo si el valor contiene espacios)

## 📚 Referencias

- [django-environ Documentation](https://django-environ.readthedocs.io/)
- [Django Settings](https://docs.djangoproject.com/en/4.2/topics/settings/)
- [12 Factor App - Config](https://12factor.net/config)

