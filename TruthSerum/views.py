import os
import time

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse

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
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            filepath = handle_uploaded_file(request.FILES['file'])
            html = get_embed_html('https://twitter.com/BobWulff/status/1151642928286187525')
            # return redirect(reverse('dummy'))
            return render(request, 'result.html', {
                'tweet': html,
            })
        return HttpResponseBadRequest("Image upload form not valid.")
    else:
        form = ImageUploadForm()
    return render(request, 'simple_form.html', {'form': form})

def dummy(request):
    return render(request, 'dummy.html')
