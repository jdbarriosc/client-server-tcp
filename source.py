from socket import socket, error
from threading import *
from hashlib import md5
import time
buffer_size = 1024
clientes = []
semaforo = Semaphore(1)
class Client(Thread):
    def __init__(self, conn, addr, file, hash, id):
        # Inicializar clase padre.
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.file = file
        self.hash = hash
        self.id= id
        self.estado =False
    def run(self):
        while True:
            try:
                # enviar datos del cliente.
                print("enviando archivo al cliente: " + str(self.id))
                self.conn.send(self.hash.encode())
                self.enviarArchivo()
                if self.conn.recv(1024):
                    self.estado = True
                break
            except error:
                print("[%s] Error de envío." % self.name)
                break
 ##########

    def enviarArchivo(self):
        cont = self.file.read(buffer_size)
        while(cont):
            self.conn.send(cont)
            cont = self.file.read(buffer_size)
        self.conn.send("Finished".encode())
        self.file.close()
        print("se terminó de enviar el archivo")


#################
def main():
    numrecibidos = 0
    s = socket()
    s.bind(("0.0.0.0", 6030))
    s.listen(25)
    contador = 0
    #Inicia el servidor
    print("Servidor conectado")
    #solicita cantidad de clientes a conectar
    print("Digite la cantidad de clientes que desea que se conecten")
    while True:
        strClientes= input()
        numClientes = int(strClientes)
        if(numClientes > 25 or numClientes < 0):
             print("Por favor ingrese un número de clientes valido")
        else: break
    #solicita el archivo que desea enviar
    rutaArchivo: ""
    print("Digite '1' para enviar el archivo multimedia o '2' para enviar el archivo otro:")
    inputarchi=int(input())
    if(inputarchi==1):
        rutaArchivo = "./archivos/1.mp4"
    elif(inputarchi == 2):
        rutaArchivo = "./archivos/2.jpg"
    else:
        print("Por favor digite un valor válido")

    #Lee el archivo y calcula el hash de los primero caracteres
    file = open(rutaArchivo, 'rb')
    contenido = file.read(buffer_size)
    hash = md5(contenido).hexdigest()

    #Espera que se conecten los clientes que se solicitaron anteriormente
    while len(clientes) < numClientes :
        print("Esperando conexiones...")
        conn, addr = s.accept()
        c = Client(conn,addr,file,hash, len(clientes))
        clientes.append(c)

    tiempo_inicial = time.time()
    #una vez conectados, inicia todos los threads de clientes
    for client in clientes:
       client.start()

    while True:
        for client in clientes:
            if client.estado:
                contador += 1
        if contador == numClientes:
            break


    tiempo_final = time.time()
    tiempo_total = tiempo_final - tiempo_inicial

    print(tiempo_total)




if __name__ == "__main__":
    main()