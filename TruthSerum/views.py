from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import DocumentForm
from .backend.tweet_processing import generate_link_to_tweet, get_embed_html

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            html = get_embed_html('https://twitter.com/BobWulff/status/1151642928286187525')
            return render(request, 'result.html', {
                'tweet': html,
            })
    else:
        form = DocumentForm()
    return render(request, 'simple_form.html', {
        'form': form
    })
