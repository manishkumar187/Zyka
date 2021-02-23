from django.shortcuts import render,get_object_or_404,reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from secondapp.models import Contact_Us,Category,register_table,add_product,cart,Order
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from secondapp.forms import add_product_form
from django.db.models import Q
from datetime import datetime
from django.core.mail import EmailMessage


def index(request):
    # if "user_id" in request.COOKIES:
    #     uid = request.COOKIES["user_id"]
    #     usr = get_object_or_404(User,id=uid)
    #     login(request,usr)
    #     if usr.is_active:
    #         return HttpResponseRedirect("/cust_dashboard")
        # return HttpResponseRedirect() 
    cats = Category.objects.all().order_by("cat_name")
    return render(request,"home.html",{"category":cats})

def aboutpage(request):
    cats = Category.objects.all().order_by("cat_name")
    return render(request,"about.html",{"category":cats})

def contactpage(request):
    cats = Category.objects.all().order_by("cat_name")
    recent = Contact_Us.objects.all().order_by("-id")[:5]

    
    if(request.method == "POST"):
        nm= request.POST["name"]
        con= request.POST["contact"]
        sub= request.POST["subject"]
        msz= request.POST["message"]

        if(len(con)>10):
            res="Dear {} Please Enter 10 Digit Contact Number".format(nm)
            return render(request,"contact.html",{"status":res,"message":recent,"category":cats})
        elif(len(con)<10):
            res="Dear {} Please Enter 10 Digit Contact Number".format(nm)
            return render(request,"contact.html",{"status":res,"message":recent,"category":cats})
        elif(con.isnumeric()==False):
            res="Dear {} Please Enter 10 Digit Contact Number".format(nm)
            return render(request,"contact.html",{"status":res,"message":recent,"category":cats})
        elif(sub.isnumeric()==True):
            res="Dear {} Please Enter Valid Subject".format(nm)
            return render(request,"contact.html",{"status":res,"message":recent,"category":cats})
        elif(nm.isnumeric()==True):
            res="Dear {} Please Enter Valid name".format(nm)
            return render(request,"contact.html",{"status":res,"message":recent,"category":cats})
        else:
            data=Contact_Us(name=nm,contact_number=con,subject=sub,message=msz)
            data.save()
            res = "Dear {} Thanks for your feedback".format(nm)
            return render(request,"contact.html",{"status":res,"category":cats,"message":recent})
    return render(request,"contact.html",{"message":recent,"category":cats})

def register(request):
    if(request.method == "POST"):
        fname = request.POST["first"]
        last = request.POST["last"]
        un = request.POST["uname"]
        pwd = request.POST["password"]
        em = request.POST["email"]
        con = request.POST["contact"]
        tp = request.POST ["utype"]

        if(fname.isalpha()!=True):
            return render(request,"register.html",{"status":"Mr/Miss. {} Please Enter Valid First Name".format(fname)})
        elif(last.isalpha()!=True):
            return render(request,"register.html",{"status":"Mr/Miss. {} Please Enter Valid Second Name".format(fname)})
        elif(len(con)>10):
            return render(request,"register.html",{"status":"Mr/Miss. {} Please Enter 10 Digit Contact Number".format(fname)})
        elif(len(con)<10):
            return render(request,"register.html",{"status":"Mr/Miss. {} Please Enter 10 Digit Contact Number".format(fname)})
        elif(con.isnumeric()==False):
            return render(request,"register.html",{"status":"Mr/Miss. {} Please Enter Valid Contact Number".format(fname)})
        else:
            usr = User.objects.create_user(un,em,pwd)
            usr.first_name = fname
            usr.last_name = last
            if tp=="sell":
                usr.is_staff=True
            usr.save()
            reg = register_table(user=usr,contact_number=con)
            reg.save()
            return render(request,"register.html",{"status":"Mr/Miss. {} Your Account Created Successfully".format(fname)})

    return render(request,"register.html")


def check_user(request):
    if request.method=="GET":
        un= request.GET["usern"]
        check= User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")


def user_login(request):
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]

        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            # if user.is_staff:
            else:
                return HttpResponseRedirect("/cust_dashboard")
                # return HttpResponseRedirect("/seller_dashboard")
            # if user.is_active:
            #     return HttpResponseRedirect("/cust_dashboard")

        else:
            return render(request,"home.html",{"status":"Invalid Username or Password"})
        
    return HttpResponse("called")

@login_required
def cust_dashboard(request):
    context = {}
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data
    
    return render(request,"cust_dashboard.html",context)

@login_required
def seller_dashboard(request):
    return render(request,"seller_dashboard.html")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")
    # res = HttpResponseRedirect("/")
    # res.delete_cookie("user_id")
    # res.delete_cookie("date_login")
    # return res



def edit_profile(request):
    context={}
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data

    
    if request.method == "POST":
        fn = request.POST["fname"]
        ln = request.POST["lname"]
        em = request.POST["email"]
        con = request.POST["contact"]
        age = request.POST["age"]
        ct = request.POST["city"]
        gen = request.POST["gender"]
        addr = request.POST["address"]

        usr = User.objects.get(id=request.user.id)
        usr.first_name=fn
        usr.last_name=ln
        usr.email=em
        usr.save()

        data.contact_number=con
        data.age=age
        data.city=ct
        data.gender=gen
        data.address=addr
        data.save()

        if "image" in request.FILES:
            img = request.FILES["image"]
            data.profile_pic=img
            data.save()
        context["status"]="changes save successfully"
    return render(request,"edit_profile.html",context)


def change_password(request):
    context={}
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data

    if request.method =="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]

        user = User.objects.get(id=request.user.id)
        un = user.username
        
        check = user.check_password(current)

        if check == True:
            user.set_password(new_pas)
            user.save()

            context["msz"]="Password Change Successfully"
            context["col"]="alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        
        else:
            context["msz"]="Incorrect Current password"
            context["col"]="alert-danger"
        
        # return render(request,"change_password.html",context)


    return render(request,"change_password.html",context)


def add_product_view(request):
    context={}
    # form = add_product_form()
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data
    form = add_product_form()
    if request.method =="POST":
        form = add_product_form(request.POST,request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            login_user = User.objects.get(username=request.user.username)
            data.seller_name=login_user
            data.save()
            context["status"]="{} Added Successfully".format(data.product_name)
    context["form"]=form
    return render(request,"addproduct.html",context)


def my_products(request):
    context={}
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    # form = add_product_form()
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data

    all_p = add_product.objects.filter(seller_name__id=request.user.id).order_by("-id")
    context["products"]=all_p
    return render(request,"myproducts.html",context)


def single_product(request):
    context={}
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    id = request.GET["pid"]
    obj = add_product.objects.get(id=id)
    context["product"]=obj
    return render(request,"single_product.html",context)

def update_product(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data

    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    
    pid = request.GET["pid"]
    # product = add_product.objects.get(id=pid)
    product = get_object_or_404(add_product,id=pid)
    context["product"]=product

    if request.method == "POST":
        pn = request.POST["pname"]
        ct_id = request.POST["pcat"]
        pr = request.POST["pp"]
        sp = request.POST["sp"]
        des = request.POST["des"]

        cat_obj = Category.objects.get(id=ct_id)

        product.product_name=pn
        product.product_category=cat_obj
        product.product_price=pr
        product.sale_price=sp
        product.details=des
        if "pimg" in request.FILES:
            img = request.FILES["pimg"]
            product.product_image=img
        product.save()
        context["status"]="Changes Saved Successfully"
        context["id"]=pid
    return render(request,"update_product.html",context)

def delete_product(request):
    context={}
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data

    if "pid" in request.GET:
        pid=request.GET["pid"]
        prd = get_object_or_404(add_product,id=pid)
        context["product"]=prd

        if "action" in request.GET:
            prd.delete()
            context["status"]=str(prd.product_name)+ "Deleted Successfully !!!!"
    return render(request,"delete_product.html",context)

def all_products(request):
    context={}
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    all_products = add_product.objects.all().order_by("product_name")
    context["products"]=all_products

    if "qry" in request.GET:
        q = request.GET["qry"]
        # p = request.GET["price"]
        prd=add_product.objects.filter(Q(product_name__icontains=q)|Q(product_category__cat_name__contains=q))
        context["products"]=prd
        context["abcd"]="search"

    if "cat" in request.GET:
        cid=request.GET["cat"]
        prd = add_product.objects.filter(product_category__id=cid)
        context["products"]=prd
        context["abcd"]="search"
    return render(request,"allproducts.html",context)

def sendemail(request):
    context={}
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    # form = add_product_form()
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data

    if request.method=="POST":
        rec = request.POST["to"].split(",")
        sub = request.POST["sub"]
        msz = request.POST["msz"]
        try:
            em =EmailMessage(sub,msz,to=rec)
            em.send()
            context["message"]="Email Sent"
            context["cls"]="alert-success"
        except:
            context["message"]="Could not send, Please check internet connection / Email address"
            context["cls"]="alert-danger"

    return render(request,"sendemail.html",context)

def forgot_pass(request):
    context={}
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]

        user = get_object_or_404(User,username=un)
        user.set_password(pwd)
        user.save()

        login(request,user)
        if user.is_superuser:
            return HttpResponseRedirect("/admin")
        else:
            return HttpResponseRedirect("/cust_dashboard")
        # context["status"]="Password Changed Successfully!!!"
    return render(request,"forgot_pass.html",context)

import random
def reset_password(request):
    un = request.GET["username"]
    try:
        user = get_object_or_404(User,username=un)
        otp = random.randint(1000,9999)
        msz = "Dear {} \n{} Here is your one time password (OTP) \nDo not share it with other \nThanks & Regard \nMywebsite".format(user.username,otp)
        try:
            email = EmailMessage("Account Verification",msz,to=[user.email])
            email.send()
            return JsonResponse({"status":"sent","email":user.email,"rotp":otp})
        except:
            return JsonResponse({"status":"error","email":user.email})
    except:
        return JsonResponse({"status":"failed"})

def add_to_cart(request):
    context={}
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    items = cart.objects.filter(user__id=request.user.id,status=False)
    context["items"]=items
    if request.user.is_authenticated:
        if request.method=="POST":
            pid = request.POST["pid"]
            qty = request.POST["quantity"]
            is_exit = cart.objects.filter(product__id=pid,user__id=request.user.id,status=False)
            if len(is_exit)>0:
                context["msz"]="Item Already exits in your cart"
                context["cls"]="alert alert-warning"
            else:
                product = get_object_or_404(add_product,id=pid)
                usr = get_object_or_404(User,id=request.user.id)
                c= cart(user=usr,product=product,quantity =qty)
                c.save()
                context["msz"]="{} Added in your cart".format(product.product_name)
                context["cls"]="alert alert-success"
    else:
        context["status"]="Please Login to View Your Cart"
    return render(request,"cart.html",context)

def get_cart_data(request):
    items = cart.objects.filter(user__id=request.user.id,status=False)
    sale,total,quantity=0,0,0
    for i in items:
        sale+=float(i.product.sale_price)*i.quantity
        total+=float(i.product.product_price)*i.quantity
        quantity+=int(i.quantity)
        print(total)
    res = {
        "total":total,"offer":sale,"quan":quantity,
    }
    
    return JsonResponse(res)

def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(cart,id=cid)
        cart_obj.quantity=qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)
    if "delete_cart" in request.GET:
        id=request.GET["delete_cart"]
        cart_obj = get_object_or_404(cart,id=id)
        cart_obj.delete()
        return HttpResponse(1)

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

def process_payment(request):
    items = cart.objects.filter(user_id__id=request.user.id,status=False)
    amt=0
    products=""
    inv="INV1001-"
    cart_ids =""
    p_ids = ""
    for j in items:
        products += str(j.product.product_name)+","
        p_ids += str(j.product.id)+","
        amt +=j.product.sale_price*j.quantity
        inv +=str(j.id)
        cart_ids +=str(j.id)+","

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': (amt)/73,
        'item_name': products,
        'invoice': inv,
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              reverse('payment_cancelled')),
        
    }
    usr = User.objects.get(username=request.user.username)
    fetch_add = get_object_or_404(register_table,user__id=request.user.id)
    
    ord = Order(cust_id=usr,cart_ids=cart_ids,product_ids=p_ids,address=fetch_add.address,product_name=products,product_amount=amt)
    ord.save()
    ord.invoice_id=str(ord.id)+inv
    ord.save()
    request.session["order_id"]=ord.id

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'form': form})

def payment_done(request):
    if "order_id" in request.session:
        order_id = request.session["order_id"]
        ord_obj = get_object_or_404(Order,id=order_id)
        ord_obj.status=True
        ord_obj.save()

        for i in ord_obj.cart_ids.split(",")[:-1]:
            cart_object = cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()

        name = User.objects.get(username=request.user.username)
        user_email = name.email
        mail=user_email.split(",")
        sub = "Order Confirmation from Zyka"
        msz = "Your Order will be delivered from 1 to 2 hours. Thanks !!!"
        em =EmailMessage(sub,msz,to=mail)
        em.send()

    return render(request,"payment_success.html")

def payment_cancelled(request):
    return render(request,"payment_failed.html")

def order_history(request):
    context={}
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data
    all_orders=[]
    orders = Order.objects.filter(cust_id__id=request.user.id).order_by("-id")
    for order in orders:
        products=[]
        for id in order.product_ids.split(",")[:-1]:
            pro = get_object_or_404(add_product,id=id)
            products.append(pro)
        ord={
            "order_id":order.id,
            "products":products,
            "invoice":order.invoice_id,
            "status":order.status,
            "date":order.processed_on,

        }
        all_orders.append(ord)
    context["order_history"]=all_orders
    return render(request,"order_history.html",context)

def my_cust(request):
    context={}
    cats = Category.objects.all().order_by("cat_name")
    context["category"]=cats
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data

    products = cart.objects.filter(product__seller_name__id=request.user.id,status=True)
    cust = []
    ids = []
    context["times"]=len(products)
    for i in products:
        us = {
            "username":i.user.username,
            "first_name":i.user.first_name,
            "last_name":i.user.last_name,
            "email":i.user.email,
            "join":i.user.date_joined,
        }
        check = register_table.objects.filter(user__id=i.user.id)
        if len(check)>0:
            prf = get_object_or_404(register_table,user__id=i.user.id)
            us["profile_pic"]=prf.profile_pic
            us["contact"]=prf.contact_number
        ids.append(i.user.id)
        count = ids.count(i.user.id)
        if count<2:
            cust.append(us)
    context["customers"]=cust
    return render(request,"my_cust.html",context)
    



    
