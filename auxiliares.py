import random
from bs4 import BeautifulSoup
import requests


class NoImagenesDisponibles(Exception):
    pass


URLS_PELICULAS = {
    # film-grab.com
    'https://film-grab.com/2014/10/20/chungking-express/'  : 'Chungking Express (1994)',
    'https://film-grab.com/2014/09/25/fallen-angels/'      : 'Fallen Angels (1995)',
    'https://film-grab.com/2014/06/22/as-tears-go-by/'     : 'As Tears Go By (1988)',
    'https://film-grab.com/2014/02/19/happy-together/'     : 'Happy Together (1997)',
    'https://film-grab.com/2014/02/17/days-of-being-wild/' : 'Days of Being Wild (1990)',
    'https://film-grab.com/2014/02/21/my-blueberry-nights/': 'My Blueberry Nights (2007)',
    'https://film-grab.com/2014/02/18/ashes-of-time-redux/': 'Ashes of Time Redux (1994)',
    'https://film-grab.com/2014/02/20/2046/'               : '2046 (2004)',
    'https://film-grab.com/2013/03/09/in-the-mood-for-love/': 'In the Mood for Love (2000)',
    'https://film-grab.com/2014/04/30/the-grandmaster/'    : 'The Grandmaster (2013)',
    'https://film-grab.com/2025/02/03/eros/'               : 'Eros (2004)',
    # scenestill.com
    'https://www.scenestill.com/films/11104': 'Chungking Express (1994)',
    'https://www.scenestill.com/films/11220': 'Fallen Angels (1995)',
    'https://www.scenestill.com/films/844'  : '2046 (2004)',
    'https://www.scenestill.com/films/843'  : 'In the Mood for Love (2000)',
}


def convertir_thumbnail_filmgrab(url_sin_convertir):
    # Agrego %20 y saco el thumb para que la imagen se vea completa.
    url_modificada = url_sin_convertir.replace(' ', '%20')
    url_final = url_modificada.replace('thumb/', '')
    return url_final


def request_url(random_url):

    try:
        pagina = requests.get(random_url, timeout=10)
        pagina.raise_for_status()
    except requests.exceptions.RequestException:
        raise NoImagenesDisponibles(f"No se pudo acceder a: {random_url}")

    soup = BeautifulSoup(pagina.content, 'html.parser')

    imagenes = [img for img in soup.find_all('img') if img.get('src')]

    if not imagenes:
        raise NoImagenesDisponibles(f"No se encontraron imágenes en: {random_url}")

    imagen_random = random.choice(imagenes)
    return imagen_random['src']


def request_url_scenestill(random_url):

    try:
        pagina = requests.get(random_url, timeout=10)
        pagina.raise_for_status()
    except requests.exceptions.RequestException:
        raise NoImagenesDisponibles(f"No se pudo acceder a: {random_url}")

    soup = BeautifulSoup(pagina.content, 'html.parser')

    imagenes = [
        img['data-full-src'] for img in soup.find_all('img')
        if img.get('data-full-src', '').startswith('https://www.scenestill.com/storage/')
    ]

    if not imagenes:
        raise NoImagenesDisponibles(f"No se encontraron imágenes en: {random_url}")

    return random.choice(imagenes)


def seleccionar_url(max_intentos=3):

    urls_disponibles = list(URLS_PELICULAS.items())

    for _ in range(max_intentos):
        random_url, nombre_pelicula = random.choice(urls_disponibles)

        try:
            if random_url.startswith('https://www.scenestill.com'):
                url_final = request_url_scenestill(random_url)

            elif random_url.startswith('https://film-grab.com'):
                url_final = convertir_thumbnail_filmgrab(request_url(random_url))

        except NoImagenesDisponibles:
            continue

        return url_final, nombre_pelicula

    raise NoImagenesDisponibles("No se encontraron imágenes válidas.")
