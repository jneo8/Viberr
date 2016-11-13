from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, List
from .forms import ItemForm, EMPTY_ITEM_ERROR



def home_page(request):
    return render(request, 'superlist/home.html', {'form': ItemForm()})

@csrf_exempt
def view_list(request, list_id): 
    try:
        list_ = List.objects.get(id=list_id)
        form = ItemForm()
        if request.method == 'POST':
            form = ItemForm(data=request.POST)
            if form.is_valid():
                Item.objects.create(text=request.POST['text'], list=list_)
                return redirect(list_)
        return render(request, 'superlist/list.html', {'list': list_, 'form': form})

    except:
        return render(request, 'superlist/home.html', {'form': form})

@csrf_exempt
def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        # if get error
        return render(request, 'superlist/home.html', {'form': form})


