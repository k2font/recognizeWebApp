from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import PhotoForm # forms.py内のPhotoFormを読み込む
from .models import Photo

def index(request):
    template = loader.get_template('carbike/index.html')
    context = {'form':PhotoForm()}
    return HttpResponse(template.render(context, request))

def predict(request):
    if not request.method == 'POST':
        redirect('carbike:index')
    
    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError('Formが不正です')

    photo = Photo(image=form.cleaned_data['image']) # models.pyで定義されたPhotoクラスを読んで、photo変数に格納する
    predicted, percentage = photo.predict() # Photoクラスのpredict関数を呼び出さないと、実行してもモデルに適用して予測ができない。

    template = loader.get_template('carbike/result.html')

    context = {
        'photo_name': photo.image.name,
        'photo_data': photo.image_src(),
        'predicted': predicted,
        'percentage': percentage,
    }

    return HttpResponse(template.render(context, request))

def result(request):
    template = loader.get_template('carbike/result.html')
    context = {}
    return HttpResponse(template.render(context, request))