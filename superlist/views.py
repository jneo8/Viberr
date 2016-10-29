from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item


@csrf_exempt
def home_page(request):

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('superlist:home')
    all_item = Item.objects.all()
   
    return render(request, 'superlist/home.html', {'all_item': all_item,})

# Create your views here.
