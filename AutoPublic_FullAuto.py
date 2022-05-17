
   
from urllib import request
import pandas as pd #pip install pandas
pd.options.mode.chained_assignment = None  #Sirve para quitar un warning molesto

from bs4 import BeautifulSoup as bs #para hacer scrapping
import requests

import datetime
def formatoFecha(fecha):
  if(fecha<10):
    return "0"+str(fecha)
  else: 
    return str(fecha)


#==============================================================================================   
#                                                                      
#                                  FEODO             
#                            
#==============================================================================================
def feodo():
  print("--------------------------------------------------------------------------")
  print("[Public]: Se inicio FEODO;")
#Descargo es CSV de la web feodo
  remote_url="https://feodotracker.abuse.ch/downloads/ipblocklist_aggressive.csv"

#Path donde se guarda el CSV de feodo que siempre se descarga
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
  local_file="./fuenteFeodo.csv"
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
  
  request.urlretrieve(remote_url, local_file)

  #Abro el archivo de Feodo como dataframe
  data=pd.read_csv(local_file,skiprows=8)[:-1] #skiprows para eliminar los detalles de feodo y [:-1] para eliminar el #END 

  #los IOC de hoy
  dataHoy=data[(data.first_seen_utc.str[:4]==anio) & (data.first_seen_utc.str[5:7]==mes) & (data.first_seen_utc.str[8:10]==dia)]
  
  #si es lunes, traeme los IOCs de el sabado y el domingo
  if(datetime.datetime.today().weekday()==0):
    dataDomingo=data[(data.first_seen_utc.str[:4]==anio) & (data.first_seen_utc.str[5:7]==mes)  & (data.first_seen_utc.str[8:10]==str(int(dia)-1))]
    dataSabado=data[(data.first_seen_utc.str[:4]==anio) & (data.first_seen_utc.str[5:7]==mes)  & (data.first_seen_utc.str[8:10]==str(int(dia)-2))]
    dataAyer=pd.concat([dataDomingo,dataSabado])

  #si es dia de semana, traeme los de ayer, ya sea: si lo ejecute a las 10:20, los que se subieron de 10:20 a 11:00 y de 11:00 a el fin del dia.
  else:
    dataAyerOtrasHoras=data[(data.first_seen_utc.str[:4]==anio) & (data.first_seen_utc.str[5:7]==mes)  & (data.first_seen_utc.str[8:10]==str(int(dia)-1)) & (data.first_seen_utc.str[10:13].astype(int)>int(hora))]
    dataAyerOtrosMinutos=data[(data.first_seen_utc.str[:4]==anio) & (data.first_seen_utc.str[5:7]==mes)  & (data.first_seen_utc.str[8:10]==str(int(dia)-1)) & (data.first_seen_utc.str[10:13].astype(int)==int(hora)) & (data.first_seen_utc.str[14:16].astype(int)>int(minutos))]
    dataAyer=pd.concat([dataAyerOtrasHoras,dataAyerOtrosMinutos])
    
  dataRequerida=pd.concat([dataHoy,dataAyer])

  #si no obtuve ningun IOC
  if(dataRequerida.empty):
    print("<!>: No se obtuvieron IOCs en Feodo. Checkear que se haya usado formato mm o dd para el input o revisar manualmente el CSV para verificar que no hay resultados.")
    return pd.DataFrame(columns=['IOC', 'Type', 'Family', 'Source'])

  else:  
    #Tomo las columnas de IP y Family del CSV que son las que me importan
    ipsLimpias=dataRequerida[["dst_ip","malware"]]

    #Le agrego una columna source y otra IP
    ipsLimpias["Type"]="IP"
    ipsLimpias["Source"]="https://feodotracker.abuse.ch/blocklist/#iocs"

    #Las ordeno para que quede bonito el orden a como quiero
    ipsLimpias.rename(columns = {'dst_ip':'IOC', 'malware':'Family'}, inplace = True)
    ipsLimpias = ipsLimpias[['IOC', 'Type', 'Family', 'Source']]
    
    print("[Feodo]: IPs recopiladas con exito!")
    return ipsLimpias




#==============================================================================================   
#                                                                      
#                                  MALWARE BAZAAR             
#                            
#==============================================================================================
from bs4 import BeautifulSoup as bs #para hacer scrapping
import requests #para realizar peticiones al sitio web y obtener la informacion
import pandas as pd

#Obtener fechas e IOCs de una tabla de MalwareBazaar (uso beautifulSoup)
def scrapearTabla(url):
  r = requests.get(url)
  soup= bs(r.content, features="lxml")
  info_box= soup.find(id="samples") #las tablas tienen ese id en el HTML de la pagina, asi es como la localiza :)
  inforows=info_box.find_all("tr") #encontrame fila por fila

  
  samples = [[]]
  for index,row in enumerate(inforows): #por cada fila de la tablita
      if(row.find("td")):
        c= row.find_all("td") #encontrame todos los <td>, esto es una lista con todas las columnas de una fila (fecha,hash,tipo,autor,etc...)
        #print(c[0].string[10:13], c[1].string[0:200]) #print(c[0])

        samples.append([c[0].string[0:17],c[1].string[0:200]]) #guardame la columna fecha y hash por c/fila
        
  return samples


#scrapping por c/familia
def malbazaar():
  print("")
  print("[Public]: Se inicio MALWARE BAZAAR;")
  tag=[]
  with open("./familias.txt","r") as f:
    tag = f.read().splitlines()
     
  
  dataFramesAUnir= []
  for familia in tag: 
    print("[MalBaz]: Recolectando IOCs de "+familia)
    fechaHash=scrapearTabla("https://bazaar.abuse.ch/browse.php?search=tag%3A"+familia)
    df = pd.DataFrame(fechaHash, columns=['Fecha', 'IOC'])
    df["Family"]=familia
    df["Source"]="https://bazaar.abuse.ch/browse.php?search=tag%3A"+familia
    dataFramesAUnir.append(df)

  data = pd.concat(dataFramesAUnir)
  data["Type"]="Artifact"

  data=data.dropna() #hay que eliminar unos missing values que surgen de la concatenacion y no aportan nada
  
  #los IOC de hoy
  dataHoy=data[(data.Fecha.str[:4]==anio) & (data.Fecha.str[5:7]==mes) & (data.Fecha.str[8:10]==dia)]
  
  #si es Lunes, agarrame los del Sabado y domingo
  if(datetime.datetime.today().weekday()==0):
    dataDomingo=data[(data.Fecha.str[:4]==anio) & (data.Fecha.str[5:7]==mes)  & (data.Fecha.str[8:10]==str(int(dia)-1))]
    dataSabado=data[(data.Fecha.str[:4]==anio) & (data.Fecha.str[5:7]==mes)  & (data.Fecha.str[8:10]==str(int(dia)-2))]
    dataAyer=pd.concat([dataDomingo,dataSabado])

  #si es dia de semana, traeme los de ayer, ya sea: si lo ejecute a las 10:20, los que se subieron de 10:20 a 11:00 y de 11:00 a el fin del dia. 
  else:
    print(data.Fecha.str[14:16])
    dataAyerOtrasHoras=data[(data.Fecha.str[:4]==anio) & (data.Fecha.str[5:7]==mes)  & (data.Fecha.str[8:10]==str(int(dia)-1)) & (data.Fecha.str[10:13].astype(int)>int(hora))]
    dataAyerOtrosMinutos=data[(data.Fecha.str[:4]==anio) & (data.Fecha.str[5:7]==mes)  & (data.Fecha.str[8:10]==str(int(dia)-1)) & (data.Fecha.str[10:13].astype(int)==int(hora)) & (data.Fecha.str[14:16].astype(int)>int(minutos))]
    dataAyer=pd.concat([dataAyerOtrasHoras,dataAyerOtrosMinutos])
    


  dataRequerida=pd.concat([dataHoy,dataAyer])

  if(dataRequerida.empty):
    print("<!>: No se obtuvieron IOCS en MalwareBazaar. Checkear que se haya usado formato mm o dd para el input o revisar manualmente el CSV para verificar que no hay resultados.")
    return pd.DataFrame(columns=['IOC', 'Type', 'Family', 'Source'])
  else:
    dataRequerida = dataRequerida[['IOC', 'Type', 'Family', 'Source']]
    print("[MalBaz]: Hashes recopilados con exito!")
    print("")
    return dataRequerida




#==============================================================================================   
#                                                                      
#                                  BANNER            
#                            
#==============================================================================================
def banner():
    textoBaner= '''      
   █████████               █████             ███████████             █████     ████   ███          
  ███░░░░░███             ░░███             ░░███░░░░░███           ░░███     ░░███  ░░░           
 ░███    ░███  █████ ████ ███████    ██████  ░███    ░███ █████ ████ ░███████  ░███  ████   ██████ 
 ░███████████ ░░███ ░███ ░░░███░    ███░░███ ░██████████ ░░███ ░███  ░███░░███ ░███ ░░███  ███░░███
 ░███░░░░░███  ░███ ░███   ░███    ░███ ░███ ░███░░░░░░   ░███ ░███  ░███ ░███ ░███  ░███ ░███ ░░░ 
 ░███    ░███  ░███ ░███   ░███ ███░███ ░███ ░███         ░███ ░███  ░███ ░███ ░███  ░███ ░███  ███
 █████   █████ ░░████████  ░░█████ ░░██████  █████        ░░████████ ████████  █████ █████░░██████ 
░░░░░   ░░░░░   ░░░░░░░░    ░░░░░   ░░░░░░  ░░░░░          ░░░░░░░░ ░░░░░░░░  ░░░░░ ░░░░░  ░░░░░░  
    
		>Collections: Public Sources                                                                                               
                >FeodoTracker & MalwareBazaar                                                                                   
                >v2.1 FullAuto 2022-05-17                                                                                   
               
    '''


    print("{}".format(textoBaner))
#==============================================================================================   
#                                                                      
#                                        MAIN             
#                            
#==============================================================================================
banner()

dia=formatoFecha(datetime.datetime.today().day)
mes=formatoFecha(datetime.datetime.today().month)
anio=str(datetime.datetime.today().year)
hora="00"
minutos="00"

print("[AutoPublic]: Hoy es "+datetime.datetime.today().strftime('%Y-%m-%d'))
print(" ")
if(datetime.datetime.today().weekday()!=0):
   print("<?>: Ingresa la hora en la que se ejecuto AutoPublic ayer (hh:mm): ")
   hora=input()
   minutos= hora[3:]
   hora=str(int(hora[:2])+3) #sumar el UTC de diferencia horaria

print("<?>: Ingresa el nombre del CSV a guardar (sin .csv) ")
archivo=input()


#Ejecuto los modulos correspondientes y los guardo en un csv
ipsfeodo=feodo()
artifacts=malbazaar()

result = pd.concat([ipsfeodo,artifacts])
result.to_csv(archivo+".csv",index=False)
print("==========================================================================================")
print("")
print(result)
