from src.modelo.VO.ClaseVO import ClaseVO

class ClasesDao:
    def select(self) -> list[ClaseVO]:
        """Recupera todas las clases"""
        raise NotImplmentedError ("Método select() no implmentado")
    
    def selectById(self, id_clase: int) -> ClaseVO:
        """Recupera una clase por su ID"""
        raise NotImplemnetedError("Método selectById() no implementado")