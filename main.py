import tweepy
import argparse
import requests
import io
from auxiliares import seleccionar_url, NoImagenesDisponibles

# Autenticación en Twitter
def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('--consumer_key', required = True)
    parser.add_argument('--consumer_secret', required = True)
    parser.add_argument('--access_token', required = True)
    parser.add_argument('--access_token_secret', required = True)
    parser.add_argument('--bearer', required = True)

    return parser.parse_args()

def twittear_imagen(consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str, bearer: str):

    # Autenticación v1.1 api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # v2.0 api
    twclient = tweepy.Client(bearer, consumer_key, consumer_secret, access_token, access_token_secret, wait_on_rate_limit=True)
    
    try:
        url, nombre_pelicula = seleccionar_url()
    except NoImagenesDisponibles as e:
        print(f"Error: {e}")
        return

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen: {e}")
        return

    image_file = io.BytesIO(response.content)
    try:
        media_info = api.media_upload(filename='image.jpg', file=image_file)
    except tweepy.errors.TweepyException as e:
        print(f"Error al subir la imagen a Twitter: {e}")
        return

    try:
        twclient.create_tweet(text=nombre_pelicula, media_ids=[media_info.media_id])
    except tweepy.errors.Forbidden as e:
        print(f"Error 403 Forbidden al publicar el tweet.")
        print(f"Detalle: {e}")
        print("Posibles causas: permisos de la app insuficientes (necesita 'Read and Write'), "
              "credenciales incorrectas, o la cuenta está suspendida/restringida.")
        return
    except tweepy.errors.TweepyException as e:
        print(f"Error de Tweepy al publicar el tweet: {e}")
        return

def main():
    args = parseArgs()
    twittear_imagen(**vars(args))

if __name__ == "__main__":
    main()
