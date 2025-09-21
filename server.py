import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

# Aquí guardaremos los resultados de los clientes
resultados = {}  # {addr: resultado}


def manejar_cliente(conn, addr, tarea):
    """
    Función que se ejecuta en un hilo por cada cliente conectado.
    1. Envía la tarea al cliente.
    2. Recibe el resultado.
    3. Lo guarda en el diccionario resultados.
    """
    print(f"[NUEVA CONEXIÓN] {addr} conectado.")
    try:
        # 1. Enviar la tarea al cliente
        conn.sendall(tarea.encode("utf-8"))

        # 2. Esperar el resultado del cliente
        resultado = conn.recv(1024).decode("utf-8")
        resultados[addr] = resultado
        print(f"[RESULTADO] {addr}: {resultado}")
    except:
        print(f"[ERROR] con {addr}")
    finally:
        conn.close()


def iniciar_servidor():
    """
    Inicia el servidor en localhost:65432
    y asigna la misma tarea a todos los clientes que se conecten.
    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[ESCUCHANDO] Servidor en {HOST}:{PORT}")

    # Ejemplo: tarea que recibirán los clientes
    tarea = "2 + 2"

    while True:
        conn, addr = servidor.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr, tarea))
        hilo.start()


if __name__ == "__main__":
    iniciar_servidor()

