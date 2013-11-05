# -*- coding: UTF-8 -*-
#START  CONFIGURATION
#General Service Configuration - ip (use 0.0.0.0 and keep it generic), port , hostname(do not use,but keep the empty string) , user , password, head of the pages,label of the button that brings the main screen, label of the save button,label of the confirmation, ssl certificate
baseConfig = ['0.0.0.0','10500','','administrateur','zazovasu','École St-Michel Garicoitz','Page principale','Sauvegarder','Êtes-vous sûr ?','/etc/ssl/routeur.pem']

service = '1'
commande = '2'
editeur = '3'
rapport = '4'
fichier = '5'

config = [

           [
            'Système',
            ['Redémarrer',service,'reboot','1','Le système redémarre'],
            ['Arrêter',service,'shutdown -h now','1','Arrêt du système en cours.'],
           ],
         
           [
            'Interfaces réseau',
            ['Configurer',editeur,'/etc/network/interfaces','0'],
            ['Réinitialiser',service,['/etc/init.d/networking','restart'],'1','Assurez-vous que tout fonctionne comme prévu…'],
           ],

           [
            'Ordinateurs du réseau (dnsmasq)',
            ['Relancer',service,['/etc/init.d/dnsmasq','restart'],'0','Le serveur de noms et d\'adresses a bien redémarré'],
            ['Hôtes connus',editeur,'/etc/ethers','0'],
            ['Inconnus',rapport,"""IFS=$'\n' ; for rapport in $(nmap -T4 -sP 192.168.40.0/24 | grep 192.168.40.[09]*) ; do 
                                     dns=$(echo $rapport | cut -d" " -f5) ;
                                     grep -q $dns /etc/hosts || \
                                         nmap -T4 -sP $dns | \
                                         grep -v "Starting Nmap 6.00" | grep -v "Host is up" | grep -v "Nmap done" | \
                                         sed s/"Nmap scan report for "/""/g | sed s/"MAC Address"/"Adresse MAC "/g ;
                                     done""",'0'],
            ['Noms d\'hôtes',editeur,'/etc/hosts','0'],
           ],

           [
            'Réseau sécurisé (ipsec)',
            ['Relancer',service,['/etc/init.d/ipsec','restart'],'1','Le reseau sécurisé a bien été relancé ; assurez-vous de réamorcer les connexions des ordinateurs clients.'],
            ['Paramètres',editeur,'/etc/ipsec.conf','0'],
            ['Sécurité',editeur,'/etc/ipsec.secrets','0'],
           ],

           [
            'Serveur proxy (squid)',
            ['Arrêter',service,['/etc/init.d/squid3','stop'],'1','Vérifiez les éventuelles erreurs.'],
            ['Démarrer',service,['/etc/init.d/squid3','start'],'1','Vérifiez les éventuelles erreurs.'],
            ['Statut',commande,'ps -ef | grep -i squid| grep -vi grep','0','Proxy démarré','Proxy arrêté'],
#            ['Recharger',service,['/usr/sbin/squid','-k','reconfigure'],'1','Check the log after this operation.'],
            ['Recharger',commande,'cd /root/proxy/ && ./listes.sh','1','Vérifiez les éventuelles erreurs.'],
            ['Configurer',editeur,'/etc/squid3/squid.conf','0'],
            ['Autorisé',editeur,'/root/proxy/autorise','0'],
            ['Eleves',editeur,'/etc/squid3/conf.d/011-eleves.conf','0'],
            ['Interdit',editeur,'/root/proxy/interdit','0'],
            ['Horaires',editeur,'/root/proxy/heures','0'],
            ['Interception',editeur,'/etc/squid3/conf.d/00-ssl.conf','0'],
            ['Accès',rapport,'tail -500 /var/log/squid3/access.log','0'],
            ['Erreurs',rapport,'tail -500 /var/log/squid3/cache.log','0'],
           ],

#           [
#            'POUND',
#            ['Stop','1',['/etc/init.d/pound','stop'],'1','Check the log after this operation.'],
#            ['Start','1',['/etc/init.d/pound','start'],'1','Check the log after this operation.'],
#            ['Status','2','ps -ef | grep -i pound| grep -vi grep','0','Pound ON','Pound OFF'],
#            ['Configuration','3','/etc/pound/pound.cfg','0'],
#            ['Error Log','4','tail -500 /var/log/syslog','0'],
#           # ['Upload','5','/home/webadmin/','0','File to upload','40','File Upload OK'],
#           ],

         ]
#END - CONFIGURATION

#Per administered service configuration
#You must add an array named Config that has N child arrays for each set of buttons in the following format:
#First String with then name of the administered service 
# N Buttons of that administered service. It can be of the following types (5):

# Type 1 - "Call with screen" format (used in scripts of /etc/init.d to start/stop/reload services):
 #Label
 #Button type : 1
 #Array of command and parameters
 #1 - Has confirmation prompt 0 - do not has confirmation prompt
 #Message to present in the end of processing (no matter what happened, this message wil be shown)

#Type 2 - "System with Screen" format (used to execute scripts - like status - and capture the result):
#DANGER: DO NOT USE THIS BUTTON TO START SCRIPTS THAT WILL LAUNCH PROCESSES IN BACKGROUD(like /etc/init.d scripts) - USE TYPE 1 IN THIS CASE 
#DANGER: USE THIS TYPE TO LAUNCH SCRIPTS THAT WILL END WITHOUT going BACKGROUND 
 #Label 
 #Button type : 2
 #String with the command (can have pipes)
 #1 - Has confirmation prompt 0 - do not has confirmation prompt
 #return menssage when success
 #return message when fails

#Type 3 - "File Edit" format
 #Label 
 #Button type : 3
 #String with the file to be edited
 #1 - Has confirmation prompt 0 - do not has confirmation prompt
 
#Type 4 - "Watch result file" format (Used to run commands  that will show results - like a processing with awk  ):
 #Label 
 #Button type  : 4
 #String with the commands that will have the result piped to a known file that will be shown 
 #1 - Has confirmation prompt 0 - do not has confirmation prompt
 

#Type 5 - "File upload" format:
 #Label 
 #Button type : 5
 #Upload directory (like "/opt/test/" dont forget the bars)
 #1 - Has confirmation prompt 0 - do not has confirmation prompt
 #Message in the screen that chooses the file 
 #Size of the label that shows the file name
 #Menssage in case of success


