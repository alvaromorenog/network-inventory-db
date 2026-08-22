-- Esquema de la base de datos network_inventory
-- Ejecutar dentro de SQL Shell (psql) tras conectar con: \c network_inventory

CREATE TABLE dispositivos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ip VARCHAR(15) UNIQUE NOT NULL,
    mac VARCHAR(17) UNIQUE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
