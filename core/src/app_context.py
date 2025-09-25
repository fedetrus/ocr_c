from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class AppContext:
    directorio_actual: str | None = None
    paths_archivos: List[str] = field(default_factory=list)
    
    configuracion: Dict[str, Any] = field(default_factory=dict)