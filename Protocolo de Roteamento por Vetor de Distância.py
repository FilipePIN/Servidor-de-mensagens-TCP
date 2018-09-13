#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import socket
import sys
import time
import threading

typemsg = 'type'
updatemsg = 'update'
tracemsg = 'trace'
datamsg = 'data'
sourcemsg = 'source'
destinationmsg = 'destination'
payloadmsg = 'payload'
distancesmsg = 'distances'
hopsmsg = 'hops'
AddrDispAtual = "127.0.1.1"
tempo_para_expirar = 60
disp_diret_conect = []

'''
msg2 = { #Exemplo de msg de update
    "type": "update",
    "source": "127.0.3.1",
    "destination": "127.0.1.10",
    "distances": {
    "127.0.3.1": 100,
    "127.0.1.1": 20,
    "127.0.1.2": 10,
    "127.0.1.3": 10
    }
}

msg2 = { #Exemplo de msg de trace
"type": "trace",
"source": "127.0.1.1",
"destination": "127.0.1.2",
"hops": ["127.0.1.1", "127.0.1.5", "127.0.1.2"]
}


msg2 = { #Exemplo de msg de dados
"type": "data",
"source": "127.0.1.2",
"destination": "127.0.1.1",
"payload": "{\"destination\": \"127.0.1.2\", \"type\": \"trace\", ...}"
}



msg = { #Exemplo de msg de trace
"type": "trace",
"source": "127.0.1.1",
"destination": "127.0.1.2",
"hops": ["127.0.1.1", "127.0.1.5", "127.0.1.2"]
}

def TabelaRoteamento():

    Destino = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
    Distancia = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
    Proximo = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
    return Destino, Distancia, Proximo'''



TabelaRoteamentoDist = {
    AddrDispAtual: 0
}

TabelaRoteamentoProx = {

}

#TimeStart = time.time()
Time_atual = time.time()


TabelaRoteamentoTime= {
    AddrDispAtual: time.time()
}

'''

TabelaRoteamentoDist = {
    "127.0.1.1": 50,
    "127.0.1.2": 50,
    "127.0.1.3": 50,
    "127.0.1.4": 50,
    "127.0.1.5": 50,
    "127.0.1.6": 50,
    "127.0.1.7": 50,
    "127.0.1.8": 50,
    "127.0.1.9": 50,
    "127.0.1.10": 50
}

TabelaRoteamentoProx = {
    "127.0.1.1": "127.0.1.1",
    "127.0.1.2": "127.0.1.1",
    "127.0.1.3": "127.0.1.1",
    "127.0.1.4": "127.0.1.1",
    "127.0.1.5": "127.0.1.1",
    "127.0.1.6": "127.0.1.1",
    "127.0.1.7": "127.0.1.1",
    "127.0.1.8": "127.0.1.1",
    "127.0.1.9": "127.0.1.1",
    "127.0.1.10": "127.0.1.1"
}

#TimeStart = time.time()
Time_atual = time.time()


TabelaRoteamentoTime= {
    "127.0.1.1": Time_atual,
    "127.0.1.2": Time_atual,
    "127.0.1.3": Time_atual,
    "127.0.1.4": Time_atual,
    "127.0.1.5": Time_atual,
    "127.0.1.6": Time_atual,
    "127.0.1.7": Time_atual,
    "127.0.1.8": Time_atual,
    "127.0.1.9": Time_atual,
    "127.0.1.10": Time_atual
}
'''

#def tempodeupdate():



def EnviaMsg(msg, host):
    #host = '127.0.0.1'
    port = 55151
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (host, port)
    msgjson = json.dumps(msg)
    udp.sendto(msgjson.encode('utf-8'), dest)
    udp.close()
    print(msg[hopsmsg])


def RecebeMsg():
    host = AddrDispAtual
    port = 55151
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    orig = (host, port)
    udp.bind(orig)
    msg, cliente = udp.recvfrom(65535)
    msgdata = json.loads(msg.decode('utf-8'))
    Roteador(msgdata)
    #print(cliente, msgdata)
    udp.close()


def Roteador(msg):

    if msg[typemsg] == 'data':

        destino = msg[destinationmsg]
        if AddrDispAtual == destino:
            print("Campo payload da mensagem:")
            print(msg[payloadmsg])
        else:
            EnviaMsg(msg, TabelaRoteamentoProx[destino])

    elif msg[typemsg] == 'update':
        update(msg)

    elif msg[typemsg] == 'trace':
        msgtrace(msg)

    else:
        print('error funcao roteador')


def update(msg):

    atualizaDist = msg[distancesmsg]
    for key in atualizaDist:
        #print("key = " + key)
        NovaDist = atualizaDist[key]
        #if AddrDispAtual in atualizaDist:      colocar forma de descobrir D1 - dist�ncia entre disp atual e vizinho
        D1 = atualizaDist[AddrDispAtual]
        #print(D1)
        if key in TabelaRoteamentoDist:
            if (NovaDist <= TabelaRoteamentoDist[key]):
                TabelaRoteamentoDist[key] = NovaDist+D1
                TabelaRoteamentoProx[key] = msg[sourcemsg]
                TabelaRoteamentoTime[key] = time.time()
            #print(NovaDist)
    TabelaRoteamentoDist[AddrDispAtual] = 0


def msgtrace(msg):

    origem = msg[sourcemsg]
    destino = msg[destinationmsg]
    hopsm = msg[hopsmsg] #alterar aqui para append
    hopsm.append(AddrDispAtual)
    msgT = {
        typemsg: tracemsg,
        sourcemsg: origem,
        destinationmsg: destino,
        hopsmsg: hopsm
    }
    if AddrDispAtual == destino:
        print("Campo hops do trace:")
        print(msg[hopsmsg])
    else:
        EnviaMsg(msg, TabelaRoteamentoProx[destino])

    #print(TabelaRoteamentoProx)
    #print(destino)
    #print(TabelaRoteamentoProx[destino])
    #print(msgT)


def Envia_Update():

    for item in disp_diret_conect:
        msg_update = {
            "type": "update",
            "source": AddrDispAtual,
            "destination": item,
            "distances": TabelaRoteamentoDist
        }


def teclado():
    while True:
        #print("digite algo:\n")
        lincmd = sys.stdin.readline()
        #print("Entrada cmd: %s" %lincmd)
        lincmd = lincmd.replace("\n", "")
        if lincmd[0] == "a":
            comando, IP, D1 = lincmd.split(" ")
            D1 = D1.replace("\n", "")
            D1 = int(D1)
            A = TabelaRoteamentoDist
            A[IP] = D1
            B = TabelaRoteamentoProx
            B[IP] = IP
            C = TabelaRoteamentoTime
            C[IP] = time.time()
            disp_diret_conect.append(IP)

        elif lincmd[0] == "d":
            comando, IP = lincmd.split(" ")

            A = TabelaRoteamentoDist
            if IP in A:
                del A[IP]
            B = TabelaRoteamentoProx
            if IP in B:
                del B[IP]
            C = TabelaRoteamentoTime
            if IP in C:
                del C[IP]

        elif lincmd[0] == "t":
            comando, IPtrace = lincmd.split(" ")
            msg1 = {  # Exemplo de msg de trace
                "type": "trace",
                "source": AddrDispAtual,
                "destination": IPtrace,
                "hops": [AddrDispAtual]
            }
            EnviaMsg(msg1,IPtrace)

        else:
            print("Erro no comando")
        #print(TabelaRoteamentoProx)
        #print(TabelaRoteamentoDist)
        #print(TabelaRoteamentoTime)

def F_arquivo(linha,cont):

    if linha[0] == "a":
        comando, IP, D1 = linha.split(" ")
        D1 = D1.replace("\n", "")
        D1 = int(D1)
        A = TabelaRoteamentoDist
        A[IP] = D1
        B = TabelaRoteamentoProx
        B[IP] = IP
        C = TabelaRoteamentoTime
        C[IP] = time.time()
        disp_diret_conect.append(IP)

    elif linha[0] == "d":
        comando, IP = linha.split(" ")
        A = TabelaRoteamentoDist
        del A[IP]
        B = TabelaRoteamentoProx
        del B[IP]
        C = TabelaRoteamentoTime
        del C[IP]

    else:
        print("Erro na linha {}".format(cont))



def timeout():
    while True:
        for key in TabelaRoteamentoTime:
            if (time.time() - TabelaRoteamentoTime[key]) > tempo_para_expirar:
                del TabelaRoteamentoDist[key]
                del TabelaRoteamentoProx[key]
                del TabelaRoteamentoTime[key]


def coordena():
    while True:
        '''for key in TabelaRoteamentoDist:
            if TabelaRoteamentoDist[key] == 0:
                AddrDispAtual = key'''

        #print("AddrDispAtual = "+AddrDispAtual)
        #print(TabelaRoteamentoDist)

        Time_atual = time.time()
        RecebeMsg()
        #Roteador(msg)
        #print(TabelaRoteamentoDist)
        #print(TabelaRoteamentoProx)


def main():

    global AddrDispAtual
    AddrDispAtual = sys.argv[1]
    tempo_para_expirar = int(sys.argv[2])
    Arquivo = sys.argv[3]
    #AddrDispAtual = "127.0.3.1"
    #Arquivo = "C:/Users/filca/PycharmProjects/TP2Redes/spoke.txt"
    cont = 0
    arq = open(Arquivo, 'r')
    for linha in arq:
        F_arquivo(linha, cont)
        cont += 1

    ThreadTeclado = threading.Thread(target=teclado)
    ThreadAtualiza = threading.Thread(target=timeout)
    ThreadRecebe = threading.Thread(target=coordena)

    ThreadTeclado.start()
    #ThreadAtualiza.start()
    ThreadRecebe.start()



main()
