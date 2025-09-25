from .app_context import AppContext
from src.processing.base_strategy import ProcesoStrategy

class ProcesoFactory:
    def __init__(self):
        self._strategies = {}

    def registrar_estrategia(self, nombre: str, clase_estrategia, clase_config):
        self._strategies[nombre] = (clase_estrategia, clase_config)

    def crear(self, tipo_proceso: str, contexto: AppContext) -> ProcesoStrategy:
        if tipo_proceso not in self._strategies:
            raise ValueError(f"Tipo de proceso '{tipo_proceso}' no es válido.")

        clase_estrategia, clase_config = self._strategies[tipo_proceso]
        
        config_dict = contexto.configuracion.get(tipo_proceso, {}) 
        config_obj = clase_config(**config_dict)

        return clase_estrategia(config=config_obj)