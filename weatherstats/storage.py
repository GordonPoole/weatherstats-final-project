import json
from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True)
class JSONStorage:
    indent: int = 2

    def save_obj(self, obj: dict, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=self.indent)
        return path