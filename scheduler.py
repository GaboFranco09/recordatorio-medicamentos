import time
import schedule
import datetime as dt
from tts_engine import TTSEngine
from config_loader import cargar_medicamentos
from ollama_client import OllamaClientWrapper

tts = TTSEngine()
ollama = OllamaClientWrapper()

def now_ts():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def make_job(med):
    nombre = med.get("nombre_adulto") or "Usuario"
    medicamento = med.get("nombre") or "Medicamento desconocido"
    dosis = med.get("dosis") or "dosis no especificada"
    hora = med.get("hora") or ""

    def job():
        try:
            mensaje = ollama.generar_mensaje(nombre, medicamento, dosis, hora)
            print(f"⏰ [{now_ts()}] {mensaje}")
            tts.speak(mensaje)
        except Exception as e:
            print(f"[Error] Exception en job para {medicamento}: {e}")

    return job

def schedule_med(med):
    nombre = med.get("nombre") or "Medicamento desconocido"
    scheduled = False

    if "intervalo_segundos" in med:
        schedule.every(int(med["intervalo_segundos"])).seconds.do(make_job(med))
        print(f"[OK] Programado {nombre} cada {med['intervalo_segundos']} segundos.")
        scheduled = True
    if "intervalo_minutos" in med:
        schedule.every(int(med["intervalo_minutos"])).minutes.do(make_job(med))
        print(f"[OK] Programado {nombre} cada {med['intervalo_minutos']} minutos.")
        scheduled = True
    if "intervalo_horas" in med:
        schedule.every(int(med["intervalo_horas"])).hours.do(make_job(med))
        print(f"[OK] Programado {nombre} cada {med['intervalo_horas']} horas.")
        scheduled = True
    if "hora" in med:
        schedule.every().day.at(med["hora"]).do(make_job(med))
        print(f"[OK] Programado {nombre} diariamente a las {med['hora']}.")
        scheduled = True
    if "horas" in med:
        for hval in med["horas"]:
            schedule.every().day.at(hval).do(make_job(med))
            print(f"[OK] Programado {nombre} diariamente a las {hval}.")
            scheduled = True

    if not scheduled:
        print(f"[⚠️] El medicamento '{nombre}' no se programó: no tiene intervalos válidos.")

def load_and_schedule(ruta=None):
    meds = cargar_medicamentos(ruta) if ruta else cargar_medicamentos()
    if isinstance(meds, dict) and "medicamentos" in meds:
        meds = meds["medicamentos"]

    if not isinstance(meds, list) or not meds:
        print("[Info] No hay medicamentos en config.json.")
        return

    for med in meds:
        schedule_med(med)

if __name__ == "__main__":
    print("⏰ Iniciando scheduler...")
    load_and_schedule()
    print("✅ Recordatorio de medicamentos iniciado. Presiona Ctrl+C para salir.\n")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Programa detenido por el usuario.")
        tts.stop()
