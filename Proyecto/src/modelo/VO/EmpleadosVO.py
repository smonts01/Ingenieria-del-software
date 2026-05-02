class EmpleadoVO:
    def __init__(self, id_empleado, salario):
        self._id_empleado = id_empleado
        self._salario = salario
        
    @property
    def id_empleado(self):
        return self._id_empleado
    
    @property
    def salario(self):
        return self._salario