from src.modelo.dao.DaoJDBCBase import DaoJDBCBase
from src.modelo.VO.SalarioVO import SalarioVO
from src.modelo.VO.HistorialInformeVO import HistorialInformeVO
from src.modelo.VO.GestionEconomicaVO import GestionEconomicaVO
from src.modelo.VO.BalanceMensualVO import BalanceMensualVO


class InformeConsultasDaoJDBC(DaoJDBCBase):

    SQL_GENERAR_INFORME = """
            INSERT INTO informe (id_contable, tipo_informe, fecha_generacion)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """

    SQL_INFORME_SALARIOS = """
            SELECT u.nombre, r.nombre_rol, e.salario
            FROM empleados e
            JOIN usuarios u ON e.id_empleado = u.id_usuario
            JOIN roles r ON u.id_rol = r.id_rol
            ORDER BY e.salario DESC
        """

    SQL_NUM_INFORMES_MES = """
            SELECT COUNT(*)
            FROM informe
            WHERE YEAR(fecha_generacion) = YEAR(CURRENT_DATE)
              AND MONTH(fecha_generacion) = MONTH(CURRENT_DATE)
        """

    SQL_HISTORIAL_INFORMES = """
            SELECT i.id_informe,
                   u.nombre AS contable,
                   i.tipo_informe,
                   DATE(i.fecha_generacion) AS fecha
            FROM informe i
            INNER JOIN usuarios u ON i.id_contable = u.id_usuario
            ORDER BY i.fecha_generacion DESC
        """

    SQL_BALANCE_MENSUAL = """
        SELECT YEAR(fecha_pago) AS anio,
            MONTH(fecha_pago) AS mes,
            COALESCE(SUM(importe), 0) AS ingresos
        FROM pago
        GROUP BY YEAR(fecha_pago), MONTH(fecha_pago)
        ORDER BY anio DESC, mes DESC
    """

    SQL_INFORMES_USUARIO = """
            SELECT COUNT(*)
            FROM informe
            WHERE id_contable = ?
        """

    def generar_informe(self, id_contable: int, tipo: str):
        return self.ejecutar(self.SQL_GENERAR_INFORME, (id_contable, tipo))

    def informe_salarios(self):
        filas = self.consultar(self.SQL_INFORME_SALARIOS)
        return [SalarioVO(f[0], f[1], f[2]) for f in filas]

    def num_informes_mes_contable(self):
        datos = self.consultar(self.SQL_NUM_INFORMES_MES)
        return datos[0][0] if datos else 0

    def historial_informes_contable(self):
        filas = self.consultar(self.SQL_HISTORIAL_INFORMES)
        return [HistorialInformeVO(f[0], f[1], f[2], f[3]) for f in filas]

    def informe_balance_mensual_contable(self, gasto_mensual):
        ingresos_mensuales = self.consultar(self.SQL_BALANCE_MENSUAL)
        resultado = []
        for fila in ingresos_mensuales:
            anio = fila[0]
            mes = fila[1]
            ingresos = fila[2]
            balance = ingresos - gasto_mensual
            resultado.append(BalanceMensualVO(
                anio, mes,
                f"{float(ingresos):.2f} €",
                f"{float(gasto_mensual):.2f} €",
                f"{float(balance):.2f} €"
            ))
        return resultado

    def informe_gestion_economica_contable(self, ingresos, gastos, balance, pendiente, tarifas_activas, nominas):
        return [
            GestionEconomicaVO("Ingresos abonados", f"{float(ingresos):.2f} €"),
            GestionEconomicaVO("Gastos / nominas", f"{float(gastos):.2f} €"),
            GestionEconomicaVO("Balance", f"{float(balance):.2f} €"),
            GestionEconomicaVO("Pagos pendientes", f"{float(pendiente):.2f} €"),
            GestionEconomicaVO("Tarifas activas", str(tarifas_activas)),
            GestionEconomicaVO("Total nominas", f"{float(nominas):.2f} €"),
        ]

    def contable_informes_generados_usuario(self, id_contable):
        datos = self.consultar(self.SQL_INFORMES_USUARIO, (id_contable,))
        return datos[0][0] if datos else 0