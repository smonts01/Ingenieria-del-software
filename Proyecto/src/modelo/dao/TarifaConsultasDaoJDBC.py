from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
from src.modelo.VO.TarifaEconomicaVO import TarifaEconomicaVO


class TarifaConsultasDaoJDBC(DaoJDBCBase):

    SQL_CONTAR_CLIENTE = """
        SELECT COUNT(*)
        FROM cliente_tarifa ct
        JOIN tarifa t ON ct.id_tarifa = t.id_tarifa
        WHERE LOWER(t.nombre) LIKE ? 
          AND ct.estado = 'activa'
    """

    SQL_TARIFAS_ACTIVAS = """
        SELECT COUNT(*)
        FROM tarifa
    """

    SQL_TARIFAS_ECONOMICA = """
        SELECT 
            nombre,
            CONCAT(precio_mensual, ' €') AS precio,
            'Mensual' AS duracion
        FROM tarifa
        ORDER BY precio_mensual ASC
    """

    def contar_clientes_tarifa(self, nombre_tarifa: str):
        t = f"%{nombre_tarifa.lower().strip()}%"
        datos = self.consultar(self.SQL_CONTAR_CLIENTE, (t,))
        return datos[0][0] if datos else 0

    def num_tarifas_activas_contable(self):
        datos = self.consultar(self.SQL_TARIFAS_ACTIVAS)
        return datos[0][0] if datos else 0

    def contable_tarifas_economica(self):
        filas = self.consultar(self.SQL_TARIFAS_ECONOMICA)
        return [TarifaEconomicaVO(f[0], f[1], f[2]) for f in filas]