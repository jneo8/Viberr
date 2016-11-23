from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Stock
from .serializers import StockSerializer

# list all stock or create a new one 
# stocks/FB
class Stocklist(APIView):

    def get(self, request):
        stocks = Stock.objects.all()
        serializers = StockSerializer(stocks, many=True)
        return Response(serializers.data)

    def post(self, request):
        
        stocks = Stock.objects.create()