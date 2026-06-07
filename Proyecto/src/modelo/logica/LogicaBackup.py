import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from src.modelo.conexion.Conexion import Conexion


class LogicaBackup:
    """
    Lógica de negocio para crear y restaurar copias de seguridad.
    Utiliza los ejecutables mysqldump y mysql del servidor MySQL instalado
    en el ordenador. Los backups se guardan en la carpeta 'backups/' del
    directorio raíz del proyecto con el formato: backup_<nombre_bd>_<fecha_hora>.sql
    """

    def __init__(self):
        # Obtener los parámetros de conexión desde Conexion para usarlos
        # en los comandos de mysqldump y mysql
        conexion = Conexion()
        self._host     = conexion._host
        self._database = conexion._database
        self._user     = conexion._user
        self._password = conexion._password
        try:
            conexion.closeConnection()
        except Exception:
            pass



    def _buscar_ejecutable_mysql(self, nombre: str) -> str:
        """Localiza el ejecutable mysqldump o mysql en el sistema.

        Primero busca en el PATH del sistema. Si no lo encuentra,
        prueba las rutas de instalación más comunes.

        Lanza FileNotFoundError si no lo encuentra en ninguna ubicación.
        """
        # Intentar localizar el ejecutable en el PATH del sistema
        ruta = shutil.which(nombre)
        if ruta:
            return ruta

        # Si no está en el PATH, buscar en las rutas de instalación típicas de MySQL
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

    # Operaciones

    def crear_copia_seguridad(self) -> str:
        """
        Crea la carpeta 'backups/' si no existe, y guarda el archivo SQL
        con la fecha y hora actuales en el nombre.

        Devuelve la ruta del archivo generado como string.
        Lanza RuntimeError si mysqldump devuelve un error.
        """
        # Crear la carpeta de backups si no existe
        carpeta_backups = Path("backups")
        carpeta_backups.mkdir(exist_ok=True)

        # Generar el nombre del archivo con la fecha y hora actuales
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"backup_{self._database}_{fecha}.sql"
        ruta_backup = carpeta_backups / nombre_archivo

        mysqldump = self._buscar_ejecutable_mysql("mysqldump")

        # Construir el comando mysqldump con rutinas, triggers y eventos
        comando = [
            mysqldump,
            f"--host={self._host}",
            f"--user={self._user}",
            f"--password={self._password}",
            "--databases", self._database,
            "--routines",
            "--triggers",
            "--events",
        ]

        # Ejecutar mysqldump redirigiendo la salida al archivo SQL
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

    def restaurar_copia_seguridad(self, ruta_sql: str) -> bool:
        """Restaura la base de datos a partir de un archivo SQL de backup.

        Lee el archivo SQL indicado y lo ejecuta en el servidor MySQL.

        Devuelve True si la restauración fue correcta.
        Lanza FileNotFoundError si el archivo no existe.
        Lanza RuntimeError si mysql devuelve un error.
        """
        # Verificar que el archivo de backup existe antes de continuar
        if not ruta_sql or not os.path.exists(ruta_sql):
            raise FileNotFoundError("No se encontró el archivo de copia de seguridad.")

        mysql = self._buscar_ejecutable_mysql("mysql")

        # Construir el comando mysql 
        comando = [
            mysql,
            f"--host={self._host}",
            f"--user={self._user}",
            f"--password={self._password}",
        ]

        # Ejecutar mysql leyendo el archivo SQL
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