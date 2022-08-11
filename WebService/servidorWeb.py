# 
#       Autora: Giovanna Pavani Martelli
#       Atividade II: Servidor web
#
# servidor de pagina web -> apenas na porta 81

import struct
import socket
import sys
import _thread

def get_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def on_new_client(cliSocket, addr):
    param = ''

    while True:
        msg = cliSocket.recv(2048)

        if msg:
            print('Recebido solicitacao de ' + str(addr) +'\n '+ msg.decode()+ '\n')
            param = msg.decode().split()[1]
            break
        else:
            break

    if param == "/":
         cliSocket.send(abrir_arquivo("home.html").encode())   
    elif param == "/arquivo":
         cliSocket.send(abrir_arquivo("arquivo.txt").encode())   
    elif param == "/icone":
         cliSocket.send(abrir_arquivo("icone.txt").encode())   
    else:
         cliSocket.send(not_Found('Página não encontrada').encode())   

    cliSocket.close()

def not_Found(msg):
    _msg = (
        'HTTP/1.1 404 Not Found\r\n'
        'Date : Sun, 18 Oct 2021 10:00:00 GMT\r\n'
        'Server: TI502\r\n'
        'Content-Type: text/html; charset=iso-8859-1\r\n'
        'Connection: close\r\n'
        '\r\n'
        '<html><head><title>Pagina do panico</title></head>'
        '<body><H1>'+msg+'</H1></body></html>\r\n'
    )
    return _msg

def abrir_arquivo(filename):
    f = open(filename, 'r')
    texto = f.read(2048)

    _msg = (
        'HTTP/1.1 200 OK\r\n'
        'Date : Sun, 18 Oct 2021 10:00:00 GMT\r\n'
        'Server: TI502\r\n'
        'Content-Type: text/html; charset=iso-8859-1\r\n'
        'Connection: close\r\n'
        '\r\n'
        ''+texto+'\r\n'
    )

    f.close
    return _msg

https = get_ip()
hport = 81

sockWeb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sockWeb.bind((https,hport))
    print('\nEscutando em '+ get_ip() + ':' + str(hport)+'\n')
except:
    sockWeb.bind(('',hport))

sockWeb.listen(1)

while True:
    sockClient, addr = sockWeb.accept()
    _thread.start_new_thread(on_new_client, (sockClient, addr))

sockWeb.close()