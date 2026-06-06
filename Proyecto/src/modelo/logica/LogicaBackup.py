import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from src.modelo.conexion.Conexion import Conexion


class LogicaBackup:
    """
    Lógica de negocio para crear y restaurar copias de seguridad
    de la base de datos desde la aplicación.
    """

    def __init__(self):
        conexion = Conexion()

        self._host = conexion._host
        self._database = conexion._database
        self._user = conexion._user
        self._password = conexion._password

        try:
            conexion.closeConnection()
        except Exception:
            pass

    def _buscar_ejecutable_mysql(self, nombre):
        ruta = shutil.which(nombre)

        if ruta:
            return ruta

        posibles_rutas = [
            fr"C:\Program Files\MySQL\MySQL Server 8.0\bin\{nombre}.exe",
            fr"C:\Program Files\MySQL\MySQL Server 8.1\bin\{nombre}.exe",
            fr"C:\Program Files\MySQL\MySQL Server 8.2\bin\{nombre}.exe",
            fr"C:\Program Files\MySQL\MySQL Server 8.3\bin\{nombre}.exe",
            fr"C:\Program Files\MySQL\MySQL Server 8.4\bin\{nombre}.exe",
        ]

        for ruta_posible in posibles_rutas:
            if os.path.exists(ruta_posible):
                return ruta_posible

        raise FileNotFoundError(
            f"No se encontró {nombre}. Añade la carpeta bin de MySQL al PATH."
        )

    def crear_copia_seguridad(self):
        carpeta_backups = Path("backups")
        carpeta_backups.mkdir(exist_ok=True)

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"backup_{self._database}_{fecha}.sql"
        ruta_backup = carpeta_backups / nombre_archivo

        mysqldump = self._buscar_ejecutable_mysql("mysqldump")

        comando = [
            mysqldump,
            f"--host={self._host}",
            f"--user={self._user}",
            f"--password={self._password}",
            "--databases",
            self._database,
            "--routines",
            "--triggers",
            "--events"
        ]

        with open(ruta_backup, "w", encoding="utf-8") as archivo:
            resultado = subprocess.run(
                comando,
                stdout=archivo,
                stderr=subprocess.PIPE,
                text=True
            )

        if resultado.returncode != 0:
            raise RuntimeError(resultado.stderr)

        return str(ruta_backup)

    def restaurar_copia_seguridad(self, ruta_sql):
        if not ruta_sql or not os.path.exists(ruta_sql):
            raise FileNotFoundError("No se encontró el archivo de copia de seguridad.")

        mysql = self._buscar_ejecutable_mysql("mysql")

        comando = [
            mysql,
            f"--host={self._host}",
            f"--user={self._user}",
            f"--password={self._password}"
        ]

        with open(ruta_sql, "r", encoding="utf-8") as archivo:
            resultado = subprocess.run(
                comando,
                stdin=archivo,
                stderr=subprocess.PIPE,
                text=True
            )

        if resultado.returncode != 0:
            raise RuntimeError(resultado.stderr)

        return True