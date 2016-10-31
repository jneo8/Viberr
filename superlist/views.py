from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, List


@csrf_exempt
def home_page(request):

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        # return redirect('superlist:home')
        return redirect('superlist:view_list')
    return render(request, 'superlist/home.html', {})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    # items = Item.objects.filter(list=list_)
    return render(request, 'superlist/list.html', {'list': list_})

@csrf_exempt
def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)

    return redirect('superlist:view_list', list_.id)

@csrf_exempt
def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)

    return redirect('superlist:view_list', list_.id)

