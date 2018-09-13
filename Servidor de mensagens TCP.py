#!-*-coding: utf8-*-

import socket
import _thread
import sys
import time

import base64


def FuncCheckSum(data, sum=0):

    for i in range(0, len(data), 2):
        if i + 1 >= len(data):
            sum += ord(data[i]) & 0xFF
        else:
            w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i + 1]) & 0xFF)
            sum += w

    while (sum >> 16) > 0:
        sum = (sum & 0xFFFF) + (sum >> 16)

    sum = ~sum

    return sum & 0xFFFF


def Codifica(Pacote):
    PacoteCodificado = ""
    x = len(Pacote) / 4
    L1 = 0
    L2 = 4
    c = ""
    while x > 0:
        Parte = Pacote[L1:L2]
        if (Parte == "0000"):
            c = "0"
        if (Parte == "0001"):
            c = "1"
        if (Parte == "0010"):
            c = "2"
        if (Parte == "0011"):
            c = "3"
        if (Parte == "0100"):
            c = "4"
        if (Parte == "0101"):
            c = "5"
        if (Parte == "0110"):
            c = "6"
        if (Parte == "0111"):
            c = "7"
        if (Parte == "1000"):
            c = "8"
        if (Parte == "1001"):
            c = "9"
        if (Parte == "1010"):
            c = "A"
        if (Parte == "1011"):
            c = "B"
        if (Parte == "1100"):
            c = "C"
        if (Parte == "1101"):
            c = "D"
        if (Parte == "1110"):
            c = "E"
        if (Parte == "1111"):
            c = "F"

        L1 += 4
        L2 += 4
        x -= 1
        PacoteCodificado = PacoteCodificado + c

    return PacoteCodificado


def Decodifica(PacoteCodificado):
    PacoteDecodificado = ""
    x = len(PacoteCodificado)
    c = ""
    n = 0
    while x > 0:
        Parte = PacoteCodificado[n]
        if (Parte == "0"):
            c = "0000"
        if (Parte == "1"):
            c = "0001"
        if (Parte == "2"):
            c = "0010"
        if (Parte == "3"):
            c = "0011"
        if (Parte == "4"):
            c = "0100"
        if (Parte == "5"):
            c = "0101"
        if (Parte == "6"):
            c = "0110"
        if (Parte == "7"):
            c = "0111"
        if (Parte == "8"):
            c = "1000"
        if (Parte == "9"):
            c = "1001"
        if (Parte == "A"):
            c = "1010"
        if (Parte == "B"):
            c = "1011"
        if (Parte == "C"):
            c = "1100"
        if (Parte == "D"):
            c = "1101"
        if (Parte == "E"):
            c = "1110"
        if (Parte == "F"):
            c = "1111"

        n += 1
        x -= 1
        PacoteDecodificado = PacoteDecodificado + c

    return PacoteDecodificado





#Cliente

def ClienteEnvia(IPePorta, Input, Output):

    IP,Porta = IPePorta.split(':')

    HOST = IP  # Endereco IP do Servidor
    PORT = int(Porta)  # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    #print('Para sair use CTRL+X\n')

    def Envia(tcp, LocaldoArquivo):
        NumeroDeQuadros = 0


        arq = open(LocaldoArquivo, 'r')

        DadosParaEnviar = arq.read()  # colocou o arquivo de entrada no vetor
        arq.close()

        '''enquadramento'''


        TamanhoArq = len(DadosParaEnviar)

        # print(TamanhoArq)
        Length = 100  # Length é configurável. Length = 65536 caracteres.

        i = TamanhoArq - Length  # Não pode começar do primeiro e ir incrementando. O primeiro pacote vai dar erro. Ele não tem tamanho fixo
        n = 1
        LimInf = 0
        LimSup = Length
        # NumDePacotes = TamanhoArq/Length
        fim = 0
        DadosDoPacote = ""
        iyd=0

        # ID = "00000000" #ID inicial
        while fim == 0:
            if i >= 0:
                DadosDoPacote = DadosParaEnviar[LimInf:LimSup]  # DadosPara enviar é o arquivo de entrada completo
                # print("Dados do pacote {} =\n{}".format(n, DadosDoPacote))


            # Aqui eu pego o último pacote, que tem tamanho variável
            elif i < 0:
                DadosDoPacote = DadosParaEnviar[LimInf:]
                fim = 1
            n = n + 1
            i = i - Length
            #print("i = {}", i)
            LimInf = LimInf + Length
            LimSup = LimSup + Length



            AC = ""
            x = 0
            DadoPack = DadosDoPacote
            Len = len(DadosDoPacote)
            DadosDoPacote = ""
            while x < Len:
                AA = ord(DadoPack[x])
                AB = bin(AA).split('b')[-1]
                DadosDoPacote = str(AB)
                while ((len(DadosDoPacote) % 8) != 0):
                    DadosDoPacote = "0" + DadosDoPacote
                AC = AC + DadosDoPacote
                x += 1
            DadosDoPacote = AC


            TamanhoDado = len(DadosDoPacote)  # Campo Length

            TamanhoDados = bin(TamanhoDado).split('b')[-1]
            aux1 = 15 - len(str(TamanhoDados))
            while aux1 >= 0:
                TamanhoDados = '0' + TamanhoDados
                aux1 = aux1 - 1

            Sync = "11011100110000000010001111000010"
            IDa = "00000000"
            IDb = "11111111"  # inverte o ID
            if iyd == 0:
                ID = IDa
                iyd = 1
            else:
                ID = IDb
                iyd = 0
            flags = "00000000"
            checksum0 = "0000000000000000"  # Valor correto do checksum
            SemiPacote = Sync + Sync + TamanhoDados + checksum0 + ID + flags + DadosDoPacote
            checksum = FuncCheckSum(SemiPacote)

            checksum = bin(checksum).split('b')[-1]
            aux1 = 15 - len(str(checksum))
            while aux1 >= 0:
                checksum = '0' + checksum
                aux1 = aux1 - 1

            checksum = str(checksum)
            Pacote = Sync + Sync + TamanhoDados + checksum + ID + flags + DadosDoPacote
            PacoteCodificado = Codifica(Pacote)

            tcp.send(PacoteCodificado)

            #tcp.settimeout(1)
            QuadroACK = tcp.recv(1024)

            flags1 = "10000000"
            checksum0 = "0000000000000000"
            Sync = "11011100110000000010001111000010"

            SyncRec1 = QuadroACK[0:32]
            SyncRec2 = QuadroACK[32:64]
            LengthRec = QuadroACK[64:80]
            checksumRec = QuadroACK[80:96]
            IDRec = QuadroACK[96:104]
            flagsRec = QuadroACK[104:112]

            TesteChecksum = SyncRec1 + SyncRec2 + LengthRec + checksum0 + IDRec + flagsRec
            ConfirmaCheckSum = FuncCheckSum(TesteChecksum)

            ConfirmaCheckSum = bin(ConfirmaCheckSum).split('b')[-1]
            aux1 = 15 - len(str(ConfirmaCheckSum))
            while aux1 >= 0:
                ConfirmaCheckSum = '0' + ConfirmaCheckSum
                aux1 = aux1 - 1

                ConfirmaCheckSum = str(ConfirmaCheckSum)

            if (SyncRec1 == Sync and SyncRec2 == Sync and IDRec == ID and flagsRec != flags1):  # falta checksum
                print()
                #print("ACK {} recebido\n".format(n - 1))
            else:
                n = n - 1
                i = i + Length
                LimInf = LimInf - Length
                LimSup = LimSup - Length
                if n % 2 == 0:
                    ID = IDa
                else:
                    ID = IDb
                time.sleep(1)
            i = i - Length
            LimInf = LimInf + Length
            LimSup = LimSup + Length
        _thread.exit()

    def Recebe(tcp1, LocaldoArquivo):

        IDAnterior = "a"
        n = 1
        # LocaldoArquivo = '/home/jertav/Desktop/saida.txt'  # recebe da linha de comando
        # aux = 1

        while True:

            flags = "10000000"

            Sync = "11011100110000000010001111000010"

            QuadroRecebido1 = tcp1.recv(1024)
            QuadroRecebido = Decodifica(QuadroRecebido1)
            SyncRec1 = QuadroRecebido[0:32]
            SyncRec2 = QuadroRecebido[32:64]
            LengthRec = QuadroRecebido[64:80]
            TamanhoDados = 0
            exp = len(LengthRec) - 1
            for I in LengthRec:
                if I == "1":
                    TamanhoDados += 2 ** exp
                exp -= 1

            checksumRec = QuadroRecebido[80:96]
            checksum0 = "0000000000000000"
            IDRec = QuadroRecebido[96:104]
            flagsRec = QuadroRecebido[104:112]

            final = 112 + TamanhoDados
            DadosRecBin = QuadroRecebido[112:final]

            TesteChecksum = SyncRec1 + SyncRec2 + LengthRec + checksum0 + IDRec + flagsRec + DadosRecBin
            ConfirmaCheckSum = FuncCheckSum(TesteChecksum)

            ConfirmaCheckSum = bin(ConfirmaCheckSum).split('b')[-1]
            aux1 = 15 - len(str(ConfirmaCheckSum))

            while aux1 >= 0:
                ConfirmaCheckSum = '0' + ConfirmaCheckSum
                aux1 = aux1 - 1

                ConfirmaCheckSum = str(ConfirmaCheckSum)

            # Transforma a string binária em string ascii
            DadosRec = ""
            J = 0
            while J < len(DadosRecBin) / 8:
                num = 0
                exp = 7
                n1 = 8 * J
                while n1 < 8 * J + 8:
                    if DadosRecBin[n1] == "1":
                        num += 2 ** exp
                    exp -= 1
                    n1 += 1
                J += 1
                DadosRec += chr(num)

            n += 1  # tirar isso depois

            if (SyncRec1 == Sync and SyncRec2 == Sync and IDRec != IDAnterior and flagsRec != flags):  # falta checksum
               # print("Pacote {} recebido/n".format(n))
                n = n + 1
                arq = open(LocaldoArquivo, 'a')
                sys.stdout.flush()
                arq.write(DadosRec)
                #arq.write(str(n))
                arq.close()
                StringCheckSumACK = Sync + Sync + LengthRec + "0000000000000000" + IDRec + flags
                checksumACK = FuncCheckSum(StringCheckSumACK)

                checksumACK = bin(checksumACK).split('b')[-1]
                aux1 = 15 - len(str(checksumACK))
                # print("tamanho dados = " + TamanhoDados)
                while aux1 >= 0:
                    checksumACK = '0' + checksumACK
                    aux1 = aux1 - 1

                    checksumACK = str(checksumACK)

                ACK = Sync + Sync + LengthRec + checksumACK + IDRec + flags

                tcp1.send(ACK)

            else:

                time.sleep(1)
            IDAnterior = IDRec

            # if DadosRec== 0:
            #   aux = 0

        tcp1.close()
        _thread.exit()



    i = 0

    while True:
        if (i == 0):
            tcp.connect(dest)
            i = 1
            _thread.start_new_thread(Envia, tuple([tcp, Input]))
        elif i==1:
            tcp1.connect(dest)
            i=2
            _thread.start_new_thread(Recebe, tuple([tcp1, Output]))
        else:
            None

    tcp.close()

'''def ClienteRecebe():

    #IP,Porta = IPePorta.split(':')

    print('\nentrou cliente2')
    HOST = '127.0.0.1'  # Endereco IP do Servidor
    PORT = 5000  # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    print('Para sair use CTRL+X\n')

    while True:
        msg = tcp.recv(1024)
        if not msg:break
        else:
            ack = 'ack'
            tcp.send(ack)
            print(msg)

    tcp.close()'''



#Servidor

def Servidor(Porta, Input, Output):
    #print('\nentrou servidor')
    HOST = ''  # Endereco IP do Servidor
    PORT = int(Porta)  # Porta que o Servidor esta

    def conectado(con, cliente, LocaldoArquivo):
        #print('Conectado por', cliente)

        IDAnterior = "a"
        n = 1

        while True:

            flags = "10000000"
            Sync = "11011100110000000010001111000010"

            #con.settimeout(1)
            QuadroRecebido1 = con.recv(1024)
            QuadroRecebido = Decodifica(QuadroRecebido1)

            SyncRec1 = QuadroRecebido[0:32]
            SyncRec2 = QuadroRecebido[32:64]
            LengthRec = QuadroRecebido[64:80]
            TamanhoDados = 0
            exp = len(LengthRec) - 1
            for I in LengthRec:
                if I == "1":
                    TamanhoDados += 2 ** exp
                exp -= 1

            checksumRec = QuadroRecebido[80:96]
            checksum0 = "0000000000000000"
            IDRec = QuadroRecebido[96:104]
            flagsRec = QuadroRecebido[104:112]

            final = 112 + TamanhoDados
            DadosRecBin = QuadroRecebido[112:final]

            TesteChecksum = SyncRec1 + SyncRec2 + LengthRec + checksum0 + IDRec + flagsRec + DadosRecBin
            ConfirmaCheckSum = FuncCheckSum(TesteChecksum)

            ConfirmaCheckSum = bin(ConfirmaCheckSum).split('b')[-1]
            aux1 = 15 - len(str(ConfirmaCheckSum))
            while aux1 >= 0:
                ConfirmaCheckSum = '0' + ConfirmaCheckSum
                aux1 = aux1 - 1

                ConfirmaCheckSum = str(ConfirmaCheckSum)

            # Transforma a string binária em string ascii
            DadosRec = ""
            J = 0
            while J < len(DadosRecBin) / 8:
                num = 0
                exp = 7
                n1 = 8 * J
                while n1 < 8 * J + 8:
                    if DadosRecBin[n1] == "1":
                        num += 2 ** exp
                    exp -= 1
                    n1 += 1
                J += 1
                DadosRec += chr(num)


            n += 1  #

            if (SyncRec1 == Sync and SyncRec2 == Sync and IDRec != IDAnterior and flagsRec != flags):  # falta checksum
               # print("Pacote {} recebido/n".format(n))
                n = n + 1
                arq = open(LocaldoArquivo, 'a')
                sys.stdout.flush()
                arq.write(DadosRec)
                #arq.write(str(n))
                arq.close()
                StringCheckSumACK = Sync + Sync + LengthRec + "0000000000000000" + IDRec + flags
                checksumACK = FuncCheckSum(StringCheckSumACK)

                checksumACK = bin(checksumACK).split('b')[-1]
                aux1 = 15 - len(str(checksumACK))
                # print("tamanho dados = " + TamanhoDados)
                while aux1 >= 0:
                    checksumACK = '0' + checksumACK
                    aux1 = aux1 - 1

                    checksumACK = str(checksumACK)

                ACK = Sync + Sync + LengthRec + checksumACK + IDRec + flags
                #print("ACK = ", ACK)
                #print("Dados = ", DadosRec)
                #print()
                con.send(ACK)

            else:
                print("Erro\n")
                time.sleep(1)
            IDAnterior = IDRec

            # if DadosRec== 0:
            #   aux = 0

        con.close()
        _thread.exit()

    def envia(con, cliente, LocaldoArquivo):
        NumeroDeQuadros = 0
        ''''''
        arq = open(LocaldoArquivo, 'r')

        DadosParaEnviar = arq.read()  # colocou o arquivo de entrada no vetor
        arq.close()
        # print(DadosParaEnviar)

        '''enquadramento'''

        TamanhoArq = len(DadosParaEnviar)

        Length = 100  # Length é configurável. Length = 65536 caracteres.

        i = TamanhoArq - Length  # Não pode começar do primeiro e ir incrementando. O primeiro pacote vai dar erro. Ele não tem tamanho fixo
        n = 1
        LimInf = 0
        LimSup = Length
        # NumDePacotes = TamanhoArq/Length -- Não usei a variável NumDePacotes
        fim = 0
        DadosDoPacote = ""
        iyd=0

        # ID = "00000000" #ID inicial
        while fim == 0:
            if i >= 0:
                DadosDoPacote = DadosParaEnviar[LimInf:LimSup]  # DadosPara enviar é o arquivo de entrada completo
                # print("Dados do pacote {} =\n{}".format(n, DadosDoPacote))


            # Aqui eu pego o último pacote, que tem tamanho variável
            elif i < 0:
                DadosDoPacote = DadosParaEnviar[LimInf:]
                fim = 1
                # print("Dados do pacote {} = {}".format(n, DadosDoPacote))
            n = n + 1
            i = i - Length
            LimInf = LimInf + Length
            LimSup = LimSup + Length

            # DadosDoPacote = bin(int.from_bytes(DadosDoPacote.encode(), 'big')).split('b')[-1]
            AC = ""
            x = 0
            DadoPack = DadosDoPacote
            Len = len(DadosDoPacote)
            DadosDoPacote = ""
            while x < Len:
                AA = ord(DadoPack[x])
                #print("AA = {}".format(AA))
                AB = bin(AA).split('b')[-1]
                #print("AB = {}".format(AB))
                DadosDoPacote = str(AB)
                while ((len(DadosDoPacote) % 8) != 0):
                    DadosDoPacote = "0" + DadosDoPacote
                AC = AC + DadosDoPacote
                x += 1

            DadosDoPacote = AC

            '''converte para ascii decimal'''

            TamanhoDado = len(DadosDoPacote)  # Campo Length

            '''TamanhoDados = str(TamanhoDado)
            aux1 = 15-len(TamanhoDados)
            while aux1 >= 0:
                TamanhoDados = '0'+ TamanhoDados
                aux1 = aux1-1
            print("tamanho dados = " + TamanhoDados)

            '''
            TamanhoDados = bin(TamanhoDado).split('b')[-1]
            aux1 = 15 - len(str(TamanhoDados))
            while aux1 >= 0:
                TamanhoDados = '0' + TamanhoDados
                aux1 = aux1 - 1

            Sync = "11011100110000000010001111000010"  # b'\xdc\xc0#\xc2' # DCC023C2 antes de codificar
            IDa = "00000000"  # Aqui dá problema.
            IDb = "11111111"  # inverte o ID
            if iyd == 0:
                ID = IDa
                iyd = 1
            else:
                ID = IDb
                iyd = 0
            flags = "00000000"
            checksum0 = "0000000000000000"  # Valor correto do checksum
            SemiPacote = Sync + Sync + TamanhoDados + checksum0 + ID + flags + DadosDoPacote
            checksum = FuncCheckSum(SemiPacote)

            checksum = bin(checksum).split('b')[-1]
            aux1 = 15 - len(str(checksum))

            while aux1 >= 0:
                checksum = '0' + checksum
                aux1 = aux1 - 1

            checksum = str(checksum)
            Pacote = Sync + Sync + TamanhoDados + checksum + ID + flags + DadosDoPacote
            PacoteCodificado = Codifica(Pacote)

            con.send(PacoteCodificado)

            #con.settimeout(1)
            QuadroACK = con.recv(1024)

            flags1 = "10000000"

            checksum0 = "0000000000000000"
            Sync = "11011100110000000010001111000010"

            SyncRec1 = QuadroACK[0:32]
            SyncRec2 = QuadroACK[32:64]
            LengthRec = QuadroACK[64:80]
            checksumRec = QuadroACK[80:96]
            IDRec = QuadroACK[96:104]
            flagsRec = QuadroACK[104:112]

            TesteChecksum = SyncRec1 + SyncRec2 + LengthRec + checksum0 + IDRec + flagsRec
            ConfirmaCheckSum = FuncCheckSum(TesteChecksum)

            ConfirmaCheckSum = bin(ConfirmaCheckSum).split('b')[-1]
            aux1 = 15 - len(str(ConfirmaCheckSum))
            # print("tamanho dados = " + TamanhoDados)
            while aux1 >= 0:
                ConfirmaCheckSum = '0' + ConfirmaCheckSum
                aux1 = aux1 - 1

                ConfirmaCheckSum = str(ConfirmaCheckSum)

            if (SyncRec1 == Sync and SyncRec2 == Sync and IDRec == ID and flagsRec != flags1):  # falta checksum
                print()
            else:
                n = n - 1
                i = i + Length
                LimInf = LimInf - Length
                LimSup = LimSup - Length
                if n % 2 == 0:
                    ID = IDa
                else:
                    ID = IDb
                time.sleep(1)
            i = i - Length
            LimInf = LimInf + Length
            LimSup = LimSup + Length
        _thread.exit()


    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    orig = (HOST, PORT)

    tcp.bind(orig)
    tcp.listen(1)

    i=0

    while True:
        con, cliente = tcp.accept()
        if(i==0):
            i = 1
            _thread.start_new_thread(conectado, tuple([con, cliente, Output]))
        else:
            _thread.start_new_thread(envia, tuple([con, cliente, Input]))


    tcp.close()

def main():

    if sys.argv[1] == "-c":
        IPePorta = sys.argv[2]
        Input = sys.argv[3]
        Output = sys.argv[4]
        ClienteEnvia(IPePorta, Input, Output)
        #ClienteRecebe()
        #print('fim')

    elif sys.argv[1] == "-s":
        Porta = sys.argv[2]
        Input = sys.argv[3]
        Output = sys.argv[4]
        Servidor(Porta, Input, Output)
        #print('fim')
    else:
        print('error')


main()





