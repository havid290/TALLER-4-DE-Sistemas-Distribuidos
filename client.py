import socket

HOST = "127.0.0.1"
PORT = 65432

# 1. Conectarse al servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

# 2. Recibir la tarea del servidor
tarea = cliente.recv(1024).decode("utf-8")
print(f"[TAREA RECIBIDA] {tarea}")

# 3. Procesar la tarea (ejemplo: resolver usando eval)
try:
    resultado = str(eval(tarea))  #  Ojo: eval solo para pruebas, no en producción según chat gpt 
except Exception as e:
    resultado = f"Error: {e}"

# 4. Enviar el resultado al servidor
cliente.sendall(resultado.encode("utf-8"))

# 5. Cerrar la conexión
cliente.close()

