from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ResultadoOperacion:
    exito: bool
    mensaje: str

class ProcesoStrategy(ABC):
    @abstractmethod
    def ejecutar(self, path_entrada: str, path_salida: str) -> ResultadoOperacion:
        pass