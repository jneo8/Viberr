# from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
# from django.http import HttpResponse
# csrf_exempt close the csrf check
from django.views.decorators.csrf import csrf_exempt
from .models import Item, List
from .forms import ItemForm, ExistingListItemForm


def home_page(request):
    return render(request, 'superlist/home.html', {'form': ItemForm()})

@csrf_exempt
def view_list(request, list_id):

    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, 'superlist/list.html', {'list': list_, 'form': form})


@csrf_exempt
def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        # if get error
        return render(request, 'superlist/home.html', {'form': form})
