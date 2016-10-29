from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item


@csrf_exempt
def home_page(request):

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        # return redirect('superlist:home')
        return redirect('/superlist/lists/the-only-list-in-the-world/')
    all_item = Item.objects.all()
    return render(request, 'superlist/home.html', {'all_item': all_item})

def view_list(request):
    all_item = Item.objects.all()
    return render(request, 'superlist/home.html', {'all_item': all_item})

