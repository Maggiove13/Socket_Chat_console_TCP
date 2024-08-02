import socket # para crear y manejar conexiones de red.
import threading # nos permite manejar múltiples tareas al mismo tiempo.

#1 - Establecer el socket que escucha
HOST = "127.0.0.1"  #Direccion Loopback
PORT = 5050 # Puerto que va a usar el servidor para escuchar 
ADDR = (HOST, PORT) # Esta es la dirección completa del servidor.
HEADER = 64 # bytes ---> Tamaño del encabezado del mensaje
FORMAT = 'utf-8' #  # Formato de codificación de los mensajes || # Seria como el idioma en que enviamos los mensajes.
DISCONNECT_MESSAGE = "DISCONNECT"# Cuando se reciba este mensaje se desconectara el cliente del servidor

# 2 - Instanciar el objeto socket, y crear el socket del punto A.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) # Vinculamos el socket a un PORT y un HOST

# Listas para almacenar clientes y sus nombres de usuario
clients = []
usernames = []

# Función para transmitir mensajes a todos los clientes
def broadcast(message, sender=None):
    """Envía el mensaje a todos los clientes conectados, excepto al remitente."""
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error sending message to {client}: {e}")
                clients.remove(client)

#---> Manejamos las conexiones individuales -- un cliente a un servidor
def handle_client(conn, addr): #Aca se manejará toda la comunicacion entre el cliente y el servidor.
    print(f"[NEW CONNECTION] {addr} connected." )
    
    # Pedir al cliente que envíe su nombre de usuario
    conn.send("@username".encode(FORMAT)) 
    username_length = conn.recv(HEADER).decode(FORMAT) # Espera recibir el tamaño del nombre del cliente.
    
    if username_length: # Verifica si el cliente ha enviado algo.
        try: 
            username_length = int(username_length) 
            username = conn.recv(username_length).decode(FORMAT) # Espera recibir el nombre del jugador.
            usernames.append(username) #  Agrega el nombre del cliente a la lista.
            clients.append(conn) # agrega el cliente a la lista
            print(f"[NEW USER] {username} has joined from {addr}")

            # Notificar a todos los clientes que un nuevo usuario se ha unido
            broadcast(f"ChatBot: {username} joined the chat!".encode(FORMAT), conn) # Le dice a todos los clientes que otro cliente se unió.
            conn.send("Connected to server".encode(FORMAT)) # el servidor le avisa al cliente que está conectado
            broadcast("ChatBot: Si deseas desconectarte, escribe 'desconectar'.".encode(FORMAT))
        except ValueError:
            print(f"[ERROR] Invalid username length received: {username_length}")
            conn.close()
            return # Sale inmediatamente de la función, deteniendo toda la ejecución de la función actual

    connected = True
    while connected: # Mientras el cliente este conectado, entonces se va a repetir esa función
        try:
            message_length= conn.recv(HEADER).decode(FORMAT) # Espera recibir el tamaño del mensaje.
            
            if message_length: #If this is not NONE
                message_length = int(message_length)# Convertiremos ese codigo a integer, que es la cantidad de bytes que vamos a recibir 
                message = conn.recv(message_length).decode(FORMAT) # Recibe el mensaje y se le informa cuantos bytes va a recibir

                
                if message == DISCONNECT_MESSAGE:  # Si el mensaje es desconectar
                    connected = False # Desconecta al usuario
                    broadcast(f"ChatBot: {username} disconnected".encode(FORMAT), conn) #El servidor informa a todos los clientes que una de los users se desconecto
                    print(f"The user [{username}] has decided  disconnected")
                else:
                    broadcast(f"[{username}] {message}".encode(FORMAT), conn) 
                    print(f"[{username}] {message}") # Mostrar en pantalla la direccion(PORT, y HOST) y el mensaje
        except:
            break
    
    
    if conn in clients:  #  Verifica si la conexión del cliente está en la lista de clientes.
        index = clients.index(conn)
        clients.remove(conn)
        conn.close()
        username = usernames[index]
        usernames.remove(username)
        print(f"The user [{username}] has disconnected")


#Esta funcion permitira al servidor a escuchar las conexiones. Manejar esas conexiones y pasarlas a "handle_client"
def start(): 
    server.listen() 
    print(f"[LISTENING] Server is listening on {HOST}") 
    while True: 
        conn, addr = server.accept() #Se bloquea esperando una conexion y luego almacena el addres de esa conexion
        thread = threading.Thread(target= handle_client, args=(conn, addr))
        thread.start() # Para iniciar el hilo y manejar la conexion.
        
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}") # Muestra cuantas conexiones activas hay

print("[STARTING] server is starting...")
start() #Llamamos a la función de start para iniciar el servidor



