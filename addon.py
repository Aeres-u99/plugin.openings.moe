import xbmc,xbmcgui
import random
import sys
import os
from xbmcswift2 import Plugin
from bs4 import BeautifulSoup
import requests
import json

plugin = Plugin()

def get_current_url():
    """
    Create a URL for calling the site again and again to get the currently playing
    video.
    """
    file = requests.get("https://openings.moe/", allow_redirects = True)
    print("-----------------------------------------------")
    soup = BeautifulSoup(file.text, "html.parser")
    temp = []
    for download in soup.find_all("a"):
        temp.append(download.get("href"))
    # There is always more than one video link inside, so we need the proper link.
    # Not the unnecessary one, that's important. 
    for temporarylink in temp:
        if ".mp4" in temporarylink:
            link = temporarylink
    # There aren't many mp4 links. 
    link = "https://openings.moe/"+link
    return link

def get_url_id(name):
    """
    Create a URL for calling the site again and again to get the currently playing
    video.
    """
    print(name.encode("utf-8"))
    url = "https://openings.moe/?video="+name
    file = requests.get(url, allow_redirects = True)
    soup = BeautifulSoup(file.text, "html.parser")
    temp = []
    for download in soup.find_all("a"):
        print(download)
        temp.append(download.get("href"))
    # There is always more than one video link inside, so we need the proper link.
    # Not the unnecessary one, that's important. 
    for temporarylink in temp:
        if ".mp4" in temporarylink:
            link = temporarylink
    # There aren't many mp4 links. 
    link2 = "https://openings.moe/"+link
    return link2




def fetch_json():
    """
    Fetch the json file of all anime openings, this is to be minimised, we cannot have it fetching everytime.
    One thing that I had thought was to have a button, another is to have a timestamp attached to the file
    and if the timestamp is more than three days we should refetch, ofcourse we will need two functions for the same. 
    So my plan for now is to have a button that allows fetching on demand.
    """
    try:
        cache = json.load(open("/tmp/cache.json", 'r'))
    except (IOError, ValueError):
        jsonlist = requests.get("http://openings.moe/api/list.php")
        cache = jsonlist.json()
        xbmc.log("--> fetched json", level=xbmc.LOGINFO)
        with open("/tmp/cache.json","w") as json_file:
            json.dump(cache,json_file)
            xbmc.log("--> Saved!", level=xbmc.LOGINFO)
    return cache

@plugin.route('/')
def index():
    proper_url = get_current_url()
    items = [
    {'label': "Current Stream", 'path':proper_url, 'is_playable': True},
    {'label': "Random Anime Openings and Endings", 'path': plugin.url_for(fetch_file),'is_playable': False},
    {'label': "Search", 'path': plugin.url_for(play_randomly) , 'is_playable': True},
    {'label': "OP|ED", 'path': plugin.url_for(play_list) , 'is_playable': False},
    {'label': "Force ReCache", 'path': plugin.url_for(force_recache), 'is_playable':False}
    ]

    return items
@plugin.route('/recache/')
def force_recache():
    try:
        os.listdir("/tmp")
        os.remove("/tmp/cache.json")
        xbmcgui.Dialog().ok("Force ReCache","ReCached Successfully")
    except:
        os.listdir("/tmp")
        print("Failed")
        xbmcgui.Dialog().ok("Force ReCache","ReCache Failed!","You can Manually remove it")
    return


@plugin.route('/fetch/')
def fetch_file():
    opdictionary = fetch_json()
    # We select only 25 elements in a go, just to stay light on system
    # My main intention of creating it is for streaming anime opeds on 
    # my smol rpi setup
    randomanimelist = []
    for i in range(15):
        ranlist = random.choice(list(opdictionary))
        randomanimelist.append(ranlist)
    print(randomanimelist)
    # Construct the list items, this requires parsing the json
    items = []
    for objects in randomanimelist:
        dictionary_format = {
            'label': objects['source'],
            'label2': objects['file'],
            'info': objects['file'],
            'path': get_url_id(objects['file']),
            'is_playable': True
        }
        items.append(dictionary_format)

    plugin.log.info(items)
    return items

@plugin.route('/random/')
def play_randomly():
    pass

@plugin.route('/playlist/')
def play_list():
    pass




if __name__ == '__main__':
    plugin.run()
