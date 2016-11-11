from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, List
from .forms import ItemForm



def home_page(request):

    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['text'])
    #     # return redirect('superlist:home')
    #     return redirect('superlist:view_list')
    return render(request, 'superlist/home.html', {'form': ItemForm()})

@csrf_exempt
def view_list(request, list_id):
    error = None
    try:
        list_ = List.objects.get(id=list_id)

        if request.method == 'POST':
            try:
                item = Item(text=request.POST['text'], list=list_)
                item.full_clean()
                item.save()
                return redirect(list_)
            except ValidationError:
                error = "You can't have an empty list item"
        return render(request, 'superlist/list.html', {'list': list_, 'error': error})

    except:
        return render(request, 'superlist/home.html', {})

    # # items = Item.objects.filter(list=list_)
    # return render(request, 'superlist/list.html', {'list': list_})


@csrf_exempt
def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'superlist/home.html', {'error': error, })
    return redirect(list_)
