from django.shortcuts import render,redirect
from .models import * 
from django.contrib import messages
from django.http import *
from django.http import JsonResponse
from app.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    pics=Image.objects.all()
    category = shop.objects.filter(status=0)
    subcat=subcategories.objects.filter(status=0)
    trending_products = products.objects.filter(trending=True, status=0)
    return render(request,'home.html', {'pics': pics, 'shops': category,'Subcateg': subcat,'trending_products': trending_products})

def about(request):
    pic=AImage.objects.all()
    return render(request,'about.html', {'pic': pic})

def logout_pg(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logged out successfully')
        return redirect('/')
    
def log_pg(request):
    pic=AImage.objects.all()
    if request.user.is_authenticated:
        # return redirect('home')
        messages.info(request, 'You are already logged in.')
        return redirect('home')
    else:
        if request.method == "POST":
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in successfully')
                return redirect('home')
            else:
                messages.error(request,'Invalid Username and Password')
                return redirect('login')
        return render(request, "login.html", {'pic': pic})

def signup(request):
    form=CustomUserForm()
    if request.method=="POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration success you can login!')
            return redirect('login')
    return render(request, "signup.html",{'form': form})
    

def category(request):
    pics=Image.objects.all()
    category = shop.objects.filter(status=0)
    subcat=subcategories.objects.filter(status=0)
    return render(request,'shop.html',{'pics': pics, 'shops': category,'Subcateg': subcat})

def product(request,name):
    if(subcategories.objects.filter(name=name,status=0)):
        Products=products.objects.filter(category__name=name)
        return render(request,'product.html',{'product':Products,'category':name})
    else:
        messages.warning(request,'No Such Category Found')
        return redirect('shop')
    
def prod_view(request,cat_name,prod_name):   
    if(subcategories.objects.filter(name=cat_name,status=0)):
        if(products.objects.filter(name=prod_name,status=0)):
            Products=products.objects.filter(name=prod_name,status=0).first()
            return render(request,'prodview.html',{'products':Products})
        else:
            messages.error(request,"Product doesn't exist")
            return redirect('product')
    else:
        messages.error(request,"Category doesn't exist")
        return redirect('product')

def productoff(request, slug):
    subcategory = subcategories.objects.filter(slug=slug, status=0).first()
    if subcategory:
        Products = products.objects.filter(category=subcategory)
        return render(request, 'product.html', {'product': Products, 'category': slug})
    else:
        messages.warning(request, 'No Such Category Found')
        return redirect('shop')

def remove_wish(request,wid):
    wishitem=wishlists.objects.get(id=wid)
    wishitem.delete()
    return redirect('wishlist')

def whishlist(request):
    if request.user.is_authenticated:
        Wishlist=wishlists.objects.filter(user=request.user)
        return render(request, "wishlist.html",{'wishlt':Wishlist})
    else:
        messages.info(request, 'Please login to access your wishlist.')
        return redirect('login')


def addtowishlist(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
                data = json.loads(request.body.decode('utf-8'))
                prod_id = data.get('pid')
                product_status=products.objects.get(id=prod_id)
                if product_status:
                    if wishlists.objects.filter(user= request.user, product_id=prod_id):
                        return JsonResponse({'status': 'Product already in Wishlist'}, status=200)
                    else:
                        wishlists.objects.create(user=request.user, product_id=prod_id)
                        return JsonResponse({'status': 'Product added to wishlist'}, status=200)
                
        else:
            return JsonResponse({'status': 'You must login to add your Wishlist'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)

import json

def add_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
                data = json.loads(request.body.decode('utf-8'))
                prod_id = data.get('pid')
                if not prod_id:
                    return JsonResponse({'status': 'Invalid product ID'}, status=400)
                product_status=products.objects.get(id=prod_id)
                if product_status:
                    if cart.objects.filter(user= request.user, product_id=prod_id):
                        return JsonResponse({'status': 'Product already in cart'}, status=200)
                    else:
                        if product_status.quantity>0:
                            cart.objects.create(user=request.user, product=product_status, prod_qty=1)
                            return JsonResponse({'status': 'Product added to cart successfully'}, status=200)
                        else:
                            return JsonResponse({'status': 'Product stock not available'}, status=200)
        else:
            return JsonResponse({'status': 'You must be logged in to add to cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)
    

def view_cart(request):
    if request.user.is_authenticated:
        Cart=cart.objects.filter(user=request.user)
        return render(request, "cart.html",{'cart':Cart})
    else:
        return redirect('login')

def update_cart(request):
    print("update_cart view function called")
    if request.method == "POST":
        print("Request method is POST")
        cart_id = request.POST.get('product_id')
        produ_qty = request.POST.get('quantity')
        token = request.POST.get('csrfmiddlewaretoken')

        print("Cart ID:", cart_id)
        print("Product Quantity:", produ_qty)
        print("CSRF Token:", token)

        print("Request user:", request.user)
        cart_contents = cart.objects.filter(user=request.user)
        print("Cart contents:", cart_contents)

        # Check if the cart item is in the cart for the user
        cart_item = cart.objects.filter(user=request.user, id=(cart_id))
        if cart_item.exists():
            # Update the quantity of the cart item
            cart_item.update(prod_qty=produ_qty)
            print("Cart updated successfully")
            return JsonResponse({'status': 'Product updated'}, status=200)
            
        else:
            print("Cart item not found in cart")
            return JsonResponse({'status': 'Not Found'})
    else:
        print("Request method is not POST")
        return redirect('/')
    
def close(request):
    if request.method == "POST":
        cart_id = request.POST.get('product_id')
        if (cart.objects.filter(user=request.user, id=cart_id)):
            cartitem=cart.objects.filter(user=request.user, id=cart_id)
            cartitem.delete()
            return JsonResponse({'status': 'Product deleted'})
        else:
            print("Cart item not found in cart")
            return JsonResponse({'status': 'Product deleted'})
    else:
        print("Request method is not POST")
        return redirect('/')


    