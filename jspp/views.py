from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class IndexView(View):
    template_name = 'javascript_test.html'

    def get(self, request):

        return render(request, self.template_name, {})
