import os
from pikepdf import Pdf

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def listar_archivos(path_directorio: str) -> list[str]:
    if not os.path.isdir(path_directorio):
        return []
    
    lista_completa = []
    # os.walk() recorre el árbol de directorios de arriba hacia abajo.
    for dirpath, dirnames, filenames in os.walk(path_directorio):
        for archivo in filenames:
            # Construimos la ruta completa del archivo.
            ruta_completa = os.path.join(dirpath, archivo)
            # Obtenemos la ruta relativa al directorio inicial.
            ruta_relativa = os.path.relpath(ruta_completa, path_directorio)
            lista_completa.append(ruta_relativa)
            
    return lista_completa
    
class PdfTools:
    @staticmethod
    def eliminar_metadata(path_entrada: str, path_salida: str) -> str:
        try:
            with Pdf.open(path_entrada) as pdf:
                # Crear un nuevo PDF en blanco y copiar las páginas
                # es la forma más segura de eliminar toda la metadata.
                pdf_nuevo = Pdf.new()
                pdf_nuevo.pages.extend(pdf.pages)
                pdf_nuevo.save(path_salida)
            return path_salida
        except Exception as e:
            # Si falla, es mejor propagar el error para que el proceso que lo usa se detenga.
            raise IOError(f"No se pudo limpiar la metadata de {os.path.basename(path_entrada)}: {e}")