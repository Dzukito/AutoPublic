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

#### AutoPublic FullAuto Version
```
- Al arrancar ya sabe que día es sin necesidad de aclararlo
- Solo te va a preguntar a que hora de ayer lo ejecutaste. Ejemplo: 10:30 (y hace la conversión a UTC).
- Recopila entonces todos los IOC de hoy + los IOC de ayer desde las 10:31 hasta el final de dicho día.
- Si es LUNES, ni te pregunta a que hora lo ejecutaste, agarra por el mismo Sabado, Domingo y Lunes.
- Las familias de MalwareBazaar a analizar las toma de un archivo personalizable llamado familias.txt.
- Hay algunos detalles extras, como un control en el input del horario (xx:xx).
```


## Demo
https://www.youtube.com/watch?v=1g_TaxVGizk
