from pprint import pprint

from django.http import HttpRequest
from django.shortcuts import render
import requests as req

# Create your views here.
def index(request: HttpRequest):
    random_girls = req.get("https://api.nekosapi.com/v3/images/random",
                           params={
                               "rating": ["safe", "suggestive"],
                               "limit": 5
                           }).json()
    ctx = {
        "random_girls": random_girls
    }
    return render(request, "index.html", random_girls)


def random_girl(request: HttpRequest):
    image = req.get("https://api.nekosapi.com/v3/images/random",
                    params={
                        "rating": ["safe"],
                        "limit": 1
                    }).json()['items'][0]

    ctx = {
        "thumbnail_url": image['sample_url'],
        "tags": [tag['name'] for tag in image['tags']],
        "characters": ", ".join([character['name'] for character in image['characters']]) if image['characters'] else None,
        "artist": image['artist']['name'] if image['artist'] is not None else None
    }
    return render(request, "blocks/image_card.html", ctx)


def image(request: HttpRequest, id: int):
    return