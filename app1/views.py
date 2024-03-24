from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Cart,Wishlistt
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.paginator import Paginator
from .forms import ContactForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse




# Create your views here.

def home(request):
    myproduct = Product.objects.all().order_by('id')
    paginator = Paginator(myproduct, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    user_cart = Cart.objects.filter(username=request.user.username).first()
    cart_items = set(user_cart.c_details.keys()) if user_cart and user_cart.c_details else set()
    print(cart_items)
    return render(request,'app1/home.html',{'page_obj':page_obj, 'cart_items': cart_items})

def  allproducts(request):
    if request.method == 'GET':
        myproducts = Product.objects.all()
        return render(request,"app1/filter.html",{'x':myproducts})
    else:
        z = request.POST.get('myfood')
        # print (z)
        m = float(request.POST.get('price_range'))
        # print(m)
        if(z=='Select'):
            k = Product.objects.filter( price__lte=m )
        # k = Product.objects.filter(category=z)
        else:
            k = Product.objects.filter(category=z, price__lte=m )
        # print(k)
        # return HttpResponse('Hello')
        return render(request, "app1/filter.html", {'x': k,'j':m})
    

def details(request,pid):
    if request.user.is_authenticated:
        myproduct = get_object_or_404(Product, pk=pid)
        return render(request,'app1/details.html',{'z':myproduct})
    else:
        if request.method == 'GET':
            return render(request,'app1/login.html',{'form':AuthenticationForm(),'o':'Login Required!'})
        else:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request,'app1/login.html',{'form':AuthenticationForm(),'k':'Invalid Username or Password!'})

    

def aboutus(request):
    return render(request, 'app1/aboutus.html')

def contactus(request):
    form = ContactForm
    return render(request, 'app1/contactus.html',{'form': form})


def add_record(request):
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

def dashboard(request):
    return render(request,"app1/dashboard.html")

def search(request):
    # query = request.GET['query']
    if request.method == 'POST':
        query = request.POST.get('search1')
        # query = request.GET('search1')
        print(query)
        if len(query) > 0 :
            if Product.objects.filter(Title__icontains=query) | Product.objects.filter( category__icontains=query):
                if(Product.objects.filter(Title__icontains=query)):
                    k = Product.objects.filter(Title__icontains=query)
                    return render(request,"app1/search.html",{'x':k})
                if(Product.objects.filter(category__icontains=query)):
                    k = Product.objects.filter(category__icontains=query)
                    return render(request,"app1/search.html",{'x':k})
            else:
                return render(request,'app1/search.html',{'o':'Item Not Available'})
        else:
            return redirect("show")

def show(request):
    myproducts = Product.objects.all()
    return render(request,"test1/search.html",{'x':myproducts})

def signupuser(request):
    if request.method == 'GET':
        return render(request,'app1/signup.html',{'form':UserCreationForm()})
    else:
        if(request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('login')
            except IntegrityError:
                return render(request,'app1/signup.html',{'form':UserCreationForm(),'y':'Username already taken'})
            
        else:
            return render(request,'app1/signup.html',{'form':UserCreationForm(),'z':'Passwords Unmatched'})

def loginuser(request):
    if request.method == 'GET':
        return render(request,'app1/login.html',{'form':AuthenticationForm()})
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request,'app1/login.html',{'form':AuthenticationForm(),'k':'Invalid Username or Password!'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    if request.method == 'GET':
        logout(request)
        return redirect('home')
    
def settings(request):
    return render(request,"app1/settings.html")


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user.username
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided

        # Check if the user already has items in the cart
        cart, created = Cart.objects.get_or_create(username=user)

        # Ensure that c_details is initialized as a dictionary
        if not isinstance(cart.c_details, dict):
            cart.c_details = {}

        # If the item is not already in the cart, add it
        if str(item_id) not in cart.c_details:
            cart.c_details[str(item_id)] = quantity
        else:
            cart.c_details[str(item_id)] += quantity
        cart.save()

    return redirect('show_cart')


from django.shortcuts import render
from django.http import HttpResponse
from .models import Cart, Product
from django.contrib.auth.decorators import login_required

@login_required
def show_cart(request):
    # Get the username of the current user
    user = request.user.username
    # Get the cart for the current user
    cart = Cart.objects.filter(username=user).first()
    # Initialize total bill
    total_bill = 0
    # If cart exists and has cart details
    if cart and cart.c_details:
        # Get cart items
        cart_items = [int(item_id) for item_id in cart.c_details.keys()]
        # Ensure that cart_items is not an empty list
        if cart_items:
            # Filter products based on the item IDs
            cart_products = Product.objects.filter(Product_id__in=cart_items)
            # Fetch all products
            products = Product.objects.all()
            # Get the items in the cart
            items = cart.c_details
            # Iterate over items in the cart
            for item_id, quantity in items.items():
                # Get the product corresponding to the item in the cart
                product = products.filter(Product_id=item_id).first()
                # If product exists
                if product:
                    subtotal = product.price * quantity
                    # Add the previous product bill to the total bill
                    total_bill += subtotal
               
    # If cart is empty or no cart details found
    if not cart or not cart.c_details:
        return render(request, 'app1/dashboard.html', {'k': 'Add items to Cart'})
  # Render the template with the cart, products, and total bill
    return render(request, "app1/dashboard.html", {'p': cart_products, 'cart':'YOUR CART', 'bill': total_bill,'c':cart.c_details})   



@login_required
def remove_item_cart(request):
    if request.method == 'POST':
        username = request.user.username
        item_id_to_remove = request.POST.get('rc_btn')

        # Retrieve the cart instance for the current user
        cart = Cart.objects.get(username=username)

        # Retrieve the cart details dictionary
        cart_details = cart.c_details

        # Remove the specified item ID from the cart details
        if str(item_id_to_remove) in cart_details:
            del cart_details[str(item_id_to_remove)]

            # Update the cart details and save the instance
            cart.c_details = cart_details
            cart.save()

        # Redirect to the show_cart page
        return redirect('show_cart')

    return render(request, 'app1/dashboard.html')



@login_required
def update_cart(request):
    if request.method == 'POST':
        user = request.user.username
        item_id = request.POST.get('item_id')
        cart = Cart.objects.get(username=user)

        cart_details = cart.c_details
        
        new_quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided

        # Update the quantity of the specified item in the cart
        cart_details[str(item_id)] = new_quantity
        
        # Save the updated cart details
        cart.c_details = cart_details
        cart.save()
        
            
    return redirect('show_cart')

def calculate_bill(request):
    # Get the username of the current user
    user = request.user.username
    cart = Cart.objects.get(username=user)
    products = Product.objects.all()
    items = cart.c_details
    total_bill = 0
    for item_id, quantity in items.items():
        product = products.filter(Product_id=item_id).first()
        if product:
            subtotal = product.price * quantity
            total_bill += subtotal
    total_bill = round(total_bill, 2)
    print("Total Bill:", total_bill)
    return render(request, 'app1/dashboard.html',{'bill':total_bill})



@login_required
def add_wishlists(request):
    if request.method == 'POST':
        user_name = request.user.username
        item_id = request.POST.get('w_btn')  # Assuming 'w_btn' contains the product id

        # Check if the user already has a wishlist
        wishlist, created = Wishlistt.objects.get_or_create(user=user_name)

        # If the item is not already in the wishlist, add it
        product = Product.objects.get(Product_id=item_id)
        if product not in wishlist.wl_details.all():
            wishlist.wl_details.add(product)

    return redirect('show_wishlists')

@login_required
def show_wishlists(request):
    username = request.user
    wishlist = Wishlistt.objects.filter(user=username).first()

    if wishlist:
        wl_items = wishlist.wl_details.values_list('Product_id', flat=True)

        # Ensure that wl_items is not an empty list
        if wl_items:
            # Filter products based on the item IDs
            wl_products = Product.objects.filter(Product_id__in=wl_items)

            return render(request, "app1/dashboard.html", {'o': wl_products, 'wishlist':'YOUR WISHLIST'})
    
    # If cart is empty or no cart details found
    return render(request, 'app1/dashboard.html', {'l': 'Add items to Wishlist'})



def remove_item_wishlist(request):
    if request.method == 'POST':
        username = request.user
        item_id_to_remove = request.POST.get('rw_btn')

        # Retrieve the wishlist instance for the current user
        wishlist = Wishlistt.objects.get(user=username)

        # Retrieve the product instance to remove
        product_to_remove = Product.objects.get(Product_id=item_id_to_remove)

        # Remove the specified product from the wishlist
        wishlist.wl_details.remove(product_to_remove)

        # Redirect to the wishlist page or display a success message
        return redirect('show_wishlists')

    return render(request, 'app1/dashboard.html')  # You might want to handle GET requests differently





    