#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ****************************************#
#  Programa de Transferencia de Archivos  #
#       Ing. Kennedy Sanchez			        #
#    (Security + MGP + PS. Auditor)       #
#     @ksanchez_cld on twitter		    	  #
# **************************************** 	

import paramiko
import os, smtplib, time
from sys import stdin
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

print "###########NET MONITOR###########"
print "   Disk Monitor Tool by Ksanchez    "
print "        05 Feb. 2014                "
print "####################################"
time.sleep(3)

horaRaw = time.time()
horaFormato = time.ctime(horaRaw)

SERVIDOR           = '10.0.0.10'
PUERTO_SSH         = 22
USUARIO_SSH        = 'root'
CLAVE_SSH          = '****'
CMD_HOST           = 'hostname'
PATH               = '/tmp/monitoreo'

'''
def serverGroup():
	ipfile = open('iplistssh.txt', 'r')
	ip = ipfile.readlines()
	if ip[0] == SERVIDOR_SSH:
		print "SERVIDOR BACKUP CONECTADO"
	else:
		print "NO ESTA CONECTADO!!!"
'''

'''
Hacer una funcion por cada servidor, es la opcion mas horrible de disenar un programa. Por la rapidez y la necesidad de 
colocarlo rapido en produccion lo hice de esta forma, lo ideal es crear una lista de servidores a monitorear y recorrerla
para conectar. Por el momento esta es primitiva, pero funcional.

En futura version, espero arreglar esto.
'''

def sshXferServer():
	cnx = paramiko.Transport((SERVIDOR, PUERTO_SSH))
	cnx.connect(username = USUARIO_SSH, password = CLAVE_SSH)

	canal = cnx.open_session()
	canal.exec_command('rm -rf /tmp/monitoreo/ && mkdir -p /tmp/monitoreo && hostname >/tmp/monitoreo/size_Correo.log && df -h >>/tmp/monitoreo/size_Correo.log') 
	canal.exec_command('ls -alh')
	salida = canal.makefile('rb', -1).readlines()
	if salida:
		print salida
	else:
		print canal.makefile_stderr('rb', -1).readlines()
	cnx.close()
	print ('*'*50)
	print ('TRANSFIRIENDO ARCHIVOS....')
	print ('*'*50)

	cnx = paramiko.Transport((SERVIDOR, PUERTO_SSH))
	cnx.connect(username = USUARIO_SSH, password = CLAVE_SSH)

	sftp = paramiko.SFTPClient.from_transport(cnx)
	archivos = sftp.listdir('/tmp/monitoreo/')
	for f in archivos:
	  print "Recibiendo ",f
	  sftp.get(os.path.join('/tmp/monitoreo/',f),f)
	cnx.close()


def sendMail():
	msg = MIMEMultipart()
	msg['From'] = "k.sanchez@micorreo.com"
	#body = msg.attach( MIMEText(r))
	msg['Subject'] = "Reporte diario monitoreo espacio en disco" 
	macct = "otroUsuario@sucorreo.com"
	msg.attach( MIMEText("Adjunto, archivo de espacio en disco.\n\n" + "Realizado en fecha:" + horaFormato))
	files=["size_Correo.log"]
	for f in files:
	    part = MIMEBase('application', "octet-stream")
	    part.set_payload( open(f,"rb").read())
	    Encoders.encode_base64(part)
	    part.add_header('Content-Disposition', 'attachment; filename="size_servidores.log"')
	    msg.attach(part)
	s = smtplib.SMTP()
	s.connect("servidorcorreo.com", 25)
	s.sendmail("k.sanchez@micorreo.com", macct , msg.as_string())
	s.quit()
	 
sshXferIMSVA
sendMail()
