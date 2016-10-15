from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home_page(request):
    return render(request, 'superlist/home.html', {
        'new_item_text': request.POST.get('item_text', '')
        })

# Create your views here.
