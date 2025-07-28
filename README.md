# Pasarela MCP para Odoo (MCP-Odoo)

## Descripción
MCP Gateway for Odoo (MCP-Odoo) es un servicio que proporciona una interfaz de pasarela para la funcionalidad de Odoo. Este servicio está construido utilizando FastAPI y está diseñado para ejecutarse en un entorno containerizado.

## Estructura del Proyecto
```
MCP-Odoo/
├── src/
│   ├── config/
│   │   └── config.py          # Gestión de configuración
│   ├── models/
│   │   ├── models_product.py  # Modelos de productos
│   │   ├── models_sale.py     # Modelos de ventas
│   │   └── models_user.py     # Modelos de usuarios
│   ├── tools/                 # Herramientas MCP
│   │   ├── __init__.py       # Registro y exportación de herramientas
│   │   ├── odoo_api.py       # Cliente API de Odoo
│   │   ├── products/         # Herramientas para productos
│   │   ├── sales/            # Herramientas para ventas
│   │   └── users/            # Herramientas para usuarios
│   ├── tests/                # Pruebas unitarias
│   │   ├── test_api_client.py
│   │   ├── test_config.py
│   │   ├── test_download_routes.py
│   │   ├── test_models.py
│   │   ├── test_server.py
│   │   └── test_tools.py
│   ├── server.py             # Servidor principal FastAPI
│   ├── pyproject.toml        # Dependencias y configuración del proyecto
│   └── uv.lock              # Archivo de bloqueo de dependencias
└── docs/                    # Documentación
    └── prompts/             # Prompts para agentes IA
```

## Requisitos
- Python 3.10 o superior
- Docker (para despliegue containerizado)

## Dependencias
El proyecto utiliza las siguientes dependencias principales:
- FastAPI (>=0.110) - Framework web para construcción de APIs
- HTTPX (>=0.27) - Cliente HTTP con soporte para HTTP/2
- Uvicorn (>=0.29) - Implementación de servidor ASGI
- Python-dotenv (>=1.0) - Gestión de variables de entorno
- Pydantic (>=2.7) - Validación de datos usando anotaciones de tipo Python
- MCP (>=0.1.0) - Funcionalidad central de MCP
- OdooRPC (>=0.9.0) - Cliente RPC para Odoo

### Dependencias de Desarrollo
Para desarrollo y pruebas, el proyecto requiere las siguientes dependencias adicionales:
- pytest (>=8.0.0) - Framework de pruebas
- pytest-asyncio (>=0.23.0) - Soporte para pruebas asíncronas
- pytest-mock (>=3.12.0) - Utilidades de mock para pruebas

## Configuración e Instalación

### Desarrollo Local
1. Asegúrate de tener Python 3.10+ instalado
2. Instala el gestor de paquetes `uv`
3. Clona el repositorio
4. Navega al directorio del proyecto
5. Crea un entorno virtual usando `uv`:
   ```bash
   uv venv
   ```
6. Activa el entorno virtual:
   ```bash
   source .venv/bin/activate
   ```
7. Instala las dependencias incluyendo las de desarrollo:
   ```bash
   uv pip install -e "src/[test]"
   ```
8. Ejecuta el servidor:
   ```bash
   uv run python src/server.py
   ```

### Despliegue con Docker
El proyecto incluye un Dockerfile para el despliegue containerizado. El Dockerfile utiliza un proceso de construcción multi-etapa para optimizar el tamaño de la imagen y la seguridad.

#### Características del Dockerfile:
- **Imagen Base**: Utiliza `ghcr.io/astral-sh/uv:python3.11-bookworm-slim` tanto para la etapa de construcción como para la de ejecución
- **Construcción Multi-etapa**:
  1. Etapa de construcción:
     - Instala las dependencias usando `uv`
     - Copia y prepara el código de la aplicación
  2. Etapa de ejecución:
     - Crea un usuario sin privilegios de root para seguridad
     - Configura el entorno Python
     - Expone el puerto 3000

#### Construcción y Ejecución con Docker
1. Construir la imagen:
   ```bash
   docker build -t mcp-odoo .
   ```

2. Ejecutar el contenedor:
   ```bash
   docker run -p 3000:3000 -e ODOO_URL=http://localhost:8069 -e ODOO_DB=joel -e ODOO_USER=joel.ruvira@cloudlevante.com -e ODOO_PASS=joel mcp-odoo
   ```

## Herramientas MCP
El proyecto incluye un conjunto de herramientas MCP para interactuar con la API de Odoo:

### Estructura de Herramientas
- **__init__.py**: Registra y exporta todas las herramientas MCP disponibles
- **odoo_api.py**: Cliente principal para la API de Odoo
- **products/**: Herramientas para gestión de productos
  - Crear y actualizar productos
  - Buscar productos
  - Gestionar variantes y atributos
- **sales/**: Herramientas para gestión de ventas
  - Crear y actualizar pedidos
  - Gestionar líneas de pedido
  - Procesar pagos y facturas
- **users/**: Herramientas para gestión de usuarios
  - Crear y actualizar usuarios
  - Gestionar permisos y roles
  - Autenticación y sesiones

## Pruebas
El proyecto incluye un conjunto completo de pruebas unitarias para el cliente API y las herramientas MCP.

### Ejecutar las Pruebas
Para ejecutar todas las pruebas usando `uv`:
```bash
uv run --active pytest tests/ -v
```

Para ejecutar un archivo de pruebas específico:
```bash
uv run --active pytest tests/test_api_client.py -v
```

Para ejecutar una prueba específica:
```bash
uv run --active pytest tests/test_tools.py::test_create_product -v
```

También puedes usar `pytest` directamente si estás en el entorno virtual:
```bash
pytest tests/ -v
```

### Cobertura de Pruebas
Las pruebas cubren:
- Cliente API (OdooAPIClient)
  - Autenticación y gestión de sesiones
  - CRUD de productos, ventas y usuarios
  - Manejo de errores y excepciones
- Herramientas MCP
  - Validación de datos de entrada
  - Transformación de datos
  - Integración con Odoo
  - Gestión de modelos y relaciones

## Configuración
La aplicación utiliza variables de entorno para su configuración. Crea un archivo `.env` en el directorio raíz con las variables necesarias.

### Variables de Entorno Básicas
  # Configuración de conexión a Odoo
  - ODOO_URL=http://localhost:8069
  - ODOO_DB=nombre_base_datos
  - ODOO_USER=usuario@ejemplo.com
  - ODOO_PASS=contraseña

  # TCP port where the MCP server runs
  - MCP_SERVER_PORT=3000

  # Logging level (DEBUG, INFO, WARNING, ERROR)
  - LOG_LEVEL=INFO

### Variables de Entorno para Modos de Despliegue
La aplicación soporta dos modos de despliegue que se configuran mediante las siguientes variables:

#### Modo Local
  - DEPLOYMENT_MODE=local
  - MCP_SERVER_HOST=0.0.0.0
  - MCP_SERVER_PORT=3000

#### Modo Producción
  - DEPLOYMENT_MODE=production
  - MCP_PRODUCTION_URL=https://odoo-mcp.ejemplo.com

## Modos de Despliegue

### Modo Local
El modo local está diseñado para desarrollo y pruebas. En este modo:
- La aplicación se ejecuta en `0.0.0.0:3000`
- Las URLs generadas usan el host y puerto local
- Ideal para desarrollo y pruebas locales

Para ejecutar en modo local:
```bash
DEPLOYMENT_MODE=local MCP_SERVER_HOST=0.0.0.0 MCP_SERVER_PORT=3000 uv run python src/server.py
```

### Modo Producción
El modo producción está diseñado para despliegue en servidores. En este modo:
- Las URLs generadas usan la URL de producción configurada
- Soporta HTTPS y dominios personalizados
- Recomendado para ambientes de producción

Para ejecutar en modo producción:
```bash
DEPLOYMENT_MODE=production MCP_PRODUCTION_URL=https://odoo-mcp.ejemplo.com uv run python src/server.py
```

## Estilo de Código
El proyecto utiliza Ruff para el formateo y linting del código con la siguiente configuración:
- Longitud de línea: 100 caracteres
- Reglas seleccionadas: E (pycodestyle), F (pyflakes), I (isort)
- Organización personalizada de importaciones para módulos del proyecto

## Seguridad
- El contenedor Docker se ejecuta bajo un usuario sin privilegios de root para mayor seguridad
- Las dependencias están bloqueadas usando `uv.lock` para garantizar builds reproducibles
- Soporte para HTTP/2 habilitado para mejor rendimiento y seguridad
- Gestión segura de credenciales de Odoo usando variables de entorno

