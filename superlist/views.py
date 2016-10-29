from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item


@csrf_exempt
def home_page(request):

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        # return redirect('superlist:home')
        return redirect('superlist:view_list')
    return render(request, 'superlist/home.html', {})

def view_list(request):
    all_item = Item.objects.all()
    return render(request, 'superlist/list.html', {'all_item': all_item})

@csrf_exempt
def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    # Item.objects.create(text='123')

    return redirect('superlist:view_list')


