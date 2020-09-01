from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,orders,OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from . import Checksum
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'merchant key'

# Create your views here.
def index(request):
   
    allProduct = []
    catprods = Product.objects.values('category', 'id') #<QuerySet [{'category': 'Shoes', 'id': 8}, {'category': 'Shoes', 'id': 9}]>
    
    cats = {item['category'] for item in catprods} #cats {'Shoes', 'Earphon', 'Earphone'}
    
    for cat in cats:
        products = Product.objects.filter(category=cat)
        print(products)
        n = len(products)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProduct.append([products, range(1, nSlides)]) #, nSlides
    context={"allproduct":allProduct}
    print("all product",allProduct)
    return render(request,'home.html',context)
def searchquery(item,query):
    if query in item.product_name.lower() or query in item.desc.lower() or query in item.category.lower():
        return True
    else:
        return False
def search(request):
    query=request.GET.get('query')
    allProduct = []
    catprods = Product.objects.values('category', 'id') #<QuerySet [{'category': 'Shoes', 'id': 8}, {'category': 'Shoes', 'id': 9}]>
    cats = {item['category'] for item in catprods} #cats {'Shoes', 'Earphon', 'Earphone'}
    
    for cat in cats:
        products = Product.objects.filter(category=cat)
        prod=[item for item in products if searchquery(item,query)]

        print(products)
        n = len(prod)
        if n>0:
                
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProduct.append([prod, range(1, nSlides)]) #, nSlides
    context={"allproduct":allProduct,'msg':""}
    print("all product",allProduct)
    if len(allProduct) == 0 or len(query)<4:
        context = {'msg': "Please make sure to enter relevant search query"}
    return render(request,'search.html',context)

def about(request):
    return HttpResponse("Its about")

def contact(request):
    return HttpResponse("Hello contact")
def tracker(request):
    
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        
        try:
            order = orders.objects.filter(order_id=orderId, email=email)
            print(order)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemJson": order[0].items_json}, default=str)
                
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'tracker.html')


def checkout(request):
    if request.method=='POST':
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        address=request.POST.get('address','')+" "+request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        itemjson=request.POST.get('itemsJson','')
        amount=request.POST.get('amount','')


        
        order=orders(amount=amount,items_json=itemjson,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
        order.save()
        thank=True
        id=order.order_id
         # return render(request, 'market/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'Merchant id',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/market/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'checkout.html')


    return render(request,'checkout.html')

def product(request,id):
    prod=Product.objects.filter(id=id).first()
    context={"product":prod}
    print(product)
    return render(request,'product.html',context)
@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

