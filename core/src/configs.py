from dataclasses import dataclass

PROCESSING_FOLDER_NAME = 'PROCESAMIENTO'

@dataclass
class BaseConfig:
    """Clase base para futuras configuraciones."""
    pass

@dataclass
class OcrConfig(BaseConfig):
    tipo_salida: str = 'pdfa'
    idioma: str = 'spa'
    forzar_ocr: bool = True
    # dpi: int = 300