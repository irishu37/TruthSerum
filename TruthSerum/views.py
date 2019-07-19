import os
import time

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ImageUploadForm
from .backend.tweet_processing import generate_link_to_tweet, get_embed_html
from .settings import MEDIA_URL

def handle_uploaded_file(file):
    folder = time.strftime('%Y_%m_%d')
    location = os.path.join(MEDIA_URL, folder)
    fs = FileSystemStorage(location=location)
    orig_filename = file.name
    relative_path = fs.save(orig_filename, file)
    filepath = os.path.join(location, relative_path)
    return filepath

def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            filepath = handle_uploaded_file(request.FILES['file'])
            link = generate_link_to_tweet(filepath)
            if link:
                html = get_embed_html(link)
                return render(request, 'result.html', {
                    'tweet': html,
                    'image': None,
                })
            return render(request, 'result.html', {
                'tweet': None,
                'image': filepath,
            })

        return HttpResponseBadRequest("Image upload form not valid.")
    else:
        form = ImageUploadForm()
    return render(request, 'simple_form.html', {'form': form})

def dummy(request):
    return render(request, 'dummy.html')

def success(request):
    return render(request, 'result.html', {
        'tweet': get_embed_html('https://twitter.com/realDonaldTrump/status/1021234525626609666'),
        'image': None,
    })

def failure(request):
    return render(request, 'result.html', {
        'tweet': None,
        'image': 'static/images/elonmusktweet.jpg',
    })
