import threading
import queue
import pyttsx3

class TTSEngine:
    def __init__(self):
        self.queue = queue.Queue()
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 1.0)
            self.available = True
        except Exception as e:
            print(f"[TTS] Error al inicializar pyttsx3: {e}")
            self.available = False

        self.running = True
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def _worker(self):
        while self.running:
            try:
                text = self.queue.get(timeout=0.5)
                if self.available:
                    self.engine.say(text)
                    self.engine.runAndWait()
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[TTS Error en worker] {e}")

    def speak(self, text: str):
        self.queue.put(text)
        print(f"[TTS] Mensaje agregado a la cola. Cola actual: {self.queue.qsize()}")

    def stop(self):
        self.running = False
        self.thread.join(timeout=2)
