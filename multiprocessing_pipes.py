import multiprocessing

def trabajador(conn, tarea_id):
    """
    Proceso hijo que recibe tareas desde el padre y devuelve resultados.
    """
    while True:
        tarea = conn.recv()  # Espera recibir una tarea
        if tarea == "FIN":   # Señal para terminar
            print(f"[Proceso {tarea_id}] Finalizando...")
            break
        print(f"[Proceso {tarea_id}] Recibió tarea: {tarea}")
        
        # Aquí simulas el procesamiento de la tarea
        resultado = f"Resultado de {tarea} en proceso {tarea_id}"
        
        # Enviar el resultado de vuelta al padre
        conn.send(resultado)


if __name__ == "__main__":
    procesos = []
    conexiones = []
    num_procesos = 3  # Número de procesos hijos

    # Crear procesos hijos con pipes
    for i in range(num_procesos):
        padre_conn, hijo_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(target=trabajador, args=(hijo_conn, i))
        procesos.append(p)
        conexiones.append(padre_conn)
        p.start()

    # Enviar tareas a cada proceso
    for i, conn in enumerate(conexiones):
        tarea = f"Tarea {i+1}"
        print(f"[Padre] Enviando: {tarea}")
        conn.send(tarea)

    # Recibir resultados de cada proceso
    for conn in conexiones:
        resultado = conn.recv()
        print("[Padre] Recibió:", resultado)

    # Enviar señal de finalización
    for conn in conexiones:
        conn.send("FIN")

    # Esperar que todos los procesos terminen
    for p in procesos:
        p.join()

    print("[Padre] Todos los procesos han finalizado.")
