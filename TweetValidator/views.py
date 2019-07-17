from django.http import HttpResponse
from .forms import DocumentForm
from django.shortcuts import redirect, render

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'simple_form.html', {
        'form': form
    })
