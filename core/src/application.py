import os
from .app_context import AppContext
from src.processing.ocr_strategy import ProcesoOCR
from src.ui.menus import MenuPrincipalUI, MenuOcrUI, AppView
from .utils import listar_archivos, limpiar_pantalla
from .configs import OcrConfig
from .factory import ProcesoFactory
from dataclasses import asdict

class Application:
    def __init__(self):
        self.contexto = AppContext()
        self._cargar_configuracion_defecto()
        self.view = AppView() 
        self.vistas = {
            'principal': MenuPrincipalUI(),
            'ocr': MenuOcrUI()
        }
        self.vista_actual = self.vistas['principal']
        self.corriendo = True
        self.acciones = {
            'salir': self.salir,
            'volver': self._navegar_a_principal,
            'seleccionar_directorio': self.elegir_directorio,
            'ir_a_ocr': self._navegar_a_ocr,
            'configurar_ocr': self.configurar_ocr,
            'procesar_ocr': lambda: self.ejecutar_proceso('ocr')
        }
        self.factory = ProcesoFactory()
        self._registrar_procesos()

    def _registrar_procesos(self):
        self.factory.registrar_estrategia('ocr', ProcesoOCR, OcrConfig)

    def _cargar_configuracion_defecto(self):
        config_por_defecto = OcrConfig()
        self.contexto.configuracion['ocr'] = asdict(config_por_defecto)

    def run(self):
        while self.corriendo:
            limpiar_pantalla()
            accion = self.vista_actual.mostrar(self.contexto)
            if accion:
                self.manejar_accion(accion)
            else:
                self.salir()
    
    def _navegar_a_principal(self):
        self.vista_actual = self.vistas['principal']

    def _navegar_a_ocr(self):
        self.vista_actual = self.vistas['ocr']

    def manejar_accion(self, accion: str):
        metodo_a_ejecutar = self.acciones.get(accion)
        if metodo_a_ejecutar:
            metodo_a_ejecutar()
        else:
            self.view.mostrar_error(f"Acción '{accion}' no reconocida.")
            self.view.pausar_y_continuar()
        
    def elegir_directorio(self):
        path_seleccionado, error_msg = self.vistas['principal'].solicitar_directorio_procesamiento()
        limpiar_pantalla()
        if error_msg:
            self.view.mostrar_error(error_msg)
        elif path_seleccionado:
            lista_archivos = listar_archivos(path_seleccionado)
            self.contexto.directorio_actual = path_seleccionado
            self.contexto.paths_archivos = lista_archivos
            self.view.mostrar_confirmacion(f"📂 Directorio: {os.path.basename(path_seleccionado)}")
            self.view.mostrar_confirmacion(f"📄 Archivos encontrados: {len(lista_archivos)}")
        self.view.pausar_y_continuar()

    def configurar_ocr(self):
        nuevo_tipo = self.vistas['ocr'].solicitar_tipo_salida()
        if nuevo_tipo:
            self.contexto.configuracion['ocr']['tipo_salida'] = nuevo_tipo
            self.view.pausar_y_continuar()

    def _preparar_proceso(self, tipo_proceso: str) -> tuple | None:
        if not self.contexto.paths_archivos:
            self.view.mostrar_error("⚠️ No hay archivos para procesar.")
            return None
        try:
            strategy = self.factory.crear(tipo_proceso, self.contexto)             
            nombre_carpeta_salida = f"Out_{tipo_proceso.upper()}"
            directorio_base = os.path.dirname(self.contexto.directorio_actual)
            directorio_salida_base = os.path.join(directorio_base, nombre_carpeta_salida)
            return strategy, directorio_salida_base
        except Exception as e:
            self.view.mostrar_error(f"❌ Error al preparar el proceso: {e}")
            return None

    def _ejecutar_bucle_proceso(self, strategy, directorio_salida_base) -> tuple[int, int]:
        errores = 0
        exitos = 0
        total_archivos = len(self.contexto.paths_archivos)
        
        for idx, ruta_relativa in enumerate(self.contexto.paths_archivos, start=1):
            path_entrada = os.path.join(self.contexto.directorio_actual, ruta_relativa)
            path_salida = os.path.join(directorio_salida_base, ruta_relativa)
            os.makedirs(os.path.dirname(path_salida), exist_ok=True)
            
            self.view.iniciar_progreso_archivo(idx, total_archivos, ruta_relativa)
            resultado = strategy.ejecutar(path_entrada, path_salida)
            self.view.finalizar_progreso_archivo(resultado)
            
            if resultado.exito:
                exitos += 1
            else:
                errores += 1
        return exitos, errores

    def ejecutar_proceso(self, tipo_proceso: str):
        limpiar_pantalla()
        preparacion = self._preparar_proceso(tipo_proceso)
        if not preparacion:
            self.view.pausar_y_continuar()
            return

        strategy, directorio_salida_base = preparacion
        self.view.mostrar_progreso_inicio(tipo_proceso, len(self.contexto.paths_archivos))
        exitos, errores = self._ejecutar_bucle_proceso(strategy, directorio_salida_base)
        self.view.mostrar_resumen_proceso(exitos, errores)
        self.view.pausar_y_continuar()

    def salir(self):
        self.corriendo = False
        limpiar_pantalla()
        self.view.mostrar_despedida()