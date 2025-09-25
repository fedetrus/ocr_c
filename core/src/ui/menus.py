import questionary
import os
from ..app_context import AppContext
from src.processing.base_strategy import ResultadoOperacion
from .styles import custom_style
from src.configs import PROCESSING_FOLDER_NAME

class BaseMenuUI:
    def _mostrar_header_comun(self, titulo: str, contexto: AppContext):
        nombre_dir = os.path.basename(contexto.directorio_actual) if contexto.directorio_actual else "⛔ SIN DIRECTORIO"
        print(f"{titulo}")
        print(f"\n📂 Directorio actual: {nombre_dir}")

class MenuPrincipalUI(BaseMenuUI):
    def mostrar(self, contexto: AppContext) -> str | None:
        self._mostrar_header_comun("🧪 Laboratorio de Imágenes", contexto)
        
        print("")

        choices = [
            {"name": "1: 📂 Seleccionar directorio de ARCHIVOS:", "value": "seleccionar_directorio"},
            {"name": "2: 📖 Procesamiento OCR", "value": "ir_a_ocr"},
            {"name": "0: 🚪 Salir", "value": "salir"},
        ]
        return questionary.select("", choices=choices, style=custom_style).ask()

    def solicitar_directorio_procesamiento(self) -> tuple[str | None, str | None]:
        try:
            ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            ruta_procesamiento = os.path.join(ruta_base, PROCESSING_FOLDER_NAME)

            if not os.path.exists(ruta_procesamiento):
                os.makedirs(ruta_procesamiento)

            directorios = [d for d in os.listdir(ruta_procesamiento) if os.path.isdir(os.path.join(ruta_procesamiento, d))]
            if not directorios:
                return None, "🤷 No se encontraron subdirectorios en la carpeta 'PROCESAMIENTO'."

            directorios.append("<< Cancelar >>")
            seleccion = questionary.select("Seleccione el directorio de trabajo:", choices=directorios, style=custom_style).ask()

            if seleccion is None or seleccion == "<< Cancelar >>":
                return None, "❌ Selección de directorio cancelada."

            return os.path.join(ruta_procesamiento, seleccion), None
        except Exception as e:
            return None, f"🚨 Error inesperado al leer los directorios: {e}"

class MenuOcrUI(BaseMenuUI):
    def _formatear_configuracion(self, contexto: AppContext) -> str:
        config = contexto.configuracion.get('ocr', {})
        tipo_salida = config.get('tipo_salida', 'N/A').upper()
        idioma = config.get('idioma', 'N/A').capitalize()

        return f"⚙ Configuración actual: Salida: {tipo_salida}, Idioma: {idioma}"

    def mostrar(self, contexto: AppContext) -> str | None:
        self._mostrar_header_comun("📖 Procesamiento OCR", contexto)
        print(self._formatear_configuracion(contexto))
    
        print("")

        config_actual = contexto.configuracion.get('ocr', {})
        tipo_salida_actual = config_actual.get('tipo_salida', 'N/A').upper()

        choices=[
            {"name": f"1: 🎚️ Cambiar tipo de salida (actual: {tipo_salida_actual})", "value": "configurar_ocr"},
            {"name": "2: ⚙️ Procesar archivos con OCR", "value": "procesar_ocr"},
            {"name": "0: ⬅ Volver al menú principal", "value": "volver"}
        ]
        return questionary.select("", choices=choices, style=custom_style).ask()

    def solicitar_tipo_salida(self) -> str | None:
        choices=[
            {"name": "📑 PDF estándar", "value": "pdf"},
            {"name": "📜 PDFA archivado", "value": "pdfa"}
        ]
        return questionary.select("Seleccione el tipo de salida:", choices=choices, style=custom_style).ask()
    

class AppView:
    def mostrar_error(self, mensaje: str):
        print(mensaje)

    def mostrar_confirmacion(self, mensaje: str):
        print(mensaje)

    def pausar_y_continuar(self):
        input("\nPresione Enter para continuar...")

    def mostrar_progreso_inicio(self, tipo_proceso: str, total_archivos: int):
        print(f"⚙️ Iniciando proceso '{tipo_proceso.upper()}' para {total_archivos} archivo(s)...")

    def iniciar_progreso_archivo(self, idx: int, total: int, ruta: str):
        print(f"  Procesando {idx}/{total}: {ruta}...", end='', flush=True)

    def finalizar_progreso_archivo(self, resultado: ResultadoOperacion):
        if resultado.exito:
            print(" ✅")
        else:
            print(" ❌")
            print(f"    └─> {resultado.mensaje}")

    def mostrar_resumen_proceso(self, exitos: int, errores: int):
        print("\n--- Proceso Finalizado ---")
        print(f"✅ Archivos procesados con éxito: {exitos}")
        if errores:
            print(f"❌ Archivos con errores: {errores}")
        else:
            print(f"✅ Sin errores.")

    def mostrar_despedida(self):
        print("Gracias por usar el laboratorio. ¡👋👋👋!")