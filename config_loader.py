import json

def cargar_medicamentos(ruta="config.json"):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Config] Error cargando {ruta}: {e}")
        return {}
