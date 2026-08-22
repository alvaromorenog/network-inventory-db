# 🗄️ Network Inventory DB — Inventario de dispositivos de red

Proyecto individual — Python + PostgreSQL

## 📋 Descripción

Sistema de inventario de dispositivos de red gestionado por terminal, que permite registrar, consultar, actualizar y eliminar dispositivos (routers, PCs, cámaras IP, móviles, etc.) identificados por su IP y dirección MAC.

El proyecto se desarrolló como ejercicio para aplicar de forma conjunta conocimientos de **diseño de bases de datos**, **SQL** y **Python**, conectando ambos mundos mediante `psycopg2`.

## 🎯 Objetivo

Diseñar e implementar un sistema CRUD completo (Crear, Leer, Actualizar, Eliminar) sobre una base de datos relacional, aplicando buenas prácticas de:
- Diseño de esquema con restricciones de integridad (`UNIQUE`, `NOT NULL`)
- Uso de *prepared statements* para evitar inyección SQL
- Gestión de conexiones y manejo de errores en Python
- Separación de credenciales del código fuente

## 🏗️ Modelo de datos

```
Dispositivo
-----------
id              SERIAL PRIMARY KEY
nombre          VARCHAR(100)  NOT NULL
ip              VARCHAR(15)   UNIQUE NOT NULL
mac             VARCHAR(17)   UNIQUE NOT NULL
tipo            VARCHAR(50)   NOT NULL   -- router, PC, cámara IP, móvil...
ubicacion       VARCHAR(100)
fecha_registro  TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
```

*(Diagrama entidad-relación disponible en [`docs/er-diagram.png`](docs/er-diagram.png))*

## 🔧 Tecnologías utilizadas

| Componente | Herramienta |
|---|---|
| Lenguaje | Python 3 |
| Base de datos | PostgreSQL |
| Conector | psycopg2-binary |
| Interfaz | Terminal (CLI) |

## ✅ Funcionalidades

- [x] Añadir dispositivo (con validación de IP/MAC duplicadas)
- [x] Listar todos los dispositivos registrados
- [x] Buscar dispositivo por IP o MAC
- [x] Actualizar nombre y/o ubicación de un dispositivo existente
- [x] Eliminar dispositivo (con confirmación previa)
- [ ] Autodescubrimiento de dispositivos en la red mediante escaneo (Scapy) — próxima mejora

## 📁 Estructura del repositorio

```
network-inventory-db/
├── README.md
├── LICENSE
├── .gitignore
├── schema.sql              # Script de creación de la tabla
├── requirements.txt        # Dependencias de Python
├── config.example.py       # Plantilla de configuración (sin credenciales reales)
├── inventory.py            # Script principal (menú CRUD)
└── docs/
    └── er-diagram.png      # Diagrama entidad-relación
```

## 🚀 Instalación y uso

### Requisitos previos
- PostgreSQL instalado y en ejecución
- Python 3.8 o superior

### Pasos

**1. Clona el repositorio**
```bash
git clone https://github.com/alvaromorenog/network-inventory-db.git
cd network-inventory-db
```

**2. Instala las dependencias**
```bash
pip install -r requirements.txt
```

**3. Crea la base de datos**

Desde `psql` (o SQL Shell en Windows):
```sql
CREATE DATABASE network_inventory;
\c network_inventory
```

Ejecuta el script de esquema:
```bash
psql -U postgres -d network_inventory -f schema.sql
```

**4. Configura las credenciales**

Copia la plantilla y edítala con tus datos:
```bash
cp config.example.py config.py
```
Edita `config.py` y sustituye `<TU_CONTRASEÑA_AQUI>` por tu contraseña real de PostgreSQL.

> ⚠️ `config.py` está incluido en `.gitignore` y nunca debe subirse al repositorio.

**5. Ejecuta el programa**
```bash
python inventory.py
```

## 🔒 Seguridad

- Las credenciales de conexión se gestionan en un fichero `config.py` externo, excluido del control de versiones.
- Todas las consultas SQL usan *prepared statements* (parámetros `%s`), evitando inyección SQL.
- Las columnas `ip` y `mac` tienen restricción `UNIQUE` a nivel de base de datos, evitando registros duplicados incluso ante fallos de validación en la aplicación.

## 📌 Próximas mejoras

- Autodescubrimiento de dispositivos en la red local mediante escaneo con Scapy, para poblar la base de datos automáticamente en lugar de introducir los datos manualmente.
- Exportación del inventario a CSV.

---

📫 Autor: **Álvaro Moreno González** — [LinkedIn](https://www.linkedin.com/in/álvaro-moreno-gonzález-14792b367)
