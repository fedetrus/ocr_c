# ocr_c
# Laboratorio de Procesamiento de PDFs

Una herramienta de línea de comandos (CLI) construida en Python para aplicar procesamiento por lotes a archivos PDF, comenzando con una potente funcionalidad de OCR.

##  Características

- **Selección Interactiva de Directorios:** Menús amigables para elegir la carpeta de trabajo.
- **Procesamiento OCR:** Utiliza `ocrmypdf` para agregar una capa de texto a PDFs de imágenes.
- **Configuración Flexible:** Permite ajustar parámetros como el tipo de salida (PDF/A, PDF estándar).
- **Estructura Extensible:** Diseñado con patrones Strategy y Factory para agregar fácilmente nuevos tipos de procesamiento en el futuro.

##  Tecnologías

- Python 3.10+
- ocrmypdf
- questionary
- pikepdf

##  Prerrequisitos del Sistema (Linux)

Antes de instalar el proyecto, es necesario instalar las dependencias del sistema. Para distribuciones basadas en Debian/Ubuntu, ejecuta:

```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-spa ghostscript

##  Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
    cd tu-repositorio
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

##  Uso

1.  Dentro de `PROCESAMIENTO`, crea subcarpetas para cada lote de archivos (ej. `lote_facturas`, `reportes_cliente_X`).
2.  Coloca tus archivos PDF dentro de esas subcarpetas.
3.  Ejecuta la aplicación y sigue las instrucciones del menú:
    ```bash
    python main.py
    ```


