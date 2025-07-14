from django.shortcuts import render
from . models import products


# Create your views here.
def index(request):
    return render(request,'index.html')


def list_products(request):
    product_list=products.objects.order_by('priority')
    context={'products':product_list}
    return render(request,'products.html',context)


def products_details(request,pk):
    product=products.objects.get(pk=pk)
    context={'product':product}
    return render(request,'product_details.html',context)

