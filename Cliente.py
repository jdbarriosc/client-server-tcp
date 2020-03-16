from socket import socket, error
from hashlib import md5
buffer_size = 1024

def main():

    conec = "localhost"
    s = socket()
    s.connect((conec, 6030))
    f = open("recibido", "wb")

    while True:
        print("Listo para recibir archivo...")
        # Enviar notificacion al servidor
        # v = 'L'
        # s.sendall(v.encode('ascii'))

        #Recibir archivo
        try:
            hashrecibido = s.recv(buffer_size)
            input_data = s.recv(buffer_size)
            print("Recibiendo archivo")
            data = input_data
            termino = "Finished".encode()
            f.write(data)
            while data:
                data = s.recv(buffer_size)
                if data == termino:
                    break
                f.write(data)

            f.close()
            print("se terminó de recibir el archivo")
            hash = md5(input_data).hexdigest()
            if hashrecibido.decode() == hash:
                print("Integridad del archivo verificada")
            break

        except error:
            print("Error de lectura.")
            break

    r = 'R'
    s.send(r.encode())
    print("El archivo se ha recibido correctamente.")
    f.close()



if __name__ == "__main__":
    main()