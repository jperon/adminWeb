#!/usr/bin/python
# -*- coding: UTF-8 -*-
import string,time,subprocess
import os,sys,cgi,base64,socket,ssl
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from config import *

#Program developed to control linux in a web fashion
#AUThOR : ROBERTO RIBEIRO - PRODASEN SSA
#DATE : 31/05/2011
# Initial point of the program - DO NOT CHANGE ANYTHING FROM THIS POINT
bstyle="style='color:white;background-color:#55575c;font-color:white;width:120;height:35;border:1px solid;'"
hostname = socket.gethostname()
global result
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        caminho = os.path.realpath(os.path.dirname(sys.argv[0]))
        try:
           basic = base64.b64encode(baseConfig[3]+":"+baseConfig[4])           
           if self.headers.getheader('Authorization') == None or self.headers.getheader('Authorization') != 'Basic '+basic:
              self.send_response(401)
              self.send_header('WWW-Authenticate', 'Basic realm=\"adminWeb\"')
              self.send_header('Content-type', 'text/html; charset=utf-8')
              self.end_headers()
              self.wfile.write("<html><head></head><body style='color:white;background-color:grey'><center>"+baseConfig[5]+" </center>") 
              self.wfile.write("<center><br><br>Acesso nao autorizado</center></body></html>") 
              return
           self.send_response(200)
           self.send_header('Content-type','text/html; charset=utf-8') 
           self.end_headers()
           self.wfile.write("<html><head></head><body style='color:white;background-color:grey'><center>"+baseConfig[5]+" </center><br><center>"+hostname+"</center>") 
           if self.path.endswith("editaarquivo") or  self.path.endswith("executaTarefa") or self.path.endswith("logtail")or self.path.endswith("uploadprepara"):
             linha=self.path[1:4]
             coluna=self.path[4:7]

           if self.path.endswith("editaarquivo"):
             temp = config[int(linha)][int(coluna)]
             f = open(temp[2],"rb") 
             self.wfile.write("<center><form name='arquivoedit' method='POST' action='https://"+hostname+":"+baseConfig[1]+"/"+linha+coluna+"salvaarquivo'><textarea name='texto' COLS=145 ROWS=20>"+f.read()+"</textarea><br><br><button "+bstyle+" onclick=\"javascript:if (confirm('"+baseConfig[8]+"')){document.arquivoupload.submit()};return false;\">"+baseConfig[7]+"</button></form><button "+bstyle+" onclick='javascript:window.document.location=\"https://"+hostname+":"+baseConfig[1]+"/\"'>"+baseConfig[6]+"</button></center>")
             f.close()

           elif self.path.endswith("logtail"):
             temp = config[int(linha)][int(coluna)]
#TODO : Cette ligne pose problème dans certains cas.
             print temp[2]
             os.system(temp[2]+" >"+caminho+"/logtail.log")             
             f = open(caminho+"/logtail.log","r")
             self.wfile.write("<center><form name='xxx' method='POST' action=''><textarea name='texto' COLS=145 ROWS=20>"+f.read()+"</textarea><br><br></form><button "+bstyle+" onclick='javascript:window.document.location=\"https://"+hostname+":"+baseConfig[1]+"/\"'>"+baseConfig[6]+"</button></center>")
             f.close()
           elif self.path.endswith("uploadprepara"):
             temp = config[int(linha)][int(coluna)]
             self.wfile.write("<center><form name='arquivoupload' method='POST' enctype=\"multipart/form-data\" action='https://"+hostname+":"+baseConfig[1]+"/"+linha+coluna+"uploadarquivo'><br>"+temp[4]+"<br><input type=\"file\" name=\"file\" size=\""+temp[5]+"\"><br><br><button "+bstyle+" onclick=\"javascript:if (confirm('"+baseConfig[8]+"')){document.arquivoupload.submit()};return false;\">Upload</button></form><button "+bstyle+" onclick='javascript:window.document.location=\"https://"+hostname+":"+baseConfig[1]+"/\"'>"+baseConfig[6]+"</button></center>")
           elif self.path.endswith("executaTarefa"):
             # EVOCACAO DO COMANDO
             result=0
             temp = config[int(linha)][int(coluna)]
             tipo = str(temp[1])
             if (tipo == "1"):
               print "Comando call executado: "+str(temp[2])
               subprocess.call(temp[2],close_fds=True)
             elif (tipo == "2"):
               print "Comando normal executado: "+str(temp[2])
               result=os.system(temp[2])

             # TRATAMENTO DA APRESENTACAO
             if tipo == "2":
                if result == 0:                    
                   self.wfile.write("<center><br> "+temp[4]+"<br><br><button "+bstyle+" onclick='javascript:history.go(-1)'>"+baseConfig[6]+"</button></center>")  
                else:
                   self.wfile.write("<center><br> "+temp[5]+"<br><br><button "+bstyle+" onclick='javascript:history.go(-1)'>"+baseConfig[6]+"</button></center>")
             if tipo == "1":
                self.wfile.write("<center><br>"+temp[4]+"<br><br><button "+bstyle+" onclick='javascript:window.document.location=\"https://"+hostname+":"+baseConfig[1]+"/\"'>"+baseConfig[6]+"</button></center>")   


           else:
             for x in range(len(config)):
                 linha = config[x]
                 grupo = linha[0]
                 self.wfile.write("<br><br><center>")
                 for y in range(len(linha)):
                   if (y == 0):
                      self.wfile.write(linha[0])
                      self.wfile.write("<br>")
                   else:
                      botao=linha[y]
                      if (str(botao[3])=='1'):
                        confirm='confirm(\''+baseConfig[8]+'\')'
                      else:
                        confirm='true'
                    
                      if (str(botao[1])=='1'):
                        acao='executaTarefa'
                      elif (str(botao[1])=='2'):
                        acao='executaTarefa'
                      elif (str(botao[1])=='3'):
                        acao='editaarquivo'
                      elif (str(botao[1])=='4'):
                        acao='logtail'
                      elif (str(botao[1])=='5'): 
                        acao='uploadprepara'
                         
                      self.wfile.write("<button "+bstyle+" onclick=\"javascript:if ("+confirm+"){window.document.location='https://"+hostname+":"+baseConfig[1]+"/"+str(x).zfill(3)+str(y).zfill(3)+acao+"'}\">"+botao[0]+"</button>&nbsp;")
                                            
 
                      
              #     if (y == 4):   
              #       self.wfile.write("<button>"+Start+"</button>")
              #     if (y == 4):   
              #       self.wfile.write("<button>"+Start+"</button>")
             self.wfile.write("</center></body></html>") 
             #f = open(caminho+'/adminWeb.cfg', 'r')
             #self.wfile.write(f.read())
             #f.close()
           return

        except Exception , e:
            print e
            self.send_error(500,e)


    #POST USADO PARA SALVAR O ARQUIVO DE CONFIGURACAO
    def do_POST(self):
      try:
        if self.path.endswith("salvaarquivo"):
           form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],})
           self.send_response(200)
           self.send_header('Content-type','text/html; charset=utf-8')
           linha=self.path[1]
           coluna=self.path[2]
           temp = config[int(linha)][int(coluna)]
           print "Fichier sauvegardé : "+str(temp[2])
           f = open(temp[2],"wb") 
           f.write(form.getvalue("texto").replace("\r\n","\n"))
           f.close()
           self.end_headers()
           self.wfile.write("<html><head></head><body style='color:white;background-color:grey'><center>"+baseConfig[5]+"</center>") 
           self.wfile.write("</center><br><br><center>Fichier sauvegardé<br><br><button "+bstyle+" onclick='javascript:window.document.location=\"https://"+hostname+":"+baseConfig[1]+"/\"'>"+baseConfig[6]+"</button></center></body></html>") 
        elif self.path.endswith("uploadarquivo"):
           linha=self.path[1]
           coluna=self.path[2]
           temp = config[int(linha)][int(coluna)]
           form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],})
           fileitem = form['file'] 
           print "nome arquivo:"+fileitem.filename
           f = open(str(temp[2])+fileitem.filename,"wb")
           f.write(fileitem.file.read())
           f.close()
           self.send_response(200)
           self.end_headers()
           self.wfile.write("<html><head></head><body style='color:white;background-color:grey'><center>"+baseConfig[5]+"</center>")
           self.wfile.write("</center><br><br><center>"+temp[6]+"<br><br><button "+bstyle+" onclick='javascript:window.document.location=\"https://"+hostname+":"+baseConfig[1]+"/\"'>"+baseConfig[6]+"</button></center></body></html>")

      except Exception , e:
          print e
          self.send_error(500,e)          


def main ():
    try:
        server = HTTPServer(('',int(baseConfig[1])), Handler)
	server.socket = ssl.wrap_socket(server.socket, certfile=baseConfig[9], server_side=True)
        server.serve_forever()
    except Exception , e:
        server.socket.close()
        print e


if __name__ == '__main__':
    main()
            
