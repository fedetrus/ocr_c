from questionary import Style

custom_style = Style([
    ('qmark', 'fg:#2a9d8f bold'),        # El signo de pregunta "?" color cyan
    ('question', 'bold'),                 # La pregunta en negrita
    ('answer', 'fg:#ff9d00 bold'),         # La respuesta seleccionada después
    ('pointer', 'fg:#2a9d8f bold'),        # La flecha "➤" cyan y bold
    ('highlighted', 'fg:#2a9d8f bold'),    # El texto de la opción seleccionada
    ('selected', 'fg:#2a9d8f bold'),       # Cuando ya está seleccionada
    ('separator', 'fg:#6C6C6C'),            # Separadores de listas
    ('instruction', ''),                  # Las instrucciones
    ('text', ''),                         # Texto normal 
])