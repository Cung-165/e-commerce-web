from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_item
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_item':0}
        cartItems=order['get_cart_item']
    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return render(request,'store/store.html',context)
def Cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_item
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_item':0}
        cartItems=order['get_cart_item']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/Cart.html',context)
def CheckOut(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_item
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_item':0,'shipping':False}
        cartItems=order['get_cart_item']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/CheckOut.html',context)


def updateItem(request):
    data=json.loads(request.body)
    productId=data['productID']
    action=data['action']
    print('Action: ',action)
    print('Product: ',productId)

    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

    if action=='add':
        orderItem.quantity+=1
    elif action=='remove':
        orderItem.quantity-=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('item was added',safe=False)
def processOrder(request):
    print('Data: ',request.body)
    data=json.loads(request.body)
    transaction_id=datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        total=float(data['form']['total'])
        order.transaction_id=transaction_id
        if total == order.get_cart_total:
            order.complete=True
        order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(
                Customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode']
            )
    else:
        print('User is not to login...')
    print(transaction_id)
    return JsonResponse('payment',safe=False)