"""
Sistema de inventario de dispositivos de red.
Permite añadir, listar, buscar, actualizar y eliminar dispositivos
almacenados en una base de datos PostgreSQL.

Requiere un fichero config.py con las credenciales de conexión
(ver config.example.py como plantilla).
"""

import psycopg2
from psycopg2 import errors

try:
    from config import DB_CONFIG
except ImportError:
    print("ERROR: No se encontró el fichero config.py.")
    print("Copia config.example.py como config.py y rellena tus credenciales.")
    exit(1)


def conectar():
    """Abre una conexión a la base de datos."""
    return psycopg2.connect(**DB_CONFIG)


def añadir_dispositivo():
    print("\n--- Añadir nuevo dispositivo ---")
    nombre = input("Nombre: ").strip()
    ip = input("IP (ej. 192.168.1.10): ").strip()
    mac = input("MAC (ej. AA:BB:CC:DD:EE:FF): ").strip()
    tipo = input("Tipo (router, PC, cámara IP, móvil...): ").strip()
    ubicacion = input("Ubicación (opcional): ").strip() or None

    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO dispositivos (nombre, ip, mac, tipo, ubicacion)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (nombre, ip, mac, tipo, ubicacion),
            )
        conn.commit()
        print(f"✅ Dispositivo '{nombre}' añadido correctamente.")
    except errors.UniqueViolation:
        conn.rollback()
        print("❌ Error: ya existe un dispositivo con esa IP o MAC.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al añadir el dispositivo: {e}")
    finally:
        conn.close()


def listar_dispositivos():
    print("\n--- Listado de dispositivos ---")
    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nombre, ip, mac, tipo, ubicacion, fecha_registro
                FROM dispositivos
                ORDER BY id
                """
            )
            filas = cur.fetchall()

        if not filas:
            print("No hay dispositivos registrados todavía.")
            return

        print(f"{'ID':<4}{'Nombre':<20}{'IP':<16}{'MAC':<19}{'Tipo':<15}{'Ubicación':<15}{'Registrado'}")
        print("-" * 100)
        for fila in filas:
            id_, nombre, ip, mac, tipo, ubicacion, fecha = fila
            ubicacion = ubicacion or "-"
            print(f"{id_:<4}{nombre:<20}{ip:<16}{mac:<19}{tipo:<15}{ubicacion:<15}{fecha}")
    except Exception as e:
        print(f"❌ Error al listar dispositivos: {e}")
    finally:
        conn.close()


def buscar_dispositivo():
    print("\n--- Buscar dispositivo ---")
    termino = input("Introduce IP o MAC a buscar: ").strip()

    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nombre, ip, mac, tipo, ubicacion, fecha_registro
                FROM dispositivos
                WHERE ip = %s OR mac = %s
                """,
                (termino, termino),
            )
            resultado = cur.fetchone()

        if resultado:
            id_, nombre, ip, mac, tipo, ubicacion, fecha = resultado
            print("\n✅ Dispositivo encontrado:")
            print(f"  ID:         {id_}")
            print(f"  Nombre:     {nombre}")
            print(f"  IP:         {ip}")
            print(f"  MAC:        {mac}")
            print(f"  Tipo:       {tipo}")
            print(f"  Ubicación:  {ubicacion or '-'}")
            print(f"  Registrado: {fecha}")
        else:
            print("No se encontró ningún dispositivo con esa IP/MAC.")
    except Exception as e:
        print(f"❌ Error al buscar el dispositivo: {e}")
    finally:
        conn.close()


def actualizar_dispositivo():
    print("\n--- Actualizar dispositivo ---")
    ip_actual = input("IP del dispositivo a actualizar: ").strip()

    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM dispositivos WHERE ip = %s", (ip_actual,))
            if cur.fetchone() is None:
                print("No existe ningún dispositivo con esa IP.")
                return

        print("Deja en blanco los campos que no quieras cambiar.")
        nuevo_nombre = input("Nuevo nombre: ").strip()
        nueva_ubicacion = input("Nueva ubicación: ").strip()

        campos = []
        valores = []
        if nuevo_nombre:
            campos.append("nombre = %s")
            valores.append(nuevo_nombre)
        if nueva_ubicacion:
            campos.append("ubicacion = %s")
            valores.append(nueva_ubicacion)

        if not campos:
            print("No se ha introducido ningún cambio.")
            return

        valores.append(ip_actual)
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE dispositivos SET {', '.join(campos)} WHERE ip = %s",
                valores,
            )
        conn.commit()
        print("✅ Dispositivo actualizado correctamente.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al actualizar el dispositivo: {e}")
    finally:
        conn.close()


def eliminar_dispositivo():
    print("\n--- Eliminar dispositivo ---")
    ip = input("IP del dispositivo a eliminar: ").strip()
    confirmacion = input(f"¿Seguro que quieres eliminar el dispositivo con IP {ip}? (s/n): ").strip().lower()

    if confirmacion != "s":
        print("Operación cancelada.")
        return

    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM dispositivos WHERE ip = %s", (ip,))
            filas_afectadas = cur.rowcount
        conn.commit()

        if filas_afectadas > 0:
            print("✅ Dispositivo eliminado correctamente.")
        else:
            print("No se encontró ningún dispositivo con esa IP.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al eliminar el dispositivo: {e}")
    finally:
        conn.close()


def menu():
    opciones = {
        "1": añadir_dispositivo,
        "2": listar_dispositivos,
        "3": buscar_dispositivo,
        "4": actualizar_dispositivo,
        "5": eliminar_dispositivo,
    }

    while True:
        print("\n===== INVENTARIO DE DISPOSITIVOS DE RED =====")
        print("1. Añadir dispositivo")
        print("2. Listar dispositivos")
        print("3. Buscar dispositivo (por IP/MAC)")
        print("4. Actualizar dispositivo")
        print("5. Eliminar dispositivo")
        print("0. Salir")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "0":
            print("Saliendo...")
            break
        elif opcion in opciones:
            opciones[opcion]()
        else:
            print("Opción no válida, inténtalo de nuevo.")


if __name__ == "__main__":
    menu()
