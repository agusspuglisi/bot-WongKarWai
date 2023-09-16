import tweepy
import argparse
import requests
import io
from auxiliares import seleccionar_url

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
    
    url, nombre_pelicula = seleccionar_url()
    response = requests.get(url)

    if response.status_code == 200:

        image_file = io.BytesIO(response.content)
        media_info = api.media_upload(filename = 'image.jpg', file = image_file)

        twclient.create_tweet(text = nombre_pelicula, media_ids = [media_info.media_id])

def main():
    args = parseArgs()
    twittear_imagen(**vars(args))

if __name__ == "__main__":
    main()
