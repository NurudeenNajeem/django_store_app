from django.shortcuts import render,HttpResponse, render
from django.db.models import F,Q
from django.db.models.aggregates import Count,Max,Min,Avg
from store.models import Product,OrderItem,Order

# Create your views here.
def index(request):
     queryse =  Order.objects.select_related("customer").order_by("-placed_at")[:5]
     queryset = Product.objects.aggregate(
          count=Count("id"), max_price = Max("unit_price"),min_price=Min("unit_price"))


     # print(queryset)
     context = {
          "products":queryset,
          "name":"Nurudeen"

     }
     # context ={"name":"Nurudeen"}
     return render(request, 'hello.html', {"name":"Nur","result":queryset})


     # return render(request,"hello.html",{"name":"Nurudeen Alani"})
