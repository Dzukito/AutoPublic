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

# Instalar las librerias necesar9as
$ pip install requests
$ pip install pandas
$ pip install beautifulsoup4

# Entrar en el directorio del proyecto
$ cd AutoPublic

```
## Configuración

 Abrir el script en un editor e ir a la seccion de Feodo, en la linea rodeada por signos de peso $$$ y cambiar
   el path del local_file que se desee, cambiando el usuario. OJO: no tocar el nombre del archivo por si acaso :)

## Uso

```console
$ python AutPublic.py
```
Ingresar mes y dia para filtrar la informacion (2022 viene por defecto)
	
> Aclaracion importante 1: ojo si es lunes, correr el script para el sabado y el domingo. Al final habra 3 CSV (sabado,domingo y lunes) a los que podes unir vos mismo en 1 solo.
	
> Aclaracion importante 2: el script trae info del dia solicitado, asi que revisar tambien el dia de ayer por si se subio algun IOC fuera del trabajo y hay que agregarlo hoy (tendras 2 CSV entonces).

## Sobre el output

Si se el CSV se ve feo y queremos que se vea bonito en excel, seguir estos pasos:
	
  * Seleccionar toda la primera columna
* Ir a Datos->Texto en columnas->Delimitados (y siguiente)->Coma (y siguiente)->Texto (general aveces va masomenos)

## Demo
[![Watch the video](https://i.postimg.cc/bv4sGr4F/image.png)](https://www.youtube.com/watch?v=1g_TaxVGizk)
