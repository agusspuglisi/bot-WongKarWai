import tweepy
import argparse
import requests
import os
from auxiliares import seleccionar_url

# Autenticación en Twitter
def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('--consumer_key', required = True)
    parser.add_argument('--consumer_secret', required = True)
    parser.add_argument('--access_token', required = True)
    parser.add_argument('--access_token_secret', required = True)

    return parser.parse_args()

def twittear_imagen(consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    url, nombre_pelicula = seleccionar_url()
    response = requests.get(url)

    if response.status_code == 200:

        api.update_status_with_media(filename = None, file = response.content, status = nombre_pelicula)

def main():
    args = parseArgs()
    twittear_imagen(**vars(args))

if __name__ == "__main__":
    main()
