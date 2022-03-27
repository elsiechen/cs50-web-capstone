from django.shortcuts import render
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from datetime import datetime, timedelta
import datetime
from .models import User, Meal, Size, Price, Address, OrderItem, Cart
import json
from django.core.serializers import serialize
from decimal import Decimal

# Create your views here.
def index(request):
    return render(request, "delivery/index.html")

@login_required
def order(request):   
    meals = Meal.objects.all()
    category = ['APPETIZER', 'ENTRE', 'DESSERT', 'SOUP', 'DRINK']
    try:
        app = Meal.objects.filter(type=category[0]).all()
    except Meal.DoesNotExist:
        app = None
    try:
        ent = Meal.objects.filter(type=category[1]).all()
    except Meal.DoesNotExist:
        ent = None    
    try:
        des = Meal.objects.filter(type=category[2]).all()
    except Meal.DoesNotExist:
        des = None
    try:
        sou = Meal.objects.filter(type=category[3]).all()
    except Meal.DoesNotExist:
        sou = None
    try:
        dri = Meal.objects.filter(type=category[4]).all()
    except Meal.DoesNotExist:
        dri = None

    return render(request, 'delivery/order.html', {
        "meals": meals,
        "app": app,
        "ent": ent,
        "des": des,
        "sou": sou,
        "dri": dri
    })        
   

@login_required
def orderitem(request, item_id):
    if request.method == "POST":
        data = json.loads(request.body)
        qty = data.get("item_qty")
        size = data.get("item_size")
        price = data.get("item_price")

        current_user = User.objects.get(id=request.user.id)
        item = Meal.objects.get(id=item_id)
        item_size = Size.objects.get(id=size)
        
        OrderItem.objects.create(user=current_user, meal=item, size=item_size, price=price, qty=qty).save()
        order_item = OrderItem.objects.filter(user=current_user).order_by('-id')[0]
        
        # Set and save session of itemid
        if "itemid" not in request.session:
            request.session['itemid'] = []
        request.session['itemid'].append(order_item.id)
        request.session.modified = True
        print(f"request.session['itemid']: {request.session['itemid']}")

        return JsonResponse({"order_id": order_item.id})


@login_required
def updateitem(request, item_id):
    if request.method == "POST":
        data = json.loads(request.body)
        updateqty = data.get("item_qty")
        print(updateqty)
        item = OrderItem.objects.get(id=item_id)
        # Delete item if updateqty=0 
        if int(updateqty) == 0:
            item.delete()
            # Find the index of item_id in list of session
            id_list = request.session["itemid"]
            index = id_list.index(item_id)
            print(index)
            #Delete itemid in session
            request.session["itemid"].pop(index)
            request.session.modified = True
            # Sum the total order item qty 
            item_id_list = request.session["itemid"]
            print(f"item_id_list:{item_id_list}")
            items = OrderItem.objects.filter(id__in=item_id_list)
            qty_sum = 0
            for i in items:
                qty_sum += int(i.qty)
            total_qty = int(qty_sum) 
        # Update item qty if updateqty != 0        
        if int(updateqty)>0:
            item.qty = updateqty
            item.save()
            # Sum the total order item qty 
            ## Get other order items except this(id=item_id), sum their qtys first, then add them with the updateqty           
            ### Find the index of item_id in list of session
            id_list = request.session["itemid"]
            index = id_list.index(item_id)
            print(index)
            item_id_list = request.session["itemid"]
            item_id_list.pop(index)
            request.session.modified = True
            items = OrderItem.objects.filter(id__in=item_id_list)
            qty_sum = 0
            for i in items:
                qty_sum += int(i.qty)
            total_qty = int(qty_sum) + int(updateqty)
            # Add back the item_id in session
            item_id_list.append(item_id)
            request.session.modified = True

        # Update the fields: subtotal, delivery, tax, total
        id_list = request.session['itemid']
        try:    
            orderitems = OrderItem.objects.filter(id__in=id_list)
        except OrderItem.DoesNotExist:
            orderitems = None

        subtotal = Decimal(0.00)
        for i in orderitems:
            total = i.price*i.qty
            subtotal += total   
        subtotal = round(subtotal, 2)
        # $2.5 <=delivery fee = subtotal*2% <= $5.0
        d_fee = subtotal*Decimal(0.02)
        if d_fee < 2.5:
            d_fee = 2.5
        if d_fee > 5.0:
            d_fee = 5.0
        d_fee = round(d_fee,2)
        tax = round(subtotal*Decimal(0.06), 2)
        total = round(Decimal(subtotal) + Decimal(d_fee) + Decimal(tax), 2)
        print(f"tax: {tax}")
        print(f"subtotal: {subtotal}")
        print(f"d_fee: {d_fee}")
        return JsonResponse({"status": "Update successfully!",
                             "total_qty": total_qty,
                             "subtotal": subtotal,
                             "d_fee": d_fee,
                             "tax": tax,
                             "total": total,
                             "updateqty": updateqty
                            })


@login_required
def cart(request):
    now = datetime.datetime.now()
    today = now.strftime("%B %d %Y")
    tomorrow = str((now + timedelta(days=1)).strftime("%B %d %Y"))
    third_day = str((now + timedelta(days=2)).strftime("%B %d %Y"))
    forth_day = str((now + timedelta(days=3)).strftime("%B %d %Y"))
    fifth_day = str((now + timedelta(days=4)).strftime("%B %d %Y"))
    sixth_day = str((now + timedelta(days=5)).strftime("%B %d %Y"))
    seventh_day = str((now + timedelta(days=6)).strftime("%B %d %Y"))

    # Check if session of itemid exist, if yes, access the value and get the order items
    if "itemid" not in request.session:
        request.session['itemid'] = []
        items = None
    else:
        itemid_list = request.session['itemid']
        try:    
            items = OrderItem.objects.filter(id__in=itemid_list)
        except OrderItem.DoesNotExist:
            items = None

    if items == None:
        subtotal = 0
        d_fee = 0
        tax = 0
        total = 0
    else:
        subtotal = Decimal(0.00)
        for i in items:
            total = i.price*i.qty
            subtotal += total   
        subtotal = round(subtotal, 2)
        # $2.5 <=delivery fee = subtotal*2% <= $5.0
        d_fee = subtotal*Decimal(0.02)
        if d_fee < 2.5:
            d_fee = 2.5
        if d_fee > 5.0:
            d_fee = 5.0
        d_fee = round(d_fee, 2)
        tax = round(subtotal*Decimal(0.06), 2)
        total = round(Decimal(subtotal) + Decimal(d_fee) + Decimal(tax), 2)

    if request.method == "POST":
        current_user = User.objects.get(id=request.user.id)
        created_time = datetime.datetime.now()    

        date = request.POST.get("date", False)        
        time = request.POST.get("time", False)
        # Delivery now returns time with "False" value
        if time == False:
            d_time = date
        else:
            d_time = date + time

        address = request.POST.get("address", False)
        utensils = request.POST.get("utensils", False)
        note = request.POST.get("note", False)

        itemid_list = request.session['itemid']
        try:    
            items = OrderItem.objects.filter(id__in=itemid_list)
        except OrderItem.DoesNotExist:
            items = None
        subtotal = Decimal(0.00)
        for i in items:
            amount = i.price*i.qty
            subtotal += amount 
        subtotal = round(subtotal, 2)
        # $2.5 <=delivery fee = subtotal*2% <= $5.0
        d_fee = subtotal*Decimal(0.02)
        if d_fee < 2.5:
            d_fee = 2.5
        if d_fee > 5.0:
            d_fee = 5.0
        d_fee = round(d_fee, 2)
        tax = round(subtotal*Decimal(0.06), 2)
        total = round(Decimal(subtotal) + Decimal(d_fee) + Decimal(tax), 2)
       
        newcart = Cart(user=current_user, 
                    created_time=created_time, 
                    delivery_time= d_time, 
                    address=address, 
                    fee=d_fee, 
                    subtotal=subtotal, 
                    tax=tax, 
                    total=total,
                    utensils=utensils,                   
                    note=note
                    )
        newcart.save()
        print(newcart)
        ### Save orderitems to manytomanyfield in cart
        orderitems = OrderItem.objects.filter(id__in=itemid_list)
        for i in orderitems:
            newcart.orderitems.add(i) 
        # Delete session key of itemid
        del request.session['itemid']
        request.session.modified = True
        print(f"itemid_list: {itemid_list}")
        return HttpResponseRedirect(reverse("success"))
    
    return render(request, 'delivery/cart.html', {
        "today": today,
        "tomorrow": tomorrow,
        "third_day": third_day,
        "forth_day": forth_day,
        "fifth_day": fifth_day,
        "sixth_day": sixth_day,
        "seventh_day": seventh_day,
        "items": items,
        "subtotal": subtotal,
        "d_fee": d_fee,
        "tax": tax,
        "total": total
    })  

@login_required
def success(request):
    current_user = User.objects.get(id=request.user.id)
    try:    
        order = Cart.objects.filter(user=current_user).latest('id')
    except OrderItem.DoesNotExist:
        order = None 
    return render(request, 'delivery/success.html', {
        "order": order,
        "user": current_user
    })

@login_required
def orders(request):
    current_user = User.objects.get(id=request.user.id)
    try:    
        orders = Cart.objects.filter(user=current_user).order_by('-id')
    except OrderItem.DoesNotExist:
        orders = None
    for i in orders:
        print(f"orderitems: {i.orderitems}")
    return render(request, 'delivery/orders.html', {
        "orders": orders
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "delivery/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "delivery/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "delivery/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "delivery/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "delivery/register.html")


