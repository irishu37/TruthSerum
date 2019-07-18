import os
import time

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ImageUploadForm
from .backend.tweet_processing import generate_link_to_tweet, get_embed_html
from .settings import MEDIA_ROOT

def handle_uploaded_file(file):
    folder = time.strftime('%Y_%m_%d')
    location = os.path.join(MEDIA_ROOT, folder)
    fs = FileSystemStorage(location=location)
    orig_filename = file.name
    filepath = os.path.join(location, fs.save(orig_filename, file))
    return filepath

def index(request):
    if request.method == 'POST' and request.FILES['file']:
        filepath = handle_uploaded_file(request.FILES['file'])
        html = get_embed_html('https://twitter.com/BobWulff/status/1151642928286187525')
        return render(request, 'result.html', {
            'tweet': html,
        })
    else:
        form = ImageUploadForm()
    return render(request, 'simple_form.html', {
        'form': form
    })
