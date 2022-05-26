# https://2ch.hk/fag/catalog.json
import json
import requests
import urllib
import os
import sys
import time
import socket


def open_thread(url):
    if requests.get(url) is None:
        urls.remove('url')
        return None
    json_string = json.loads(requests.get(url).text)

    return json_string


def find_files(json_string):
    #   returns list of json for each file
    #       [{
    #       'filename': '16407214590472.mp4',
    #       'md5': 'e35a584a479ce803147e3390c6fcdfab',
    #       'file_path': '2ch.hk/b/src/267865956/16523432156430.mp4',
    #       'file_thumbnail': '/b/thumb/267865956/16523432156430s.jpg'
    #       }]

    current_thread = json_string.get('current_thread')
    files_base = []
    threads = json_string.get('threads')[0]
    posts = threads.get('posts')
    for post in posts:
        files = post.get('files')
        for file in files:
            file_parameters = {
                'thread': current_thread,
                'filename': file.get('displayname'),
                'md5': file.get('md5'),
                'file_path': 'https://2ch.hk' + file.get('path'),
                'file_thumbnail': file.get('thumbnail')
            }
            files_base.append(file_parameters)
    return (files_base)


def is_downloadable(file):
    dictionary = requests.get(file.get('file_path'), stream=True).headers
    content_types = ['video/mp4', 'video/webm', 'image/jpeg', 'image/png', 'image/gif']
    txt = open('md5.txt', 'r')
    md5_list = txt.read()
    txt.close()
    if dictionary.get('Content-Type').split(';')[0] in content_types:
        if file.get('md5') in md5_list.split('\n'):
            return False
        else:
            return True
    else:
        return False


def download_file(dict_file):
    if not os.path.exists('./' + dict_file.get('thread')):
        os.mkdir('./' + dict_file.get('thread'))
    urllib.request.urlretrieve(dict_file.get('file_path'),
                               './' + dict_file.get('thread') + '/' + dict_file.get('filename'))

    txt = open('md5.txt', 'a')
    txt.write(dict_file.get('md5') + '\n')
    txt.close()
    return


if __name__ == '__main__':
    while True:
        urls = ['https://2ch.hk/b/res/268151078.json',
                ]
        # url = 'https://2ch.hk/b/res/268037208.html'
        for url in urls:
            json_string = open_thread(url)  # dict
            if json_string is None:
                pass
            else:
                files = find_files(json_string)  # list of dicts
                print(files[0].get('thread'))
                for file in files:
                    if is_downloadable(file):
                        print(file.get('filename'))
                        download_file(file)
    time.sleep(10 * 60)
