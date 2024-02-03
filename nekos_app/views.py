from pprint import pprint
from urllib.parse import urlencode

from django.http import HttpRequest
from django.shortcuts import render, redirect
import requests as req
from django.urls import reverse


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
        "artist": image['artist']['name'] if image['artist'] is not None else None,
        "id": image["id"]
    }
    return render(request, "blocks/image_card.html", ctx)

def image_card_by_id(request: HttpRequest, id):
    image = req.get(f"https://api.nekosapi.com/v3/images/{id}").json()

    ctx = {
        "thumbnail_url": image['sample_url'],
        "tags": [tag['name'] for tag in image['tags']],
        "characters": ", ".join([character['name'] for character in image['characters']]) if image['characters'] else None,
        "artist": image['artist']['name'] if image['artist'] is not None else None,
        "id": image["id"]
    }
    return render(request, "blocks/image_card.html", ctx)


def image(request: HttpRequest, id: int):
    image = req.get(f"https://api.nekosapi.com/v3/images/{id}").json()

    ctx = {
        "id": image['id'],
        "char_id": image['characters'][0]['id'] if image['characters'] else -1,
        "image": image['image_url'],
        "tags": [tag['name'] for tag in image['tags']],
        "artist": image['artist']['name'] if image['artist'] is not None else None,
        "artist_id": image['artist']['id'] if image['artist'] is not None else -1,
        "characters": image['characters'][0]['name'] if image['characters'] else None,
    }
    return render(request, "image.html", ctx)

def character_arts(request, id):
    data = req.get(f"https://api.nekosapi.com/v3/images",
                   params={
                       "character": [id],
                       "limit": 10
                   }).json()

    ctx = {
        "images": [image['sample_url'] for image in data['items']]
    }
    return render(request, "blocks/character_arts.html", ctx)

def artist_arts(request, id):
    data = req.get(f"https://api.nekosapi.com/v3/images",
                   params={
                       "artist": [id],
                       "limit": 10
                   }).json()

    ctx = {
        "images": [image['sample_url'] for image in data['items']]
    }
    return render(request, "blocks/character_arts.html", ctx)

def search(request: HttpRequest):
    tags = req.get("https://api.nekosapi.com/v3/images/tags").json()["items"]
    characters = req.get("https://api.nekosapi.com/v3/characters").json()["items"]
    artists = req.get("https://api.nekosapi.com/v3/artists").json()["items"]

    ctx = {
        "tags": sorted(tags, key=lambda x: x["name"]),
        "characters": sorted(characters, key=lambda x: x["name"]),
        "artists": sorted(artists, key=lambda x: x["name"]),
    }

    params = dict(request.GET)
    selected_tags = params.get("tag", [])
    selected_character = params.get("character", -1)
    selected_artist = params.get("artist", -1)
    selected_rating = params.get("rating", [])
    selected_rating = list(map(lambda x: x[1:len(x)-1], selected_rating[0][1:len(selected_rating[0])-1].split(', ')))

    if request.method == "POST":
        post_data = dict(request.POST)
        query_parameters = {}
        if post_data.get("tag", []) != []:
            selected_tags = list(map(int, post_data["tag"]))
            query_parameters["tag"] = selected_tags
        if post_data.get("character", []) != []:
            selected_character = [int(post_data["character"][0])]
            query_parameters["character"] = selected_character
        if post_data.get("artist", []) != []:
            selected_artist = [int(post_data["artist"][0])]
            query_parameters["artist"] = selected_artist
        if post_data.get("rating", []) != []:
            selected_rating = post_data["rating"]
            query_parameters["rating"] = selected_rating

        base_url = reverse("search")
        query_string = urlencode(query_parameters)
        url = f"{base_url}?{query_string}"
        return redirect(url)


    tags_stringified = ('tag=[' + ','.join(selected_tags) + ']') if len(selected_tags) > 0 else ''
    rating_stringified = ('rating=[' + ','.join(selected_rating) + ']') if len(selected_rating) > 0 else ''
    character_stringified = ("character=" + str(selected_character)) if selected_character != -1 else ''
    artist_stringified = ("artist=" + str(selected_artist)) if selected_artist != -1 else ''
    link = "/search_results?" + ';'.join(filter(lambda x: x != '', [tags_stringified, character_stringified, artist_stringified, rating_stringified]))

    ctx["link"] = link

    return render(request, "search.html", ctx)

def search_results(request: HttpRequest):
    params = dict(request.GET)
    selected_tags = params.get("tag", [])
    selected_character = params.get("character", -1)
    selected_artist = params.get("artist", -1)
    selected_rating = params.get("rating", [])


    params = {
        "limit": 32
    }

    if selected_tags != []:
        params["tag"] = selected_tags
        print(selected_tags)
    if selected_character != -1:
        params["character"] = [selected_character]
    if selected_artist != -1:
        params["artist"] = [selected_artist]
    if selected_rating != []:
        params["rating"] = selected_rating[0][1:len(selected_rating[0]) - 1].split(',')

    data = req.get("https://api.nekosapi.com/v3/images",
                   params=params).json()["items"]
    print(data)

    ctx = {
        "images": data,
    }

    return render(request, "blocks/search_results.html", ctx)