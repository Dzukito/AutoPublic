# AutoPublic - Public Sources

<p align=center>

  <img src="https://i.postimg.cc/Fs9GfSsC/train-tracks-tracks.gif"/>

  <br>
  <span>Herramienta para la recolección automática de IOC en FeodoTracker y MalwareBazaar</span>
  <br>
  <br>
  <a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_2.7-green.svg"></a>
 </a>
</p>

  
## Instalación

```console
# Clonar el repo
$ git clone https://github.com/Dzukito/AutoPublic.git

# Instalar las librerias necesarias
$ pip install requests
$ pip install pandas
$ pip install beautifulsoup4
$ pip install lxml

# Entrar en el directorio del proyecto
$ cd AutoPublic

```
## Configuración

 Abrir el script en un editor e ir a la seccion de Feodo, en la linea rodeada por signos de peso $$$ y cambiar
   el path del local_file al que se desee, modificando tambien el usuario. Atención: no tocar el nombre del archivo por si acaso :)

## Uso

```console
$ python AutPublic.py
```
Ingresar mes y dia para filtrar la informacion (2022 viene por defecto)
		
> Aclaracion importante: el script trae info del dia solicitado, asi que revisar tambien el dia de ayer por si se subio algun IOC durante las horas en las que no se corrió el script para agregarlo hoy (habrá tantos CSV como días, queda en manos del analista unir la información en uno solo si se desea).


## Demo
https://www.youtube.com/watch?v=1g_TaxVGizk
