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



# Create your views here.

def home(request):
    myproduct = Product.objects.all().order_by('id')
    paginator = Paginator(myproduct, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'app1/home.html',{'page_obj':page_obj})

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
        item_id = request.POST.get('c_btn')

        # Check if the user already has items in the cart
        cart, created = Cart.objects.get_or_create(username=user)

        # If the item is not already in the cart, add it
        if cart.c_details:
            if item_id not in cart.c_details.split(', '):
                cart.c_details += ', ' + item_id
        else:
            cart.c_details = item_id

        cart.save()

    return redirect('show_cart')



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

@login_required
def show_cart(request):
    user = request.user.username
    cart = Cart.objects.filter(username=user).first()

    if cart and cart.c_details:
        cart_items = [int(item_id) for item_id in cart.c_details.split(', ') if item_id]

        # Ensure that cart_items is not an empty list
        if cart_items:
            # Filter products based on the item IDs
            cart_products = Product.objects.filter(Product_id__in=cart_items)

            return render(request, "app1/dashboard.html", {'p': cart_products, 'cart':'YOUR CART'})
    
    # If cart is empty or no cart details found
    return render(request, 'app1/dashboard.html', {'k': 'Add items to Cart'})

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


def remove_item_cart(request):
    if request.method == 'POST':
        username = request.user.username
        item_id_to_remove = request.POST.get('rc_btn')

        # Retrieve the cart instance for the current user
        z = Cart.objects.get(username=username)

        # Split the cart details string into a list of items
        c_items = z.c_details.split(', ')

        # Remove the specified item ID from the list
        c_items.remove(str(item_id_to_remove))

        # Join the modified list back into a string
        updated_cart_details = ', '.join(c_items)

        # Update the cart details and save the instance
        z.c_details = updated_cart_details
        z.save()

        # Redirect to the show_cart page
        return redirect('show_cart')

    return render(request, 'app1/dashboard.html')


    