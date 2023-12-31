from main.models import Product
from django.shortcuts import render
from django.http import HttpResponseRedirect
from main.forms import ProductForm
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
#import pytz
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

#utc_now = datetime.datetime.now(pytz.utc)
#gmt7 = utc_now.astimezone(pytz.timezone('Etc/GMT-7'))
@login_required(login_url='/login')
def show_main(request):
    products = Product.objects.filter(user=request.user)

    context = {
        'name':  request.user.username, # Nama kamu
        'class': 'PBP A', # Kelas PBP kamu
        'products': products,
        'last_login': request.COOKIES.get('last_login','Not Available'),
    }

    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return HttpResponseRedirect(reverse('main:show_main'))
    
    context = {'form': form}    
    return render(request, "create_product.html", context)
 
@csrf_exempt
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
# Create your views here.

def update_amount(request, item_name, action):

    try:
        products = Product.objects.filter(name=item_name)
    except products.DoesNotExist:
        # Handle jika item tidak ditemukan
        return redirect('main:show_main')

    for item in products:
        if action == 'increase':
            item.amount += 1
        elif action == 'decrease':
            if item.amount == 1:  # Jika item.amount sama dengan 1
                item.delete()  # Menghapus item dari database
                return redirect('main:show_main')  # Mengarahkan ulang ke halaman yang menampilkan tabel
            else:
                item.amount -= 1
            

    item.save()

    return redirect('main:show_main')

def edit_product(request, id):
    # Get product berdasarkan ID
    product = Product.objects.get(pk = id)

    # Set product sebagai instance dari form
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)


def delete_item(request, item_name):
    try:
        item = Product.objects.filter(name=item_name)
    except item.DoesNotExist:
        # Handle jika item tidak ditemukan
        return redirect('main:show_main')

    item.delete()

    return redirect('main:show_main')

def get_product_json(request):
    product_item = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', product_item))

@csrf_exempt
def add_product_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        date_added = request.POST.get("date_added")
        amount = request.POST.get("amount") 
        user = request.user

        new_product = Product(name=name, price=price, description=description, user=user, date_added=date_added, amount=amount)
        new_product.save()

        return HttpResponse("CREATED", status=201)

    return HttpResponseNotFound()


@csrf_exempt
def delete_product_ajax(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)
        product.delete()
        
        
@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_product = Product.objects.create(
            user = request.user,
            name = data["name"],
            price = int(data["price"]),
            description = data["description"]
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
