from urllib import request
import pandas as pd #pip install pandas
pd.options.mode.chained_assignment = None  #Sirve para quitar un warning molesto

from bs4 import BeautifulSoup as bs #para hacer scrapping
import requests


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
  local_file="/Users/Fede y Nico/Desktop/fuenteFeodo.csv"
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
  
  request.urlretrieve(remote_url, local_file)

  #Abro el archivo de Feodo como dataframe
  data=pd.read_csv(local_file,skiprows=8)

  #lo filtro por fecha
  dataRequerida=data[(data.first_seen_utc.str[:4]=="2022") & (data.first_seen_utc.str[5:7]==mes) & (data.first_seen_utc.str[8:10]==dia)]
  if(dataRequerida.empty):
    print("<!>: No se obtuvieron IOCs en Feodo. Checkear que se haya usado formato mm o dd para el input o revisar manualmente el CSV para verificar que no hay resultados.")
    return pd.DataFrame(columns=['IOC', 'Type', 'Family', 'Source'])

  else:  
    #Tomo las columnas de IP y Family que son las que me importan
    ipsLimpias=dataRequerida[["dst_ip","malware"]]

    #Le agrego una columna source y otra IP
    ipsLimpias["Type"]="IP"
    ipsLimpias["Source"]="https://feodotracker.abuse.ch/blocklist/#iocs"

    #Las ordeno para que quede bonito a como quiero
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
        #print(c[0].string[0:11], c[1].string[0:200]) #print(c[0])

        samples.append([c[0].string[0:11],c[1].string[0:200]]) #guardame la columna fecha y hash por c/fila
        
  return samples


#scrapping por c/familia
def malbazaar():
  print("")
  print("[Public]: Se inicio MALWARE BAZAAR;")
  tag=["qakbot","bumblebee","dridex","bazaloader","log4j"]
  
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
  
  dataRequerida=data[(data.Fecha.str[:4]=="2022") & (data.Fecha.str[5:7]==mes) & (data.Fecha.str[8:10]==dia)]
  if(dataRequerida.empty):
    print("<!>: No se obtuvieron IOCS en MalwareBazaar. Checkear que se haya usado formato mm o dd para el input o revisar manualmente el CSV para verificar que no hay resultados.")
    return pd.DataFrame(columns=['IOC', 'Type', 'Family', 'Source'])
  else:
    dataRequerida = dataRequerida[['IOC', 'Type', 'Family', 'Source']]
    print("[MalBaz]: Hashes recopilados con exito!")
    print("")
    return dataRequerida

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
                >v1.0 2022-05-15                                                                                   
               
    '''


    print("{}".format(textoBaner))
#==============================================================================================   
#                                                                      
#                                        MAIN             
#                            
#==============================================================================================
banner()
#Filtro por la fecha que me importa (Atencion: Ojo los Lunes de ejecutarlo para Sabado y Domingo)
#Atencion 2: Checkear la fecha de ayer si entraron IOCs mientras no trabajabamos y hay que agregarlos hoy
print("<?>: Ingresa el Mes en formato mm: ")
mes=input()
print("<?>: Ingresa el Dia en formato dd: ")
dia=input()
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
