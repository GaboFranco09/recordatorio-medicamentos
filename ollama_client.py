from ollama import chat, ChatResponse

class OllamaClientWrapper:
    """Usa Ollama si está disponible, de lo contrario devuelve mensaje genérico."""

    def __init__(self):
        self.available = False
        try:
            # Verificamos conexión rápida
            test = chat(model='gemma3', messages=[{'role':'user','content':'Hello'}])
            self.available = True
        except Exception:
            print("[Ollama] No disponible. Se usarán mensajes genéricos.")

    def generar_mensaje(self, nombre, medicamento, dosis, hora=""):
        if self.available:
            try:
                prompt = f"Hola {nombre}, es hora de tomar {dosis} de {medicamento}."
                response: ChatResponse = chat(model='gemma3', messages=[{'role':'user','content': prompt}])
                return response.message.content
            except Exception:
                print("[Ollama] Error generando mensaje: usar mensaje genérico.")
        # Fallback
        return f"Hola {nombre}, es hora de tomar {dosis} de {medicamento}."
