import multiprocessing
import time
import random

# --- Worker (proceso hijo) ---
def worker(cola_tareas, cola_resultados):
    """
    Función que ejecuta cada worker:
    - Toma tareas de la cola de tareas
    - Procesa la tarea
    - Devuelve el resultado en la cola de resultados
    """
    for tarea in iter(cola_tareas.get, "FIN"):  # Sale cuando recibe "FIN"
        print(f"[Worker {multiprocessing.current_process().name}] Procesando tarea: {tarea}")
        time.sleep(random.uniform(0.5, 1.5))  # Simula trabajo
        resultado = f"Tarea {tarea} completada"
        cola_resultados.put(resultado)

    print(f"[Worker {multiprocessing.current_process().name}] Finalizando...")

# --- Proceso principal (padre) ---
if __name__ == "__main__":
    num_workers = 3

    # Colas compartidas
    cola_tareas = multiprocessing.Queue()
    cola_resultados = multiprocessing.Queue()

    # Crear y arrancar procesos workers
    workers = []
    for i in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(cola_tareas, cola_resultados))
        p.start()
        workers.append(p)

    # Enviar tareas a la cola
    tareas = [f"T{i}" for i in range(1, 11)]  # 10 tareas
    for t in tareas:
        cola_tareas.put(t)

    # Enviar señal de finalización ("FIN") a cada worker
    for _ in range(num_workers):
        cola_tareas.put("FIN")

    # Recoger resultados
    for _ in tareas:
        resultado = cola_resultados.get()
        print(f"[Padre] Resultado recibido: {resultado}")

    # Esperar a que todos los workers terminen
    for p in workers:
        p.join()

    print("[Padre] Todas las tareas han finalizado.")
