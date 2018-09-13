#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys


def Interpreta_Tags(msg, cliente, socket, abort):

    #essa funcao recebe as mensagens e interpreta as tags

    #msg =  sys.stdin.readline()
    msg = msg + " "
    msg_para_enviar = msg
    tag1 = ''
    tag2 = ''
    tags_msg = []
    tags_add = []
    tags_add2 = []
    tags_del = []
    tags_del2 = []
    tamanho_msg = len(msg) - 1
    cont = 0


    while cont < tamanho_msg:

        if msg[cont] == '#':
            #cont += 1
            if (msg[cont+1] == '#') or (msg[cont+1] == '+') or (msg[cont+1] == '-') or (msg[cont+1] == ' '):
                msg_erro = "Digitacao incorreta. Nao pode haver caractere de comando ('#', '+', '-') ou espaco em branco depois de outro caractere de comando"
                cont = tamanho_msg-1
                abort = 1
                dest = ('127.0.0.1', int(cliente))
                socket.sendto(msg_erro, dest)
            while ((msg[cont+1] != " ") and (msg[cont+1] != '#') and (msg[cont+1] != '\n') and (msg[cont+1] != '+') and (msg[cont+1] != '-')):
                tag1 = tag1 + msg[cont+1]
                tag2 = tag2 + msg[cont]
                cont += 1
            tag2 = tag2 + msg[cont]

            tags_msg.append(tag1)
            #print(tag1)

        elif msg[cont] == '+':
            if (msg[cont+1] == '#') or (msg[cont+1] == '+') or (msg[cont+1] == '-') or (msg[cont+1] == ' '):
                msg_erro = "Digitacao incorreta. Nao pode haver caractere de comando ('#', '+', '-') ou espaco em branco depois de outro caractere de comando"
                cont = tamanho_msg
                abort = 1
                dest = ('127.0.0.1', int(cliente))
                socket.sendto(msg_erro, dest)
            while ((msg[cont+1] != " ") and (msg[cont+1] != '#') and (msg[cont+1] != '\n') and (msg[cont+1] != '+') and (msg[cont+1] != '-')):
                tag1 = tag1 + msg[cont + 1]
                tag2 = tag2 + msg[cont]
                cont += 1
            tag2 = tag2 + msg[cont]
            tags_add.append(tag1)
            tags_add2.append(tag2)
            #print(tag1)

        elif msg[cont] == '-':
            if (msg[cont+1] == '#') or (msg[cont+1] == '+') or (msg[cont+1] == '-') or (msg[cont+1] == ' '):
                msg_erro = "Digitacao incorreta. Nao pode haver caractere de comando ('#', '+', '-') ou espaco em branco depois de outro caractere de comando"
                cont = tamanho_msg
                abort = 1
                dest = ('127.0.0.1', int(cliente))
                socket.sendto(msg_erro, dest)
            while ((msg[cont+1] != " ") and (msg[cont+1] != '#') and (msg[cont+1] != '\n') and (msg[cont+1] != '+') and (msg[cont+1] != '-')):
                tag1 = tag1 + msg[cont + 1]
                tag2 = tag2 + msg[cont]
                cont += 1
            tag2 = tag2 + msg[cont]
            tags_del.append(tag1)
            tags_del2.append(tag2)
            #print(tag1)


        cont += 1
        tag1 = ''
        tag2 = ''

    for item in tags_add2:
        msg_para_enviar = msg_para_enviar.replace(item,"")
        #msg_para_enviar = msg_para_enviar.replace('+', "")
    for item in tags_del2:
        msg_para_enviar = msg_para_enviar.replace(item, "")
        #msg_para_enviar = msg_para_enviar.replace('-', "")
    #print("tags da mensagem: {}\nnovas tags de interesse: {}\ntags sem interesse: {}\n".format(tags_msg,tags_add,tags_del))
    return tags_msg, tags_add, tags_del, msg_para_enviar, abort


def Atualiza_Cliente(tags_interesse_cliente, msg, cliente, socket, abort):

    #essa funcao mantem atualizadas quais sao as tags que o cliente que ver

    tags_msg, tags_add, tags_del, msg_para_enviar, abort1 = Interpreta_Tags(msg, cliente, socket, abort)
    for tag in tags_add:
        if abort1 == 0:
            tags_interesse_cliente.append(tag)
            msg1 = ("Voce quer ver mensagens sobre {}".format(tag))
            dest = ('127.0.0.1', int(cliente))
            socket.sendto(msg1,dest)

    for tag in tags_del:
        if abort1 == 0:
            if (tag in tags_interesse_cliente):
                tags_interesse_cliente.remove(tag)
            msg2 = ("Voce nao quer mais ver mensagens sobre {}".format(tag))
            dest = ('127.0.0.1', int(cliente))
            socket.sendto(msg2, dest)
    return tags_msg, msg_para_enviar, abort1


def coordena(msg,cliente,socket,Tags_interesse_clientes, abort):

    #exemplo_msg = "#viagem#mar+comida-famosos indo pra #praia !! #ferias +ferias"
    #msg = exemplo_msg

    if cliente not in Tags_interesse_clientes:
        Tags_interesse_clientes[cliente] = []

    tags_msg, msg_para_enviar, abort1 = Atualiza_Cliente(Tags_interesse_clientes[cliente], msg, cliente, socket, abort)


    #+print(Tags_interesse_clientes)

    for client in Tags_interesse_clientes:

        envia = 0
        #for tag1 in Tags_interesse_clientes[client]:
        #    print(tag1)
        for tag in tags_msg:
            if tag in Tags_interesse_clientes[client] and abort == 0:
                #print(tag)
                envia = 1
        if envia == 1:
            # ---envia a mensagem para o cliente
            #print("envia mensagem")
            dest = ('127.0.0.1', int(client))
            socket.sendto(msg_para_enviar,dest)
            #print(msg_para_enviar)

        #print(tags_interesse_cliente)
        #print(msg)
        #print(msg_para_enviar)



def Recebe(PortaServidor):
    HOST = ''              # Endereco IP do Servidor
    PORT = PortaServidor            # Porta que o Servidor esta
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    orig = (HOST, PORT)
    udp.bind(orig)

    Tags_interesse_clientes = {

    }

    while True:
        msg, cliente = udp.recvfrom(1024)
        IPCliente,PortaCliente = cliente
        dest = (IPCliente, PortaCliente)
        client = str(PortaCliente)
        abort = 0
        coordena(msg, client, udp, Tags_interesse_clientes, abort)


    #udp.close()

try:
    PortaServidor = int(sys.argv[1])
    Recebe(PortaServidor)
except KeyboardInterrupt:
  pass