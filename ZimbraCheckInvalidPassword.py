#!/usr/bin/env python

import sys
import json

def sintaxe_usage():
                print "--------------------------------------------------------------------- "
                print "---------------------------- EXEMPLO DE USO ------------------------- "
                print " script.py total         #Total de tentativas de autenticacao falhadas"
                print " script.py imap          #Total de tentativas via imap "
                print " script.py pop           #Total de tentativas via pop "
                print " script.py webmail       #Total de tentativas via webmail "
                print " script.py users         #Total de tentativas por usuario "
                print "--------------------------------------------------------------------- "



def le_arquivo():
        try:
                arq_file = open (my_cfile,"r")
                lastSize = arq_file.read()
                arq_file.close()
                return lastSize
        except IOError:                         # Tratamento de erro
                print('\nFile not found!\n')

def escreve_arquivo(endSize):
        try:
                var_file = open(my_cfile,"w")
                var_file.write(str(endSize))            # Escreve posicao final do arquivo 'file_to_read' no arquivo size.log
                var_file.close()
        except IOError:
                print('\nError opening file!\n')

cont = 0

for arg in sys.argv:
        cont = cont + 1

if (cont < 4):
    sintaxe_usage();
    sys.exit(3)


# path to the file to read from
my_file = "/opt/zimbra/log/mailbox.log"
#my_file = "/root/logteste.txt"
my_cfile = "/tmp/sizeMailBox.%s.txt" % (sys.argv[1])
# what to look in each line
look_for = "CHECKOUT_REVISION"
# variable to store lines containing CHECKOUT_REVISION
temp = []
n = 0
imap = 0
pop = 0
SoapEngine = 0
users = {}
USER = ''
WARN = (sys.argv[2])
CRIT = (sys.argv[3])
name = ''
ip = ''
ok = ''
critical = ''
warning = ''
param = sys.argv


with open(my_file, "r") as file_to_read:

        lastSize = le_arquivo()
        file_to_read.seek(0,2)                  #Seta o final do arquivo.
        endSize = file_to_read.tell()           #Cria a variavel com conteudo da ultimo byte.
        escreve_arquivo(endSize)

        if int(lastSize) > int(endSize):
                startR = 0
        else:
                startR = lastSize

        file_to_read.seek(int (startR))                 #Inicia a leitura do arquivo
        #file_to_read.seek(0)            #Inicia a leitura do arquivo


        for line in file_to_read:
                if 'invalid password' in line:

                        if 'imap' in line:
                                imap += 1
                                str1 = line
                                name = str1.split('failed for [')[1].split("]")[0]
                                ip = str1.split('] [ip=')[1].split(";]")[0]
                                USER = name + "_" + ip
                        if 'pop -' in line:
                                pop += 1

                        if 'SoapEngine' in line:
                                SoapEngine += 1
                                str1 = line
                                name = str1.split('] [name=')[1].split(";")[0]
                                ip =   str1.split('ip=')[1].split(";")[0]
                                USER = name + "_" + ip

                        if USER in users:
                                users[USER] += 1
                        else:
                                users[USER] = 1

                        n += 1
                        temp.append(line)

        if 'total' in sys.argv[1] :

                if n < int(WARN):
                        #connectionsforsecond=$MYSQLCONFORSECOND,WARN,CRIT
                        #print "OK_NEW - Numero de Tentativas: {} | total={},{} ".format(n,WARN,CRIT)
                        #print "OK - Numero de Tentativas: %s | total=%s,%s " % (n,WARN,CRIT)
                        print "OK - Number of attempts: %s | total=%s;%s;%s;;" % (n,n,WARN,CRIT)
                        sys.exit(0)

                elif n < int(CRIT):

                        print "WARNING - Number of attempts: %s | total=%s;%s;%s;;" % (n,n,WARN,CRIT)
                        sys.exit(1)

                else:
                        print "Critical - Number of attempts: %s | total=%s;%s;%s;;" % (n,n,WARN,CRIT)
                        sys.exit(2)


        elif 'imap' in sys.argv[1]:

                if imap < int(WARN):

                        print "OK - Number of attempts: %s | total=%s;%s;%s;;" % (imap,imap,WARN,CRIT)
                        sys.exit(0)

                elif imap < int(CRIT):

                        print "WARNING - Number of attempts: %s | total=%s;%s;%s;;" % (imap,imap,WARN,CRIT)
                        sys.exit(1)

                else:
                        print "CRITICAL - Number of attempts: %s | total=%s;%s;%s;;" % (imap,imap,WARN,CRIT)
                        sys.exit(2)


        elif 'pop' in sys.argv[1]:

                if pop < int(WARN):

                        print "OK - Number of attempts: %s | total=%s;%s;%s;;" % (pop,pop,WARN,CRIT)
                        sys.exit(0)

                elif pop < int(CRIT):

                        print "WARNING - Number of attempts: %s | total=%s;%s;%s;;" % (pop,pop,WARN,CRIT)
                        sys.exit(1)

                else:
                        print "CRITICAL - Number of attempts: %s | total=%s;%s;%s;;" % (pop,pop,WARN,CRIT)
                        sys.exit(2)


        elif 'webmail' in sys.argv[1]:

                if SoapEngine < int(WARN):

                        print "OK - Number of attempts: %s | total=%s;%s;%s;;" % (SoapEngine,SoapEngine,WARN,CRIT)
                        sys.exit(0)

                elif SoapEngine < int(CRIT):

                        print "WARNING - Number of attempts: %s | total=%s;%s;%s;;" % (SoapEngine,SoapEngine,WARN,CRIT)
                        sys.exit(1)

                else:
                        print "CRITICAL - Number of attempts: %s | total=%s;%s;%s;;" % (SoapEngine,SoapEngine,WARN,CRIT)
                        sys.exit(2)


        elif 'users' in sys.argv[1]:

                        for USER in users:
                                if users[USER] < int(WARN):
                                        ok = ok + USER + ":" + str(users[USER]) + "; "

                                elif users[USER] < int(CRIT):
                                        warning = warning + USER + ":" + str(users[USER]) + "; "
                                else:
                                        critical = critical + USER + ":" + str(users[USER]) + "; "

                        if (len(critical) > 0):
                                print "CRITICAL - Number of attempts by users %s" %critical
                                sys.exit(2)

                        if (len(warning) > 0):
                                print "WARNING - Number of attempts by users - %s" %warning
                                sys.exit(1)

                        if (len(ok) > 0) or (len(ok) ==0):
                                print "OK - Number of attempts by users %s" %ok
                                sys.exit(0)

        else:
                sintaxe_usage();
