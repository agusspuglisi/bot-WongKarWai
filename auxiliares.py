import random
from bs4 import BeautifulSoup
import requests

def convertir_thumbnail_filmgrab(url_sin_convertir):
    # Agrego %20 y saco el thumb para que la imagen se vea completa.

    url_modificada = url_sin_convertir.replace(' ', '%20')
    url_final = url_modificada.replace('thumb/', '')

    return url_final

def convertir_thumbnail_screenmusings(url_sin_convertir, nombre_archivo):
    # Agrego %20 y saco el thumb para que la imagen se vea completa.

    url_modificada = url_sin_convertir.replace("thumbnails", "images")
    url_final = f"https://screenmusings.org/movie/blu-ray/{nombre_archivo}/{url_modificada}"

    return url_final

def request_url(random_url):
 
    pagina = requests.get(random_url)
    soup = BeautifulSoup(pagina.content, 'html.parser')

    imagenes = soup.find_all('img')

    imagen_random = random.choice(imagenes)
    imagen_url = imagen_random['src']

    return imagen_url

def seleccionar_url():

    dic_urls = {'https://film-grab.com/2014/10/20/chungking-express/' : 'Chungking Express (1994)', 
            'https://film-grab.com/2014/09/25/fallen-angels/' : 'Fallen Angels (1995)',
            'https://film-grab.com/2014/06/22/as-tears-go-by/' : 'As Tears Go By (1995)',
            'https://film-grab.com/2014/02/19/happy-together/' : 'Happy Together (1997)',
            'https://film-grab.com/2014/02/17/days-of-being-wild/' : 'Days of Being Wild (1990)',
            'https://film-grab.com/2014/02/21/my-blueberry-nights/' : 'My Blueberry Nights (2007)',
            'https://film-grab.com/2014/02/18/ashes-of-time-redux/' : 'Ashes of Time Redux (1994)',
            'https://film-grab.com/2014/02/20/2046/' : '2046 (2000)',
            'https://film-grab.com/2013/03/09/in-the-mood-for-love/' : 'In the Mood for Love (2000)',
            'https://screenmusings.org/movie/blu-ray/Chungking-Express/' : ['Chungking Express (1994)', 'Chungking-Express'], 
            'https://screenmusings.org/movie/blu-ray/Fallen-Angels/' : ['Fallen Angels (1995)', 'Fallen-Angels'],
            'https://screenmusings.org/movie/blu-ray/Days-of-Being-Wild/' : ['Days of Being Wild (1990)', 'Days-of-Being-Wild'],
            'https://screenmusings.org/movie/blu-ray/My-Blueberry-Nights/' : ['My Blueberry Nights (2007)', 'My-Blueberry-Nights'],
            'https://screenmusings.org/movie/blu-ray/In-the-Mood-For-Love/' : ['In the Mood for Love (2000)', 'In-the-Mood-For-Love']
            }

    random_url, lista_nombre_pelicula = random.choice(list(dic_urls.items()))

    url_a_convertir = request_url(random_url)

    if random_url.startswith("https://screenmusings.org"):

        nombre_pelicula = lista_nombre_pelicula[0]
        nombre_archivo = lista_nombre_pelicula[1]
        url_final = convertir_thumbnail_screenmusings(url_a_convertir, nombre_archivo)

    elif random_url.startswith("https://film-grab.com"):

        nombre_pelicula = lista_nombre_pelicula
        url_final = convertir_thumbnail_filmgrab(url_a_convertir)

    return url_final, nombre_pelicula
