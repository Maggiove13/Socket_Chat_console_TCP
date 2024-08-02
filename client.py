import socket
import threading

SERVER = "127.0.0.1"    # Ip del servidor
PORT = 5050             # Puerto de envio, (conectado al servidor)
ADDR = (SERVER, PORT)   # Direccion completa del servidor
HEADER = 64 
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
BUFFER_SIZE = 1024

# Creamos el socket del cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Funcion para enviar mensajes
def send(msg):
    message = msg.encode(FORMAT) # codificamos a un formato "UTF-8"
    msg_length = len(message) # Calculamos cuántos bytes tiene el mensaje.
    send_length = str(msg_length).encode(FORMAT) # Convertimos la longitud del mensaje en un string y luego lo codificamos a bytes.
    # Esto es para que el servidor pueda saber cuántos bytes debe esperar para el mensaje.
    
    send_length += b' ' * (HEADER - len(send_length)) # El encabezado debe tener un tamaño fijo 64bytes en este caso
    client.send(send_length) # mandamos el tmaño
    client.send(message) # mandamos el mensaje

# Funcion para recibir mensajes del servidr y procesarlos
def receive_messages():
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode(FORMAT)
            if message == "@username":
                send(username)
            else:
                print(message)
        except Exception as e:# El bloque except capturará esa excepción y la variable e contendrá una descripción del error
            print(f"An error occurred: {e}")  
            client.close() # Imprimimos e "error" para ver que tipo de error ocurrió.
            break 

def write_messages():
    while True:
        message = input('')
        if message.lower() == "desconectar":
            send(DISCONNECT_MESSAGE)
            client.close()
            break
        send(message)

username = input("Enter your username: ")

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()
