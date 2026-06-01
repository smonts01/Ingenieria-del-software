from src.modelo.dao.DaoJDBCBase import DaoJDBCBase


class TarifaConsultasDaoJDBC(DaoJDBCBase):

    def contar_clientes_tarifa(self, nombre_tarifa: str):
        t = f"%{nombre_tarifa.lower().strip()}%"
        datos = self.consultar("""
            SELECT COUNT(*) FROM cliente_tarifa ct
            JOIN tarifa t ON ct.id_tarifa = t.id_tarifa
            WHERE LOWER(t.nombre) LIKE ? AND ct.estado = 'activa'
        """, (t,))
        return datos[0][0] if datos else 0

    def num_tarifas_activas_contable(self):
        datos = self.consultar("""
            SELECT COUNT(*)
            FROM tarifa
            WHERE fecha_fin IS NULL OR fecha_fin >= CURRENT_DATE
        """)
        return datos[0][0] if datos else 0

    def contable_tarifas_economica(self):
        return self.consultar("""
            SELECT nombre,
                   CONCAT(precio_mensual, ' €') AS precio,
                   'Mensual' AS duracion
            FROM tarifa
            WHERE fecha_fin IS NULL OR fecha_fin >= CURRENT_DATE
            ORDER BY precio_mensual ASC
        """)
