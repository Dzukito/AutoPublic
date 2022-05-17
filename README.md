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

## Uso

```console
$ python AutPublic.py
```
Ingresar mes y dia para filtrar la informacion (2022 viene por defecto)
		
> Aclaracion importante: el script trae info del dia solicitado, asi que revisar tambien el dia de ayer por si se subio algun IOC durante las horas en las que no se corrió el script para agregarlo hoy (habrá tantos CSV como días, queda en manos del analista unir la información en uno solo si se desea). Esto se soluciona en AutoPublic2days, pero NO contempla el Caso Lunes donde se necesita sabado y domingo.

> AutoPublic FullAuto contempla Caso Lunes y agrega automatización completa, pero pierde libertad a la hora de checkear fechas pasadas.


## Demo
https://www.youtube.com/watch?v=1g_TaxVGizk
