import os
import ocrmypdf
import logging
from .base_strategy import ProcesoStrategy, ResultadoOperacion
from ..utils import PdfTools
from ..configs import OcrConfig

class ProcesoOCR(ProcesoStrategy):
    def __init__(self, config: OcrConfig):
        self.config = config

    def ejecutar(self, path_entrada: str, path_salida: str) -> ResultadoOperacion:
        try:
            directorio_destino = os.path.dirname(path_salida)
            nombre_base_archivo = os.path.basename(path_salida)
            path_temporal = os.path.join(directorio_destino, "temp_" + nombre_base_archivo)
            
            path_limpio = PdfTools.eliminar_metadata(path_entrada, path_temporal)
            
            logging.getLogger("ocrmypdf").setLevel(logging.ERROR)

            ocrmypdf.ocr(
                path_limpio, 
                path_salida, 
                output_type=self.config.tipo_salida,
                lang=self.config.idioma, 
                force_ocr=self.config.forzar_ocr, 
                progress_bar=False
            )

            if os.path.exists(path_temporal):
                os.remove(path_temporal)
            
            return ResultadoOperacion(exito=True, mensaje=f"OK: {nombre_base_archivo}")

        except Exception as e:
            return ResultadoOperacion(exito=False, mensaje=f"ERROR en {os.path.basename(path_entrada)}: {e}")