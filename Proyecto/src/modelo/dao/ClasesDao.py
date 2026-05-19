from src.modelo.VO.ClaseVO import ClaseVO

class ClasesDao:
    def select(self) -> list[ClaseVO]:
        """Recupera todas las clases"""
        raise NotImplmentedError ("Método select() no implmentado")
    
    def selectById(self, id_clase: int) -> ClaseVO:
        """Recupera una clase por su ID"""
        raise NotImplemnetedError("Método selectById() no implementado")
    
    def selectByEntrenador (self, id_entrenador: int) -> list[ClaseVO]:
        """Recupera todas las clases de un entrenador"""
        raise NotImplemnetedError("Método selectByEntrenador() no implementado")
    
    def selectBySala(self, id_sala:int) -> list[ClaseVO]:
        """Recupera todas las clases de una sala"""
        raise NotImplemnetedError("Método selectBySala() no implementado")
    
    def insert(self, clase: ClaseVO) -> int:
        """Inserta una nueva clase."""
        raise NotImplementedError("Método insert() no implementado")
 
    def update(self, clase: ClaseVO) -> int:
        """Actualiza los datos de una clase."""
        raise NotImplementedError("Método update() no implementado")
 
    def delete(self, id_clase: int) -> int:
        """Elimina una clase por su ID."""
        raise NotImplementedError("Método delete() no implementado")