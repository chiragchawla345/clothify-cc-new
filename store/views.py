from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
import os
# Create your views here.


def home(request):
    user_object = User.objects.filter(username=request.user).first()
    # if user_object is None:
    #     return redirect('/')
    product_object = Products.objects.order_by('-total_quantity_sold')[:10]
    product_dict = {}
    count = 1
    for product in product_object:
        product_dict[count] = {}
        product_dict[count]['id'] = 'productdetail\\'+str(product.id)
        product_dict[count]['title'] = product.title
        product_dict[count]['brand'] = product.brand
        product_dict[count]['market_price'] = product.market_price
        product_dict[count]['discounted_price'] = product.discounted_price
        product_dict[count]['discount'] = round((
            product.market_price - product.discounted_price)/product.market_price*100)
        product_dict[count]['image'] = product.image
        category = product.category
        sub_category = product.sub_category
        sizes_available = []
        if category == 'Men\'s' or category == 'Women\'s':
            if sub_category == 'Top-wear':
                if product.size_1 == True:
                    sizes_available.append('S')
                if product.size_2 == True:
                    sizes_available.append('M')
                if product.size_3 == True:
                    sizes_available.append('L')
                if product.size_4 == True:
                    sizes_available.append('XL')
            elif sub_category == 'Bottom-wear':
                if product.size_1 == True:
                    sizes_available.append('28')
                if product.size_2 == True:
                    sizes_available.append('30')
                if product.size_3 == True:
                    sizes_available.append('32')
                if product.size_4 == True:
                    sizes_available.append('34')
                if product.size_5 == True:
                    sizes_available.append('36')
            else:
                if product.size_1 == True:
                    sizes_available.append('UK-6')
                if product.size_2 == True:
                    sizes_available.append('UK-7')
                if product.size_3 == True:
                    sizes_available.append('UK-8')
                if product.size_4 == True:
                    sizes_available.append('UK-9')
                if product.size_5 == True:
                    sizes_available.append('UK-10')
                if product.size_6 == True:
                    sizes_available.append('UK-11')
        else:
            if sub_category == 'Top-wear' or sub_category == 'Bottom-wear':
                if product.size_1 == True:
                    sizes_available.append('1-2Y')
                if product.size_2 == True:
                    sizes_available.append('2-3Y')
                if product.size_3 == True:
                    sizes_available.append('3-4Y')
                if product.size_4 == True:
                    sizes_available.append('4-5Y')
                if product.size_5 == True:
                    sizes_available.append('5-6Y')
                if product.size_6 == True:
                    sizes_available.append('6-7Y')
                if product.size_7 == True:
                    sizes_available.append('7-8Y')
                if product.size_8 == True:
                    sizes_available.append('8-9Y')
                if product.size_9 == True:
                    sizes_available.append('9-10Y')
                if product.size_10 == True:
                    sizes_available.append('10-11Y')
                if product.size_11 == True:
                    sizes_available.append('11-12Y')
            else:
                if product.size_1 == True:
                    sizes_available.append('1-1.5Y')
                if product.size_2 == True:
                    sizes_available.append('1.5-2Y')
                if product.size_3 == True:
                    sizes_available.append('2-2.5Y')
                if product.size_4 == True:
                    sizes_available.append('2.5-3Y')
                if product.size_5 == True:
                    sizes_available.append('3-3.5Y')
                if product.size_6 == True:
                    sizes_available.append('3.5-4Y')
                if product.size_7 == True:
                    sizes_available.append('4-4.5Y')
                if product.size_8 == True:
                    sizes_available.append('4.5-5Y')
                if product.size_9 == True:
                    sizes_available.append('5-6Y')
                if product.size_10 == True:
                    sizes_available.append('6-7Y')
                if product.size_11 == True:
                    sizes_available.append('7-8Y')
                if product.size_12 == True:
                    sizes_available.append('8-9Y')
                if product.size_13 == True:
                    sizes_available.append('9-10Y')
                if product.size_14 == True:
                    sizes_available.append('10-11Y')
                if product.size_15 == True:
                    sizes_available.append('11-12Y')
        product_dict[count]['sizes_available'] = ', '.join(sizes_available)
        count += 1
    context = {'products': product_dict}
    return render(request, 'home.html', context)


def product_list(request):
    return render(request, 'product_list.html')


def updatecart(request):
    if request.method == 'POST':
        if request.POST.get('type') == 'decrement':
            user_id = User.objects.filter(username=request.user).first()
            product_id = request.POST.get('product')
            cart = Cart_Items.objects.filter(
                user_id=user_id, product_id=product_id).first()
            quantity = cart.quantity

            if(quantity > 1):
                cart.quantity = quantity - 1  # change field
                cart.save()
                total_price = 0
                cart_items = Cart_Items.objects.filter(user_id=user_id).all()
                for cart_item in cart_items:
                    print(cart_item)
                    product = cart_item.product_id
                    quantity = cart_item.quantity
                    total_price += (product.discounted_price * quantity)
                return HttpResponse('success'+str(total_price))
            else:
                return HttpResponse('failed')
        else:
            user_id = User.objects.filter(username=request.user).first()
            product_id = request.POST.get('product')
            cart = Cart_Items.objects.filter(
                user_id=user_id, product_id=product_id).first()
            quantity = cart.quantity
            if(quantity < 10):
                cart.quantity = quantity + 1  # change field
                cart.save()
                total_price = 0
                cart_items = Cart_Items.objects.filter(user_id=user_id).all()
                for cart_item in cart_items:
                    print(cart_item)
                    product = cart_item.product_id
                    quantity = cart_item.quantity
                    total_price += (product.discounted_price * quantity)
                return HttpResponse('success'+str(total_price))
            else:
                return HttpResponse('failed')
    else:
        return redirect('addtocart')


def productdetail(request, product_id):
    if request.method == 'POST':
        try:
            size = request.POST.getlist('inlineRadioOptions')[0]
        except:
            messages.info(request, 'Please select Size')
            return redirect('/productdetail/'+str(product_id))
        if 'add_to_cart' in request.POST:
            product = Products.objects.filter(id=product_id).first()
            user = User.objects.filter(username=request.user).first()
            cart = Cart_Items(user_id=user,
                              product_id=product, size=size, quantity=1)
            try:
                cart.save()
                messages.warning(request, "Item added successfully")
                return redirect('/addtocart')
            except IntegrityError as e:
                messages.error(
                    request, "Item already added, kindly remove item from cart")

        else:
            return select_an_address(request)

    product_object = Products.objects.filter(id=product_id).first()
    if product_object is None:
        print('Product Doesn\'t Exist')
        messages.info(request, 'Product Doesn\'t Exist')
        return redirect('home')
    else:
        product_dict = {}
        product_dict['id'] = product_id
        product_dict['brand'] = product_object.brand
        product_dict['title'] = product_object.title
        category = product_object.category
        sub_category = product_object.sub_category
        sizes_available = []
        sizes_quantity = []
        if category == 'Men\'s' or category == 'Women\'s':
            if sub_category == 'Top-wear':
                if product_object.size_1 == True:
                    sizes_available.append('S')
                    sizes_quantity.append(product_object.size_1_quantity)
                if product_object.size_2 == True:
                    sizes_available.append('M')
                    sizes_quantity.append(product_object.size_2_quantity)
                if product_object.size_3 == True:
                    sizes_available.append('L')
                    sizes_quantity.append(product_object.size_3_quantity)
                if product_object.size_4 == True:
                    sizes_available.append('XL')
                    sizes_quantity.append(product_object.size_4_quantity)
            elif sub_category == 'Bottom-wear':
                if product_object.size_1 == True:
                    sizes_available.append('28')
                    sizes_quantity.append(product_object.size_1_quantity)
                if product_object.size_2 == True:
                    sizes_available.append('30')
                    sizes_quantity.append(product_object.size_2_quantity)
                if product_object.size_3 == True:
                    sizes_available.append('32')
                    sizes_quantity.append(product_object.size_3_quantity)
                if product_object.size_4 == True:
                    sizes_available.append('34')
                    sizes_quantity.append(product_object.size_4_quantity)
                if product_object.size_5 == True:
                    sizes_available.append('36')
                    sizes_quantity.append(product_object.size_5_quantity)
            else:
                if product_object.size_1 == True:
                    sizes_available.append('UK-6')
                    sizes_quantity.append(product_object.size_1_quantity)
                if product_object.size_2 == True:
                    sizes_available.append('UK-7')
                    sizes_quantity.append(product_object.size_2_quantity)
                if product_object.size_3 == True:
                    sizes_available.append('UK-8')
                    sizes_quantity.append(product_object.size_3_quantity)
                if product_object.size_4 == True:
                    sizes_available.append('UK-9')
                    sizes_quantity.append(product_object.size_4_quantity)
                if product_object.size_5 == True:
                    sizes_available.append('UK-10')
                    sizes_quantity.append(product_object.size_5_quantity)
                if product_object.size_6 == True:
                    sizes_available.append('UK-11')
                    sizes_quantity.append(product_object.size_6_quantity)
        else:
            if sub_category == 'Top-wear' or sub_category == 'Bottom-wear':
                if product_object.size_1 == True:
                    sizes_available.append('1-2Y')
                    sizes_quantity.append(product_object.size_1_quantity)
                if product_object.size_2 == True:
                    sizes_available.append('2-3Y')
                    sizes_quantity.append(product_object.size_2_quantity)
                if product_object.size_3 == True:
                    sizes_available.append('3-4Y')
                    sizes_quantity.append(product_object.size_3_quantity)
                if product_object.size_4 == True:
                    sizes_available.append('4-5Y')
                    sizes_quantity.append(product_object.size_4_quantity)
                if product_object.size_5 == True:
                    sizes_available.append('5-6Y')
                    sizes_quantity.append(product_object.size_5_quantity)
                if product_object.size_6 == True:
                    sizes_available.append('6-7Y')
                    sizes_quantity.append(product_object.size_6_quantity)
                if product_object.size_7 == True:
                    sizes_available.append('7-8Y')
                    sizes_quantity.append(product_object.size_7_quantity)
                if product_object.size_8 == True:
                    sizes_available.append('8-9Y')
                    sizes_quantity.append(product_object.size_8_quantity)
                if product_object.size_9 == True:
                    sizes_available.append('9-10Y')
                    sizes_quantity.append(product_object.size_9_quantity)
                if product_object.size_10 == True:
                    sizes_available.append('10-11Y')
                    sizes_quantity.append(product_object.size_10_quantity)
                if product_object.size_11 == True:
                    sizes_available.append('11-12Y')
                    sizes_quantity.append(product_object.size_11_quantity)
            else:
                if product_object.size_1 == True:
                    sizes_available.append('1-1.5Y')
                    sizes_quantity.append(product_object.size_1_quantity)
                if product_object.size_2 == True:
                    sizes_available.append('1.5-2Y')
                    sizes_quantity.append(product_object.size_2_quantity)
                if product_object.size_3 == True:
                    sizes_available.append('2-2.5Y')
                    sizes_quantity.append(product_object.size_3_quantity)
                if product_object.size_4 == True:
                    sizes_available.append('2.5-3Y')
                    sizes_quantity.append(product_object.size_4_quantity)
                if product_object.size_5 == True:
                    sizes_available.append('3-3.5Y')
                    sizes_quantity.append(product_object.size_5_quantity)
                if product_object.size_6 == True:
                    sizes_available.append('3.5-4Y')
                    sizes_quantity.append(product_object.size_6_quantity)
                if product_object.size_7 == True:
                    sizes_available.append('4-4.5Y')
                    sizes_quantity.append(product_object.size_7_quantity)
                if product_object.size_8 == True:
                    sizes_available.append('4.5-5Y')
                    sizes_quantity.append(product_object.size_8_quantity)
                if product_object.size_9 == True:
                    sizes_available.append('5-6Y')
                    sizes_quantity.append(product_object.size_9_quantity)
                if product_object.size_10 == True:
                    sizes_available.append('6-7Y')
                    sizes_quantity.append(product_object.size_10_quantity)
                if product_object.size_11 == True:
                    sizes_available.append('7-8Y')
                    sizes_quantity.append(product_object.size_11_quantity)
                if product_object.size_12 == True:
                    sizes_available.append('8-9Y')
                    sizes_quantity.append(product_object.size_12_quantity)
                if product_object.size_13 == True:
                    sizes_available.append('9-10Y')
                    sizes_quantity.append(product_object.size_13_quantity)
                if product_object.size_14 == True:
                    sizes_available.append('10-11Y')
                    sizes_quantity.append(product_object.size_14_quantity)
                if product_object.size_15 == True:
                    sizes_available.append('11-12Y')
                    sizes_quantity.append(product_object.size_15_quantity)
        sizes_dict = {}
        for i in range(0, len(sizes_available)):
            size = sizes_available[i]
            quantity = sizes_quantity[i]
            sizes_dict[size] = quantity
        product_dict['sizes_available'] = sizes_dict
        product_dict['market_price'] = product_object.market_price
        product_dict['discounted_price'] = product_object.discounted_price
        product_dict['image'] = "/"+str(product_object.image)
        # print(product_object.image)
        product_dict['description'] = list(
            product_object.description.split('\r\n'))
        context = {'product': product_dict}
    return render(request, 'productdetail.html', context)


def add_to_cart(request):
    if request.user.is_authenticated == False or request.user.is_staff == True:
        return redirect('/')
    if request.method == 'POST':
        if 'remove_item' in request.POST:
            product_id = request.POST.get('product_id')
            cart_item = Cart_Items.objects.filter(
                user_id=request.user, product_id=product_id).first()
            cart_item.delete()
            return redirect('/addtocart')
        elif 'continue' in request.POST:
            return redirect('/placeorder')
    cart_items = Cart_Items.objects.filter(user_id=request.user).all()
    cart_dict = {}
    count = 0
    total_sum = 0
    for item in cart_items:
        cart_dict[count] = {}
        product = item.product_id
        cart_dict[count]['title'] = product.title
        cart_dict[count]['description'] = list(
            product.description.split("\r\n"))
        cart_dict[count]['image'] = product.image
        cart_dict[count]['price'] = product.discounted_price
        cart_dict[count]['quantity'] = item.quantity
        cart_dict[count]['size'] = item.size
        cart_dict[count]['product_id'] = product.id
        cart_dict[count]['total_price'] = item.quantity * \
            product.discounted_price
        total_sum += item.quantity * product.discounted_price
        count += 1
    context = {'cart': cart_dict, 'total_sum': total_sum,
               'total_sum_with_delivery': total_sum+70}
    return render(request, 'addtocart.html', context)


def checkout(request):
    return render(request, 'checkout.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('exampleInputEmail1')
        password = request.POST.get('exampleInputPassword1')
        user = auth.authenticate(
            username=username, password=password)
        if user is not None and user.is_staff == True:
            messages.warning(
                request, 'Seller Credentials - kindly login as Customer Credentials')
            return redirect('login')
        if(user is not None):
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register(request):
    username = request.POST.get('register_username')
    email = request.POST.get('register_email')
    pass1 = request.POST.get('register_password1')
    pass2 = request.POST.get('register_password2')
    if request.method == 'POST':
        print(username)
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already used')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already registered')
            return redirect('register')
        elif pass1 != pass2:
            messages.info(request, 'Password doesn\'t match')
            return redirect('register')
        else:
            messages.info(request, 'User : \''+username +
                          '\' added successfully')
            user = User.objects.create_user(
                username=username, email=email, password=pass1)
            user.save()
            return redirect('login')
    else:
        return render(request, 'register.html')


def country_load(request):
    file1 = open("C:\\Users\\DELL\\OneDrive\\Desktop\\Full Stack Web Development\\Django\\Django project\\ecommerce\\clothify\\store\\country.csv", "r")
    countries = file1.readlines()
    for country in countries:
        if country.strip().lower() == 'country':
            continue
        c = Countries(country=country.strip())
        c.save()
    file1 = open("C:\\Users\\DELL\\OneDrive\\Desktop\\Full Stack Web Development\\Django\\Django project\\ecommerce\\clothify\\store\\country_to_state.csv", "r")
    countrie_states = file1.readlines()
    for country_state in countrie_states:
        country, state = country_state.rsplit(",", 1)
        if country.strip().lower() == 'country':
            continue
        c = Countries(country=country.strip())
        cs = Country_to_state(country=c, state=state.strip())
        cs.save()
    return redirect('profile')


def states_load(request):
    country = request.POST.get('country_id')
    states = Country_to_state.objects.filter(country_id=country).all()
    states_list = []
    for state in states:
        if state.state not in states_list:
            states_list.append(state.state)
    states_dict = {'states': states_list}
    return JsonResponse(states_dict)


def profile(request):
    if request.user.is_authenticated == False or request.user.is_staff == True:
        return redirect('/')
    if request.method == 'POST':
        name = request.POST.get('name')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip = request.POST.get('zip')
        if name == '' or address1 == '' or city == '' or zip == '':
            messages.info(
                request, '1 or more fields with asterisk (*) are blank')
            return redirect('profile')
        elif country == 'Select Country' or country == '' or country is None:
            messages.info(request, 'Please select country')
            return redirect('profile')
        elif state == 'Select State' or state == '' or state is None:
            messages.info(request, 'Please select state')
            return redirect('profile')
        country_object = Countries.objects.filter(country=country).first()
        country_state_object = Country_to_state.objects.filter(
            country=country_object, state=state).first()
        user_object = User.objects.filter(username=request.user).first()
        customer_object = Customer_model(name=name, address1=address1, address2=address2, city=city,
                                         zip=zip, country=country_object, state=country_state_object, user=user_object)
        customer_object.save()
        messages.info(request, 'Details added successfully')
        return redirect('profile')
    else:
        if User.objects.filter(username=request.user).first() is None:
            return redirect('/')
        else:
            countries_object = Countries.objects.all()
            country_list = []
            for country in countries_object:
                country_list.append(country.country)
            context = {'countries': country_list}
            return render(request, 'profile.html', context)


def address(request):
    if request.user.is_authenticated == False:
        return redirect('/')
    if request.user.is_staff == True:
        return redirect('/')
    user_object = User.objects.filter(username=request.user).first()
    if user_object is None:
        return redirect('/')

    user_id = User.objects.filter(username=request.user).first().id
    customer_object = Customer_model.objects.filter(
        user=user_id).all()
    address_dict = {}
    count = 1
    for customer in customer_object:
        address_dict[count] = {}
        address_dict[count]['name'] = customer.name
        address_dict[count]['address1'] = customer.address1
        address_dict[count]['address2'] = customer.address2
        address_dict[count]['city'] = customer.city
        address_dict[count]['zip'] = customer.zip
        address_dict[count]['country'] = customer.country.country
        address_dict[count]['state'] = customer.state.state
        # address_dict[count].append(customer.name)
        # address_dict[count].append(customer.address1)
        # address_dict[count].append(customer.address2)
        # address_dict[count].append(customer.city)
        # address_dict[count].append(customer.zip)
        # address_dict[count].append(customer.country.country)
        # address_dict[count].append(customer.state.state)
        count += 1
    context = {'addresses': address_dict}
    print(address_dict)
    return render(request, 'address.html', context)


def change_password(request):
    if request.user.is_authenticated == False:
        return redirect('/')
    if request.method == 'POST':
        current_password = request.POST.get('password')
        new_password_1 = request.POST.get('newPassword1')
        new_password_2 = request.POST.get('newPassword2')
        user_str = str(request.user)

        user = auth.authenticate(username=user_str, password=current_password)
        if user is None:
            messages.info(request, 'Incorrect - Current password')
            return redirect('change_password')
        if new_password_1 != new_password_2:
            messages.info(request, 'Password doesn\'t match')
            return redirect('change_password')
        user_object = User.objects.get(username=user_str)
        user_object.set_password(new_password_1)
        user_object.save()
        messages.info(request, 'Password changed successfully')
        return redirect('login')
    return render(request, 'change_password.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def seller_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(
            username=username, password=password)
        if user.is_staff == False:
            messages.warning(
                request, 'Customer Credentials - kindly login as Seller Credentials')
            return redirect('seller_login')
        if(user is not None):
            auth.login(request, user)
            return redirect('seller_view_products')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('seller_login')
    else:
        return render(request, 'seller_login.html')


def seller_register(request):
    username = request.POST.get('selller_register_username')
    email = request.POST.get('selller_register_email')
    pass1 = request.POST.get('selller_register_password1')
    pass2 = request.POST.get('selller_register_password2')
    if username == '' or email == '' or pass1 == '' or pass2 == '':
        messages.info(request, 'Mandatory (*) field can\'t be blank')
        return redirect('seller_register')
    if request.method == 'POST':
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already used')
            return redirect('seller_register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already registered')
            return redirect('seller_register')
        elif pass1 != pass2:
            messages.info(request, 'Password doesn\'t match')
            return redirect('seller_register')
        else:
            messages.info(request, 'Seller : \''+username +
                          '\' added successfully')
            user = User.objects.create_user(
                username=username, email=email, password=pass1, is_staff=True)
            user.save()
            return redirect('seller_login')
    else:
        return render(request, 'seller_register.html')


def seller_home(request):
    return render(request, 'seller_view_products.html')


def seller_new_product(request):
    if request.user.is_authenticated == False or request.user.is_staff == False:
        return redirect('/')
    if request.method == 'POST':
        title = request.POST.get('title')
        brand = request.POST.get('brand')
        market_price = int(request.POST.get('mrp'))
        discounted_price = int(request.POST.get('price'))
        category = request.POST.get('category')
        description = request.POST.get('description')
        if(len(request.FILES) != 0):
            image = request.FILES['image']
            print(image)
        else:
            messages.info(
                request, 'Image is blank')
            return redirect('seller_new_product')
        sub_category = request.POST.get('sub-category')
        size_list = request.POST.getlist('size-check')
        if title == '' or brand == '' or market_price == '' or discounted_price == '' or category == '' or sub_category == '' or description == '':
            messages.info(
                request, '1 or more fields with asterisk (*) are blank')
            return redirect('seller_new_product')
        elif title is None or brand is None or market_price is None or discounted_price is None or category is None or sub_category is None or description is None:
            messages.info(
                request, '1 or more fields with asterisk (*) are blank')
            return redirect('seller_new_product')
        elif size_list == []:
            messages.info(request, "Please select size")
            return redirect('seller_new_product')
        size_1 = False
        size_2 = False
        size_3 = False
        size_4 = False
        size_5 = False
        size_6 = False
        size_7 = False
        size_8 = False
        size_9 = False
        size_10 = False
        size_11 = False
        size_12 = False
        size_13 = False
        size_14 = False
        size_15 = False
        size_1_quantity = -1
        size_2_quantity = -1
        size_3_quantity = -1
        size_4_quantity = -1
        size_5_quantity = -1
        size_6_quantity = -1
        size_7_quantity = -1
        size_8_quantity = -1
        size_9_quantity = -1
        size_10_quantity = -1
        size_11_quantity = -1
        size_12_quantity = -1
        size_13_quantity = -1
        size_14_quantity = -1
        size_15_quantity = -1
        size_1_quantity_sold = -1
        size_2_quantity_sold = -1
        size_3_quantity_sold = -1
        size_4_quantity_sold = -1
        size_5_quantity_sold = -1
        size_6_quantity_sold = -1
        size_7_quantity_sold = -1
        size_8_quantity_sold = -1
        size_9_quantity_sold = -1
        size_10_quantity_sold = -1
        size_11_quantity_sold = -1
        size_12_quantity_sold = -1
        size_13_quantity_sold = -1
        size_14_quantity_sold = -1
        size_15_quantity_sold = -1
        if((category == 'Men\'s' or category == 'Women\'s') and sub_category == "Top-wear"):
            for size in size_list:
                if size == "S":
                    size_1 = True
                    size_1_quantity = int(request.POST.get('size-1-quantity'))
                    size_1_quantity_sold = 0
                elif size == "M":
                    size_2 = True
                    size_2_quantity = int(request.POST.get('size-2-quantity'))
                    size_2_quantity_sold = 0
                elif size == "L":
                    size_3 = True
                    size_3_quantity = int(request.POST.get('size-3-quantity'))
                    size_3_quantity_sold = 0
                elif size == "XL":
                    size_4 = True
                    size_4_quantity = int(request.POST.get('size-4-quantity'))
                    size_4_quantity_sold = 0
        elif((category == 'Men\'s' or category == 'Women\'s') and sub_category == "Bottom-wear"):
            for size in size_list:
                if size == "28":
                    size_1 = True
                    size_1_quantity = int(request.POST.get('size-1-quantity'))
                    size_1_quantity_sold = 0
                elif size == "30":
                    size_2 = True
                    size_2_quantity = int(request.POST.get('size-2-quantity'))
                    size_2_quantity_sold = 0
                elif size == "32":
                    size_3 = True
                    size_3_quantity = int(request.POST.get('size-3-quantity'))
                    size_3_quantity_sold = 0
                elif size == "34":
                    size_4 = True
                    size_4_quantity = int(request.POST.get('size-4-quantity'))
                    size_4_quantity_sold = 0
                elif size == "36":
                    size_5 = True
                    size_5_quantity = int(request.POST.get('size-5-quantity'))
                    size_5_quantity_sold = 0
        elif((category == 'Men\'s' or category == 'Women\'s') and sub_category == "Foot-wear"):
            for size in size_list:
                if size == "UK-6":
                    size_1 = True
                    size_1_quantity = int(request.POST.get('size-1-quantity'))
                    size_1_quantity_sold = 0
                elif size == "UK-7":
                    size_2 = True
                    size_2_quantity = int(request.POST.get('size-2-quantity'))
                    size_2_quantity_sold = 0
                elif size == "UK-8":
                    size_3 = True
                    size_3_quantity = int(request.POST.get('size-3-quantity'))
                    size_3_quantity_sold = 0
                elif size == "UK-9":
                    size_4 = True
                    size_4_quantity = int(request.POST.get('size-4-quantity'))
                    size_4_quantity_sold = 0
                elif size == "UK-10":
                    size_5 = True
                    size_5_quantity = int(request.POST.get('size-5-quantity'))
                    size_5_quantity_sold = 0
                elif size == "UK-11":
                    size_6 = True
                    size_6_quantity = int(request.POST.get('size-6-quantity'))
                    size_6_quantity_sold = 0
        elif(category == 'Kid\'s' and (sub_category == 'Top-wear' or sub_category == 'Bottom-wear')):
            for size in size_list:
                if size == '1-2Y':
                    size_1 = True
                    size_1_quantity = int(request.POST.get('size-1-quantity'))
                    size_1_quantity_sold = 0
                if size == '2-3Y':
                    size_2 = True
                    size_2_quantity = int(request.POST.get('size-2-quantity'))
                    size_2_quantity_sold = 0
                if size == '3-4Y':
                    size_3 = True
                    size_3_quantity = int(request.POST.get('size-3-quantity'))
                    size_3_quantity_sold = 0
                if size == '4-5Y':
                    size_4 = True
                    size_4_quantity = int(request.POST.get('size-4-quantity'))
                    size_4_quantity_sold = 0
                if size == '5-6Y':
                    size_5 = True
                    size_5_quantity = int(request.POST.get('size-5-quantity'))
                    size_5_quantity_sold = 0
                if size == '6-7Y':
                    size_6 = True
                    size_6_quantity = int(request.POST.get('size-6-quantity'))
                    size_6_quantity_sold = 0
                if size == '7-8Y':
                    size_7 = True
                    size_7_quantity = int(request.POST.get('size-7-quantity'))
                    size_7_quantity_sold = 0
                if size == '8-9Y':
                    size_8 = True
                    size_8_quantity = int(request.POST.get('size-8-quantity'))
                    size_8_quantity_sold = 0
                if size == '9-10Y':
                    size_9 = True
                    size_9_quantity = int(request.POST.get('size-9-quantity'))
                    size_9_quantity_sold = 0
                if size == '10-11Y':
                    size_10 = True
                    size_10_quantity = int(
                        request.POST.get('size-10-quantity'))
                    size_10_quantity_sold = 0
                if size == '11-12Y':
                    size_11 = True
                    size_11_quantity = int(
                        request.POST.get('size-11-quantity'))
                    size_11_quantity_sold = 0
        elif(category == 'Kid\'s' and sub_category == 'Foot-wear'):
            for size in size_list:
                if size == '1-1.5Y':
                    size_1 = True
                    size_1_quantity = int(request.POST.get('size-1-quantity'))
                    size_1_quantity_sold = 0
                if size == '1.5-2Y':
                    size_2 = True
                    size_2_quantity = int(request.POST.get('size-2-quantity'))
                    size_2_quantity_sold = 0
                if size == '2-2.5Y':
                    size_3 = True
                    size_3_quantity = int(request.POST.get('size-3-quantity'))
                    size_3_quantity_sold = 0
                if size == '2.5-3Y':
                    size_4 = True
                    size_4_quantity = int(request.POST.get('size-4-quantity'))
                    size_4_quantity_sold = 0
                if size == '3-3.5Y':
                    size_5 = True
                    size_5_quantity = int(request.POST.get('size-5-quantity'))
                    size_5_quantity_sold = 0
                if size == '3.5-4Y':
                    size_6 = True
                    size_6_quantity = int(request.POST.get('size-6-quantity'))
                    size_6_quantity_sold = 0
                if size == '4-4.5Y':
                    size_7 = True
                    size_7_quantity = int(request.POST.get('size-7-quantity'))
                    size_7_quantity_sold = 0
                if size == '4.5-5Y':
                    size_8 = True
                    size_8_quantity = int(request.POST.get('size-8-quantity'))
                    size_8_quantity_sold = 0
                if size == '5-6Y':
                    size_9 = True
                    size_9_quantity = int(request.POST.get('size-9-quantity'))
                    size_9_quantity_sold = 0
                if size == '6-7Y':
                    size_10 = True
                    size_10_quantity = int(
                        request.POST.get('size-10-quantity'))
                    size_10_quantity_sold = 0
                if size == '7-8Y':
                    size_11 = True
                    size_11_quantity = int(
                        request.POST.get('size-11-quantity'))
                    size_11_quantity_sold = 0
                if size == '8-9Y':
                    size_12 = True
                    size_12_quantity = int(
                        request.POST.get('size-12-quantity'))
                    size_12_quantity_sold = 0
                if size == '9-10Y':
                    size_13 = True
                    size_13_quantity = int(
                        request.POST.get('size-13-quantity'))
                    size_13_quantity_sold = 0
                if size == '10-11Y':
                    size_14 = True
                    size_14_quantity = int(
                        request.POST.get('size-14-quantity'))
                    size_14_quantity_sold = 0
                if size == '11-12Y':
                    size_15 = True
                    size_15_quantity = int(
                        request.POST.get('size-15-quantity'))
                    size_15_quantity_sold = 0
        user_object = User.objects.filter(username=request.user).first()
        try:
            product_object = Products(title=title, brand=brand, market_price=market_price, discounted_price=discounted_price,
                                      image=image, category=category, sub_category=sub_category, description=description,
                                      size_1=size_1, size_2=size_2, size_3=size_3, size_4=size_4, size_5=size_5, size_6=size_6, size_7=size_7, size_8=size_8, size_9=size_9, size_10=size_10, size_11=size_11, size_12=size_12, size_13=size_13, size_14=size_14, size_15=size_15,
                                      size_1_quantity=size_1_quantity, size_2_quantity=size_2_quantity, size_3_quantity=size_3_quantity, size_4_quantity=size_4_quantity, size_5_quantity=size_5_quantity, size_6_quantity=size_6_quantity, size_7_quantity=size_7_quantity, size_8_quantity=size_8_quantity, size_9_quantity=size_9_quantity, size_10_quantity=size_10_quantity, size_11_quantity=size_11_quantity, size_12_quantity=size_12_quantity, size_13_quantity=size_13_quantity, size_14_quantity=size_14_quantity, size_15_quantity=size_15_quantity,
                                      size_1_quantity_sold=size_1_quantity_sold, size_2_quantity_sold=size_2_quantity_sold, size_3_quantity_sold=size_3_quantity_sold, size_4_quantity_sold=size_4_quantity_sold, size_5_quantity_sold=size_5_quantity_sold, size_6_quantity_sold=size_6_quantity_sold, size_7_quantity_sold=size_7_quantity_sold, size_8_quantity_sold=size_8_quantity_sold, size_9_quantity_sold=size_9_quantity_sold, size_10_quantity_sold=size_10_quantity_sold, size_11_quantity_sold=size_11_quantity_sold, size_12_quantity_sold=size_12_quantity_sold, size_13_quantity_sold=size_13_quantity_sold, size_14_quantity_sold=size_14_quantity_sold, size_15_quantity_sold=size_15_quantity_sold,
                                      user=user_object)
            product_object.save()
        except IntegrityError:
            messages.info(request, 'Product already exists')
            return redirect('seller_new_product')
        messages.info(request, 'Details added successfully')
        return redirect('seller_new_product')
    else:
        return render(request, 'seller_new_product.html')


def seller_update_product(request, product_id):
    if request.user.is_authenticated == False or request.user.is_staff == False:
        return redirect('/')
    if request.method == 'POST':
        if 'remove' in request.POST:
            record = Products.objects.get(id=product_id)
            os.remove(record.image.path)
            record.delete()
            return redirect('/seller_view_products')
        elif 'update_product' in request.POST:
            product = Products.objects.filter(id=product_id).first()
            category = product.category
            sub_category = product.sub_category
            market_price = request.POST.get('mrp')
            discounted_price = request.POST.get('price')
            description = request.POST.get('description')
            if(len(request.FILES) != 0):
                image = request.FILES['image']
                print("Image", image)
                image_flag = 1
            else:
                image_flag = 0
                print("No Image")
            size_list = request.POST.getlist('size-check')
            if market_price == '' or discounted_price == '' or description == '':
                messages.info(
                    request, '1 or more fields with asterisk (*) are blank')
                return redirect('/'+'seller_update_product/'+str(product_id))
            elif market_price is None or discounted_price is None or description is None:
                messages.info(
                    request, '1 or more fields with asterisk (*) are blank')
                return redirect('/'+'seller_update_product/'+str(product_id))
            elif int(market_price) == 0 or int(discounted_price) == 0:
                messages.info(
                    request, 'Either Market price or Discounted Price is 0')
                url = '/'+'seller_update_product/'+str(product_id)
                return redirect(url)
            elif size_list == []:
                messages.info(request, "Please add atleast 1 size")
                return redirect('/'+'seller_update_product/'+str(product_id))
            elif int(market_price) < int(discounted_price):
                messages.info(
                    request, "Market price is less than Discounted price")
                return redirect('/'+'seller_update_product/'+str(product_id))
            market_price = int(market_price)
            discounted_price = int(discounted_price)
            size_1 = False
            size_2 = False
            size_3 = False
            size_4 = False
            size_5 = False
            size_6 = False
            size_7 = False
            size_8 = False
            size_9 = False
            size_10 = False
            size_11 = False
            size_12 = False
            size_13 = False
            size_14 = False
            size_15 = False
            size_1_quantity = -1
            size_2_quantity = -1
            size_3_quantity = -1
            size_4_quantity = -1
            size_5_quantity = -1
            size_6_quantity = -1
            size_7_quantity = -1
            size_8_quantity = -1
            size_9_quantity = -1
            size_10_quantity = -1
            size_11_quantity = -1
            size_12_quantity = -1
            size_13_quantity = -1
            size_14_quantity = -1
            size_15_quantity = -1
            size_1_quantity_sold = -1
            size_2_quantity_sold = -1
            size_3_quantity_sold = -1
            size_4_quantity_sold = -1
            size_5_quantity_sold = -1
            size_6_quantity_sold = -1
            size_7_quantity_sold = -1
            size_8_quantity_sold = -1
            size_9_quantity_sold = -1
            size_10_quantity_sold = -1
            size_11_quantity_sold = -1
            size_12_quantity_sold = -1
            size_13_quantity_sold = -1
            size_14_quantity_sold = -1
            size_15_quantity_sold = -1
            if((category == 'Men\'s' or category == 'Women\'s') and sub_category == "Top-wear"):
                for size in size_list:
                    if size == "S":
                        size_1 = True
                        size_1_quantity = int(
                            request.POST.get('size-1-quantity'))
                        size_1_quantity_sold = 0
                    elif size == "M":
                        size_2 = True
                        size_2_quantity = int(
                            request.POST.get('size-2-quantity'))
                        size_2_quantity_sold = 0
                    elif size == "L":
                        size_3 = True
                        size_3_quantity = int(
                            request.POST.get('size-3-quantity'))
                        size_3_quantity_sold = 0
                    elif size == "XL":
                        size_4 = True
                        size_4_quantity = int(
                            request.POST.get('size-4-quantity'))
                        size_4_quantity_sold = 0
            elif((category == 'Men\'s' or category == 'Women\'s') and sub_category == "Bottom-wear"):
                for size in size_list:
                    if size == "28":
                        size_1 = True
                        size_1_quantity = int(
                            request.POST.get('size-1-quantity'))
                        size_1_quantity_sold = 0
                    elif size == "30":
                        size_2 = True
                        size_2_quantity = int(
                            request.POST.get('size-2-quantity'))
                        size_2_quantity_sold = 0
                    elif size == "32":
                        size_3 = True
                        size_3_quantity = int(
                            request.POST.get('size-3-quantity'))
                        size_3_quantity_sold = 0
                    elif size == "34":
                        size_4 = True
                        size_4_quantity = int(
                            request.POST.get('size-4-quantity'))
                        size_4_quantity_sold = 0
                    elif size == "36":
                        size_5 = True
                        size_5_quantity = int(
                            request.POST.get('size-5-quantity'))
                        size_5_quantity_sold = 0
            elif((category == 'Men\'s' or category == 'Women\'s') and sub_category == "Foot-wear"):
                for size in size_list:
                    if size == "UK-6":
                        size_1 = True
                        size_1_quantity = int(
                            request.POST.get('size-1-quantity'))
                        size_1_quantity_sold = 0
                    elif size == "UK-7":
                        size_2 = True
                        size_2_quantity = int(
                            request.POST.get('size-2-quantity'))
                        size_2_quantity_sold = 0
                    elif size == "UK-8":
                        size_3 = True
                        size_3_quantity = int(
                            request.POST.get('size-3-quantity'))
                        size_3_quantity_sold = 0
                    elif size == "UK-9":
                        size_4 = True
                        size_4_quantity = int(
                            request.POST.get('size-4-quantity'))
                        size_4_quantity_sold = 0
                    elif size == "UK-10":
                        size_5 = True
                        size_5_quantity = int(
                            request.POST.get('size-5-quantity'))
                        size_5_quantity_sold = 0
                    elif size == "UK-11":
                        size_6 = True
                        size_6_quantity = int(
                            request.POST.get('size-6-quantity'))
                        size_6_quantity_sold = 0
            elif(category == 'Kid\'s' and (sub_category == 'Top-wear' or sub_category == 'Bottom-wear')):
                for size in size_list:
                    if size == '1-2Y':
                        size_1 = True
                        size_1_quantity = int(
                            request.POST.get('size-1-quantity'))
                        size_1_quantity_sold = 0
                    if size == '2-3Y':
                        size_2 = True
                        size_2_quantity = int(
                            request.POST.get('size-2-quantity'))
                        size_2_quantity_sold = 0
                    if size == '3-4Y':
                        size_3 = True
                        size_3_quantity = int(
                            request.POST.get('size-3-quantity'))
                        size_3_quantity_sold = 0
                    if size == '4-5Y':
                        size_4 = True
                        size_4_quantity = int(
                            request.POST.get('size-4-quantity'))
                        size_4_quantity_sold = 0
                    if size == '5-6Y':
                        size_5 = True
                        size_5_quantity = int(
                            request.POST.get('size-5-quantity'))
                        size_5_quantity_sold = 0
                    if size == '6-7Y':
                        size_6 = True
                        size_6_quantity = int(
                            request.POST.get('size-6-quantity'))
                        size_6_quantity_sold = 0
                    if size == '7-8Y':
                        size_7 = True
                        size_7_quantity = int(
                            request.POST.get('size-7-quantity'))
                        size_7_quantity_sold = 0
                    if size == '8-9Y':
                        size_8 = True
                        size_8_quantity = int(
                            request.POST.get('size-8-quantity'))
                        size_8_quantity_sold = 0
                    if size == '9-10Y':
                        size_9 = True
                        size_9_quantity = int(
                            request.POST.get('size-9-quantity'))
                        size_9_quantity_sold = 0
                    if size == '10-11Y':
                        size_10 = True
                        size_10_quantity = int(
                            request.POST.get('size-10-quantity'))
                        size_10_quantity_sold = 0
                    if size == '11-12Y':
                        size_11 = True
                        size_11_quantity = int(
                            request.POST.get('size-11-quantity'))
                        size_11_quantity_sold = 0
            elif(category == 'Kid\'s' and sub_category == 'Foot-wear'):
                for size in size_list:
                    if size == '1-1.5Y':
                        size_1 = True
                        size_1_quantity = int(
                            request.POST.get('size-1-quantity'))
                        size_1_quantity_sold = 0
                    if size == '1.5-2Y':
                        size_2 = True
                        size_2_quantity = int(
                            request.POST.get('size-2-quantity'))
                        size_2_quantity_sold = 0
                    if size == '2-2.5Y':
                        size_3 = True
                        size_3_quantity = int(
                            request.POST.get('size-3-quantity'))
                        size_3_quantity_sold = 0
                    if size == '2.5-3Y':
                        size_4 = True
                        size_4_quantity = int(
                            request.POST.get('size-4-quantity'))
                        size_4_quantity_sold = 0
                    if size == '3-3.5Y':
                        size_5 = True
                        size_5_quantity = int(
                            request.POST.get('size-5-quantity'))
                        size_5_quantity_sold = 0
                    if size == '3.5-4Y':
                        size_6 = True
                        size_6_quantity = int(
                            request.POST.get('size-6-quantity'))
                        size_6_quantity_sold = 0
                    if size == '4-4.5Y':
                        size_7 = True
                        size_7_quantity = int(
                            request.POST.get('size-7-quantity'))
                        size_7_quantity_sold = 0
                    if size == '4.5-5Y':
                        size_8 = True
                        size_8_quantity = int(
                            request.POST.get('size-8-quantity'))
                        size_8_quantity_sold = 0
                    if size == '5-6Y':
                        size_9 = True
                        size_9_quantity = int(
                            request.POST.get('size-9-quantity'))
                        size_9_quantity_sold = 0
                    if size == '6-7Y':
                        size_10 = True
                        size_10_quantity = int(
                            request.POST.get('size-10-quantity'))
                        size_10_quantity_sold = 0
                    if size == '7-8Y':
                        size_11 = True
                        size_11_quantity = int(
                            request.POST.get('size-11-quantity'))
                        size_11_quantity_sold = 0
                    if size == '8-9Y':
                        size_12 = True
                        size_12_quantity = int(
                            request.POST.get('size-12-quantity'))
                        size_12_quantity_sold = 0
                    if size == '9-10Y':
                        size_13 = True
                        size_13_quantity = int(
                            request.POST.get('size-13-quantity'))
                        size_13_quantity_sold = 0
                    if size == '10-11Y':
                        size_14 = True
                        size_14_quantity = int(
                            request.POST.get('size-14-quantity'))
                        size_14_quantity_sold = 0
                    if size == '11-12Y':
                        size_15 = True
                        size_15_quantity = int(
                            request.POST.get('size-15-quantity'))
                        size_15_quantity_sold = 0
            print(image_flag)
            if(image_flag == 0):
                product = Products.objects.filter(id=product_id).first()
                product.market_price = market_price
                product.discounted_price = discounted_price
                product.description = description
                product.size_1 = size_1
                product.size_2 = size_2
                product.size_3 = size_3
                product.size_4 = size_4
                product.size_5 = size_5
                product.size_6 = size_6
                product.size_7 = size_7
                product.size_8 = size_8
                product.size_9 = size_9
                product.size_10 = size_10
                product.size_11 = size_11
                product.size_12 = size_12
                product.size_13 = size_13
                product.size_14 = size_14
                product.size_15 = size_15
                product.size_1_quantity = size_1_quantity
                product.size_2_quantity = size_2_quantity
                product.size_3_quantity = size_3_quantity
                product.size_4_quantity = size_4_quantity
                product.size_5_quantity = size_5_quantity
                product.size_6_quantity = size_6_quantity
                product.size_7_quantity = size_7_quantity
                product.size_8_quantity = size_8_quantity
                product.size_9_quantity = size_9_quantity
                product.size_10_quantity = size_10_quantity
                product.size_11_quantity = size_11_quantity
                product.size_12_quantity = size_12_quantity
                product.size_13_quantity = size_13_quantity
                product.size_14_quantity = size_14_quantity
                product.size_15_quantity = size_15_quantity
                product.size_1_quantity_sold = size_1_quantity_sold
                product.size_2_quantity_sold = size_2_quantity_sold
                product.size_3_quantity_sold = size_3_quantity_sold
                product.size_4_quantity_sold = size_4_quantity_sold
                product.size_5_quantity_sold = size_5_quantity_sold
                product.size_6_quantity_sold = size_6_quantity_sold
                product.size_7_quantity_sold = size_7_quantity_sold
                product.size_8_quantity_sold = size_8_quantity_sold
                product.size_9_quantity_sold = size_9_quantity_sold
                product.size_10_quantity_sold = size_10_quantity_sold
                product.size_11_quantity_sold = size_11_quantity_sold
                product.size_12_quantity_sold = size_12_quantity_sold
                product.size_13_quantity_sold = size_13_quantity_sold
                product.size_14_quantity_sold = size_14_quantity_sold
                product.size_15_quantity_sold = size_15_quantity_sold
                product.save()
            else:
                product = Products.objects.filter(id=product_id).first()
                product.market_price = market_price
                product.discounted_price = discounted_price
                product.description = description
                product.size_1 = size_1
                product.size_2 = size_2
                product.size_3 = size_3
                product.size_4 = size_4
                product.size_5 = size_5
                product.size_6 = size_6
                product.size_7 = size_7
                product.size_8 = size_8
                product.size_9 = size_9
                product.size_10 = size_10
                product.size_11 = size_11
                product.size_12 = size_12
                product.size_13 = size_13
                product.size_14 = size_14
                product.size_15 = size_15
                product.size_1_quantity = size_1_quantity
                product.size_2_quantity = size_2_quantity
                product.size_3_quantity = size_3_quantity
                product.size_4_quantity = size_4_quantity
                product.size_5_quantity = size_5_quantity
                product.size_6_quantity = size_6_quantity
                product.size_7_quantity = size_7_quantity
                product.size_8_quantity = size_8_quantity
                product.size_9_quantity = size_9_quantity
                product.size_10_quantity = size_10_quantity
                product.size_11_quantity = size_11_quantity
                product.size_12_quantity = size_12_quantity
                product.size_13_quantity = size_13_quantity
                product.size_14_quantity = size_14_quantity
                product.size_15_quantity = size_15_quantity
                product.size_1_quantity_sold = size_1_quantity_sold
                product.size_2_quantity_sold = size_2_quantity_sold
                product.size_3_quantity_sold = size_3_quantity_sold
                product.size_4_quantity_sold = size_4_quantity_sold
                product.size_5_quantity_sold = size_5_quantity_sold
                product.size_6_quantity_sold = size_6_quantity_sold
                product.size_7_quantity_sold = size_7_quantity_sold
                product.size_8_quantity_sold = size_8_quantity_sold
                product.size_9_quantity_sold = size_9_quantity_sold
                product.size_10_quantity_sold = size_10_quantity_sold
                product.size_11_quantity_sold = size_11_quantity_sold
                product.size_12_quantity_sold = size_12_quantity_sold
                product.size_13_quantity_sold = size_13_quantity_sold
                product.size_14_quantity_sold = size_14_quantity_sold
                product.size_15_quantity_sold = size_15_quantity_sold
                os.remove(product.image.path)
                product.image = image
                product.save()
            return redirect('/seller_view_products')
    item_dict = {}
    product = Products.objects.filter(id=product_id).first()
    item_dict['id'] = product_id
    item_dict['title'] = product.title
    item_dict['brand'] = product.brand
    item_dict['market_price'] = product.market_price
    item_dict['discounted_price'] = product.discounted_price
    item_dict['image'] = "/"+str(product.image)
    item_dict['category'] = product.category
    item_dict['sub_category'] = product.sub_category
    item_dict['description'] = product.description
    category = product.category
    sub_category = product.sub_category
    size_dict = {}
    if category == 'Men\'s' or category == 'Women\'s':
        if sub_category == 'Top-wear':
            size_dict['1'] = {}
            size_dict['1']['quantity'] = product.size_1_quantity
            size_dict['1']['value'] = 'S'
            size_dict['1']['label'] = 'Small (S)'

            size_dict['2'] = {}
            size_dict['2']['quantity'] = product.size_2_quantity
            size_dict['2']['value'] = 'M'
            size_dict['2']['label'] = 'Medium (M)'

            size_dict['3'] = {}
            size_dict['3']['quantity'] = product.size_3_quantity
            size_dict['3']['value'] = 'L'
            size_dict['3']['label'] = 'Large (L)'

            size_dict['4'] = {}
            size_dict['4']['quantity'] = product.size_4_quantity
            size_dict['4']['value'] = 'XL'
            size_dict['4']['label'] = 'Extra Large (XL)'
        elif sub_category == 'Foot-wear':
            size_dict['1'] = {}
            size_dict['1']['quantity'] = product.size_1_quantity
            size_dict['1']['value'] = 'UK-6'
            size_dict['1']['label'] = 'UK-6'

            size_dict['2'] = {}
            size_dict['2']['quantity'] = product.size_2_quantity
            size_dict['2']['value'] = 'UK-7'
            size_dict['2']['label'] = 'UK-7'

            size_dict['3'] = {}
            size_dict['3']['quantity'] = product.size_3_quantity
            size_dict['3']['value'] = 'UK-8'
            size_dict['3']['label'] = 'UK-8'

            size_dict['4'] = {}
            size_dict['4']['quantity'] = product.size_4_quantity
            size_dict['4']['value'] = 'UK-9'
            size_dict['4']['label'] = 'UK-9'

            size_dict['5'] = {}
            size_dict['5']['quantity'] = product.size_5_quantity
            size_dict['5']['value'] = 'UK-10'
            size_dict['5']['label'] = 'UK-10'

            size_dict['6'] = {}
            size_dict['6']['quantity'] = product.size_6_quantity
            size_dict['6']['value'] = 'UK-11'
            size_dict['6']['label'] = 'UK-11'
        else:
            size_dict['1'] = {}
            size_dict['1']['quantity'] = product.size_1_quantity
            size_dict['1']['value'] = '28'
            size_dict['1']['label'] = '28'

            size_dict['2'] = {}
            size_dict['2']['quantity'] = product.size_2_quantity
            size_dict['2']['value'] = '30'
            size_dict['2']['label'] = '30'

            size_dict['3'] = {}
            size_dict['3']['quantity'] = product.size_3_quantity
            size_dict['3']['value'] = '32'
            size_dict['3']['label'] = '32'

            size_dict['4'] = {}
            size_dict['4']['quantity'] = product.size_4_quantity
            size_dict['4']['value'] = '34'
            size_dict['4']['label'] = '34'

            size_dict['5'] = {}
            size_dict['5']['quantity'] = product.size_5_quantity
            size_dict['5']['value'] = '36'
            size_dict['5']['label'] = '36'
    else:
        if sub_category == 'Top-wear' or sub_category == 'Bottom-wear':
            size_dict['1'] = {}
            size_dict['1']['quantity'] = product.size_1_quantity
            size_dict['1']['value'] = '1-2Y'
            size_dict['1']['label'] = '1-2Y'

            size_dict['2'] = {}
            size_dict['2']['quantity'] = product.size_2_quantity
            size_dict['2']['value'] = '2-3Y'
            size_dict['2']['label'] = '2-3Y'

            size_dict['3'] = {}
            size_dict['3']['quantity'] = product.size_3_quantity
            size_dict['3']['value'] = '3-4Y'
            size_dict['3']['label'] = '3-4Y'

            size_dict['4'] = {}
            size_dict['4']['quantity'] = product.size_4_quantity
            size_dict['4']['value'] = '4-5Y'
            size_dict['4']['label'] = '4-5Y'

            size_dict['5'] = {}
            size_dict['5']['quantity'] = product.size_5_quantity
            size_dict['5']['value'] = '5-6Y'
            size_dict['5']['label'] = '5-6Y'

            size_dict['6'] = {}
            size_dict['6']['quantity'] = product.size_6_quantity
            size_dict['6']['value'] = '6-7Y'
            size_dict['6']['label'] = '6-7Y'

            size_dict['7'] = {}
            size_dict['7']['quantity'] = product.size_7_quantity
            size_dict['7']['value'] = '7-8Y'
            size_dict['7']['label'] = '7-8Y'

            size_dict['8'] = {}
            size_dict['8']['quantity'] = product.size_8_quantity
            size_dict['8']['value'] = '8-9Y'
            size_dict['8']['label'] = '8-9Y'

            size_dict['9'] = {}
            size_dict['9']['quantity'] = product.size_9_quantity
            size_dict['9']['value'] = '9-10Y'
            size_dict['9']['label'] = '9-10Y'

            size_dict['10'] = {}
            size_dict['10']['quantity'] = product.size_10_quantity
            size_dict['10']['value'] = '10-11Y'
            size_dict['10']['label'] = '10-11Y'

            size_dict['11'] = {}
            size_dict['11']['quantity'] = product.size_11_quantity
            size_dict['11']['value'] = '11-12Y'
            size_dict['11']['label'] = '11-12Y'
        else:
            size_dict['1'] = {}
            size_dict['1']['quantity'] = product.size_1_quantity
            size_dict['1']['value'] = '1-1.5Y'
            size_dict['1']['label'] = '1-1.5Y'

            size_dict['2'] = {}
            size_dict['2']['quantity'] = product.size_2_quantity
            size_dict['2']['value'] = '1.5-2Y'
            size_dict['2']['label'] = '1.5-2Y'

            size_dict['3'] = {}
            size_dict['3']['quantity'] = product.size_3_quantity
            size_dict['3']['value'] = '2-2.5Y'
            size_dict['3']['label'] = '2-2.5Y'

            size_dict['4'] = {}
            size_dict['4']['quantity'] = product.size_4_quantity
            size_dict['4']['value'] = '2.5-3Y'
            size_dict['4']['label'] = '2.5-3Y'

            size_dict['5'] = {}
            size_dict['5']['quantity'] = product.size_5_quantity
            size_dict['5']['value'] = '3-3.5Y'
            size_dict['5']['label'] = '3-3.5Y'

            size_dict['6'] = {}
            size_dict['6']['quantity'] = product.size_6_quantity
            size_dict['6']['value'] = '3.5-4Y'
            size_dict['6']['label'] = '3.5-4Y'

            size_dict['7'] = {}
            size_dict['7']['quantity'] = product.size_7_quantity
            size_dict['7']['value'] = '4-4.5Y'
            size_dict['7']['label'] = '4-4.5Y'

            size_dict['8'] = {}
            size_dict['8']['quantity'] = product.size_8_quantity
            size_dict['8']['value'] = '4.5-5Y'
            size_dict['8']['label'] = '4.5-5Y'

            size_dict['9'] = {}
            size_dict['9']['quantity'] = product.size_9_quantity
            size_dict['9']['value'] = '5-6Y'
            size_dict['9']['label'] = '5-6Y'

            size_dict['10'] = {}
            size_dict['10']['quantity'] = product.size_10_quantity
            size_dict['10']['value'] = '6-7Y'
            size_dict['10']['label'] = '6-7Y'

            size_dict['11'] = {}
            size_dict['11']['quantity'] = product.size_11_quantity
            size_dict['11']['value'] = '7-8Y'
            size_dict['11']['label'] = '7-8Y'

            size_dict['12'] = {}
            size_dict['12']['quantity'] = product.size_12_quantity
            size_dict['12']['value'] = '8-9Y'
            size_dict['12']['label'] = '8-9Y'

            size_dict['13'] = {}
            size_dict['13']['quantity'] = product.size_13_quantity
            size_dict['13']['value'] = '9-10Y'
            size_dict['13']['label'] = '9-10Y'

            size_dict['14'] = {}
            size_dict['14']['quantity'] = product.size_14_quantity
            size_dict['14']['value'] = '10-11Y'
            size_dict['14']['label'] = '10-11Y'

            size_dict['15'] = {}
            size_dict['15']['quantity'] = product.size_15_quantity
            size_dict['15']['value'] = '11-12Y'
            size_dict['15']['label'] = '11-12Y'
    # print(size_dict)
    context = {'item': item_dict, 'size': size_dict}
    return render(request, 'seller_update_product.html', context)


def seller_view_products(request):
    if request.user.is_authenticated == False or request.user.is_staff == False:
        return redirect('/')
    user_object = User.objects.filter(username=request.user).first()
    if user_object is None:
        return redirect('seller_view_products')

    user_id = User.objects.filter(username=request.user).first().id
    product_object = Products.objects.filter(
        user=user_id).all()
    product_dict = {}
    count = 1
    for product in product_object:
        product_dict[count] = {}
        product_dict[count]['id'] = 'seller_productdetail\\'+str(product.id)
        product_dict[count]['title'] = product.title
        product_dict[count]['brand'] = product.brand
        product_dict[count]['market_price'] = product.market_price
        product_dict[count]['discounted_price'] = product.discounted_price
        product_dict[count]['discount'] = round((
            product.market_price - product.discounted_price)/product.market_price*100)
        product_dict[count]['image'] = product.image
        category = product.category
        sub_category = product.sub_category
        sizes_available = []
        if category == 'Men\'s' or category == 'Women\'s':
            if sub_category == 'Top-wear':
                if product.size_1 == True:
                    sizes_available.append('S')
                if product.size_2 == True:
                    sizes_available.append('M')
                if product.size_3 == True:
                    sizes_available.append('L')
                if product.size_4 == True:
                    sizes_available.append('XL')
            elif sub_category == 'Bottom-wear':
                if product.size_1 == True:
                    sizes_available.append('28')
                if product.size_2 == True:
                    sizes_available.append('30')
                if product.size_3 == True:
                    sizes_available.append('32')
                if product.size_4 == True:
                    sizes_available.append('34')
                if product.size_5 == True:
                    sizes_available.append('36')
            else:
                if product.size_1 == True:
                    sizes_available.append('UK-6')
                if product.size_2 == True:
                    sizes_available.append('UK-7')
                if product.size_3 == True:
                    sizes_available.append('UK-8')
                if product.size_4 == True:
                    sizes_available.append('UK-9')
                if product.size_5 == True:
                    sizes_available.append('UK-10')
                if product.size_6 == True:
                    sizes_available.append('UK-11')
        else:
            if sub_category == 'Top-wear' or sub_category == 'Bottom-wear':
                if product.size_1 == True:
                    sizes_available.append('1-2Y')
                if product.size_2 == True:
                    sizes_available.append('2-3Y')
                if product.size_3 == True:
                    sizes_available.append('3-4Y')
                if product.size_4 == True:
                    sizes_available.append('4-5Y')
                if product.size_5 == True:
                    sizes_available.append('5-6Y')
                if product.size_6 == True:
                    sizes_available.append('6-7Y')
                if product.size_7 == True:
                    sizes_available.append('7-8Y')
                if product.size_8 == True:
                    sizes_available.append('8-9Y')
                if product.size_9 == True:
                    sizes_available.append('9-10Y')
                if product.size_10 == True:
                    sizes_available.append('10-11Y')
                if product.size_11 == True:
                    sizes_available.append('11-12Y')
            else:
                if product.size_1 == True:
                    sizes_available.append('1-1.5Y')
                if product.size_2 == True:
                    sizes_available.append('1.5-2Y')
                if product.size_3 == True:
                    sizes_available.append('2-2.5Y')
                if product.size_4 == True:
                    sizes_available.append('2.5-3Y')
                if product.size_5 == True:
                    sizes_available.append('3-3.5Y')
                if product.size_6 == True:
                    sizes_available.append('3.5-4Y')
                if product.size_7 == True:
                    sizes_available.append('4-4.5Y')
                if product.size_8 == True:
                    sizes_available.append('4.5-5Y')
                if product.size_9 == True:
                    sizes_available.append('5-6Y')
                if product.size_10 == True:
                    sizes_available.append('6-7Y')
                if product.size_11 == True:
                    sizes_available.append('7-8Y')
                if product.size_12 == True:
                    sizes_available.append('8-9Y')
                if product.size_13 == True:
                    sizes_available.append('9-10Y')
                if product.size_14 == True:
                    sizes_available.append('10-11Y')
                if product.size_15 == True:
                    sizes_available.append('11-12Y')
        product_dict[count]['sizes_available'] = ', '.join(sizes_available)
        count += 1
    context = {'products': product_dict}
    return render(request, 'seller_view_products.html', context)


def seller_productdetail(request, product_id):
    if request.user.is_authenticated == False or request.user.is_staff == False:
        return redirect('/')
    product_object = Products.objects.filter(id=product_id).first()
    if product_object is None:
        print('Product Doesn\'t Exist')
        messages.info(request, 'Product Doesn\'t Exist')
        return redirect('seller_view_products')
    else:
        product_dict = {}
        product_dict['brand'] = product_object.brand
        product_dict['title'] = product_object.title
        category = product_object.category
        sub_category = product_object.sub_category
        sizes_available = {}
        if category == 'Men\'s' or category == 'Women\'s':
            if sub_category == 'Top-wear':
                if product_object.size_1 == True:
                    sizes_available['S'] = product_object.size_1_quantity
                if product_object.size_2 == True:
                    sizes_available['M'] = product_object.size_2_quantity
                if product_object.size_3 == True:
                    sizes_available['L'] = product_object.size_3_quantity
                if product_object.size_4 == True:
                    sizes_available['XL'] = product_object.size_4_quantity
            elif sub_category == 'Bottom-wear':
                if product_object.size_1 == True:
                    sizes_available['28'] = product_object.size_1_quantity
                if product_object.size_2 == True:
                    sizes_available['30'] = product_object.size_2_quantity
                if product_object.size_3 == True:
                    sizes_available['32'] = product_object.size_3_quantity
                if product_object.size_4 == True:
                    sizes_available['34'] = product_object.size_4_quantity
                if product_object.size_5 == True:
                    sizes_available['36'] = product_object.size_5_quantity
            else:
                if product_object.size_1 == True:
                    sizes_available['UK-6'] = product_object.size_1_quantity
                if product_object.size_2 == True:
                    sizes_available['UK-7'] = product_object.size_2_quantity
                if product_object.size_3 == True:
                    sizes_available['UK-8'] = product_object.size_3_quantity
                if product_object.size_4 == True:
                    sizes_available['UK-9'] = product_object.size_4_quantity
                if product_object.size_5 == True:
                    sizes_available['UK-10'] = product_object.size_5_quantity
                if product_object.size_6 == True:
                    sizes_available['UK-11'] = product_object.size_6_quantity
        else:
            if sub_category == 'Top-wear' or sub_category == 'Bottom-wear':
                if product_object.size_1 == True:
                    sizes_available['1-2Y'] = product_object.size_1_quantity
                if product_object.size_2 == True:
                    sizes_available['2-3Y'] = product_object.size_2_quantity
                if product_object.size_3 == True:
                    sizes_available['3-4Y'] = product_object.size_3_quantity
                if product_object.size_4 == True:
                    sizes_available['4-5Y'] = product_object.size_4_quantity
                if product_object.size_5 == True:
                    sizes_available['5-6Y'] = product_object.size_5_quantity
                if product_object.size_6 == True:
                    sizes_available['6-7Y'] = product_object.size_6_quantity
                if product_object.size_7 == True:
                    sizes_available['7-8Y'] = product_object.size_7_quantity
                if product_object.size_8 == True:
                    sizes_available['8-9Y'] = product_object.size_8_quantity
                if product_object.size_9 == True:
                    sizes_available['9-10Y'] = product_object.size_9_quantity
                if product_object.size_10 == True:
                    sizes_available['10-11Y'] = product_object.size_10_quantity
                if product_object.size_11 == True:
                    sizes_available['11-12Y'] = product_object.size_11_quantity
            else:
                if product_object.size_1 == True:
                    sizes_available['1-1.5Y'] = product_object.size_1_quantity
                if product_object.size_2 == True:
                    sizes_available['1.5-2Y'] = product_object.size_2_quantity
                if product_object.size_3 == True:
                    sizes_available['2-2.5Y'] = product_object.size_3_quantity
                if product_object.size_4 == True:
                    sizes_available['2.5-3Y'] = product_object.size_4_quantity
                if product_object.size_5 == True:
                    sizes_available['3-3.5Y'] = product_object.size_5_quantity
                if product_object.size_6 == True:
                    sizes_available['3.5-4Y'] = product_object.size_6_quantity
                if product_object.size_7 == True:
                    sizes_available['4-4.5Y'] = product_object.size_7_quantity
                if product_object.size_8 == True:
                    sizes_available['4.5-5Y'] = product_object.size_8_quantity
                if product_object.size_9 == True:
                    sizes_available['5-6Y'] = product_object.size_9_quantity
                if product_object.size_10 == True:
                    sizes_available['6-7Y'] = product_object.size_10_quantity
                if product_object.size_11 == True:
                    sizes_available['7-8Y'] = product_object.size_11_quantity
                if product_object.size_12 == True:
                    sizes_available['8-9Y'] = product_object.size_12_quantity
                if product_object.size_13 == True:
                    sizes_available['9-10Y'] = product_object.size_13_quantity
                if product_object.size_14 == True:
                    sizes_available['10-11Y'] = product_object.size_14_quantity
                if product_object.size_15 == True:
                    sizes_available['11-12Y'] = product_object.size_15_quantity
        product_dict['sizes_available'] = sizes_available
        product_dict['market_price'] = product_object.market_price
        product_dict['discounted_price'] = product_object.discounted_price
        product_dict['image'] = "/"+str(product_object.image)
        product_dict['description'] = list(
            product_object.description.split('\r\n'))
        product_dict['id'] = product_object.id
        context = {'product': product_dict}
    return render(request, 'seller_productdetail.html', context)


def view_products(request, category, sub_category):
    products = Products.objects.filter(
        category=category, sub_category=sub_category).order_by('title')
    product_dict = {}
    count = 0
    for product in products:
        product_dict[count] = {}
        product_dict[count]['id'] = '/productdetail/'+str(product.id)
        product_dict[count]['title'] = product.title
        product_dict[count]['brand'] = product.brand
        product_dict[count]['market_price'] = product.market_price
        product_dict[count]['discounted_price'] = product.discounted_price
        product_dict[count]['discount'] = round((
            product.market_price - product.discounted_price)/product.market_price*100)
        image_path_list = str(product.image).split("/")
        image_path_list = image_path_list[1:]
        image_path = "/".join(image_path_list)
        product_dict[count]['image'] = ""+image_path
        sizes_available = []
        if category == 'Men\'s' or category == 'Women\'s':
            if sub_category == 'Top-wear':
                if product.size_1 == True:
                    sizes_available.append('S')
                if product.size_2 == True:
                    sizes_available.append('M')
                if product.size_3 == True:
                    sizes_available.append('L')
                if product.size_4 == True:
                    sizes_available.append('XL')
            elif sub_category == 'Bottom-wear':
                if product.size_1 == True:
                    sizes_available.append('28')
                if product.size_2 == True:
                    sizes_available.append('30')
                if product.size_3 == True:
                    sizes_available.append('32')
                if product.size_4 == True:
                    sizes_available.append('34')
                if product.size_5 == True:
                    sizes_available.append('36')
            else:
                if product.size_1 == True:
                    sizes_available.append('UK-6')
                if product.size_2 == True:
                    sizes_available.append('UK-7')
                if product.size_3 == True:
                    sizes_available.append('UK-8')
                if product.size_4 == True:
                    sizes_available.append('UK-9')
                if product.size_5 == True:
                    sizes_available.append('UK-10')
                if product.size_6 == True:
                    sizes_available.append('UK-11')
        else:
            if sub_category == 'Top-wear' or sub_category == 'Bottom-wear':
                if product.size_1 == True:
                    sizes_available.append('1-2Y')
                if product.size_2 == True:
                    sizes_available.append('2-3Y')
                if product.size_3 == True:
                    sizes_available.append('3-4Y')
                if product.size_4 == True:
                    sizes_available.append('4-5Y')
                if product.size_5 == True:
                    sizes_available.append('5-6Y')
                if product.size_6 == True:
                    sizes_available.append('6-7Y')
                if product.size_7 == True:
                    sizes_available.append('7-8Y')
                if product.size_8 == True:
                    sizes_available.append('8-9Y')
                if product.size_9 == True:
                    sizes_available.append('9-10Y')
                if product.size_10 == True:
                    sizes_available.append('10-11Y')
                if product.size_11 == True:
                    sizes_available.append('11-12Y')
            else:
                if product.size_1 == True:
                    sizes_available.append('1-1.5Y')
                if product.size_2 == True:
                    sizes_available.append('1.5-2Y')
                if product.size_3 == True:
                    sizes_available.append('2-2.5Y')
                if product.size_4 == True:
                    sizes_available.append('2.5-3Y')
                if product.size_5 == True:
                    sizes_available.append('3-3.5Y')
                if product.size_6 == True:
                    sizes_available.append('3.5-4Y')
                if product.size_7 == True:
                    sizes_available.append('4-4.5Y')
                if product.size_8 == True:
                    sizes_available.append('4.5-5Y')
                if product.size_9 == True:
                    sizes_available.append('5-6Y')
                if product.size_10 == True:
                    sizes_available.append('6-7Y')
                if product.size_11 == True:
                    sizes_available.append('7-8Y')
                if product.size_12 == True:
                    sizes_available.append('8-9Y')
                if product.size_13 == True:
                    sizes_available.append('9-10Y')
                if product.size_14 == True:
                    sizes_available.append('10-11Y')
                if product.size_15 == True:
                    sizes_available.append('11-12Y')
        product_dict[count]['sizes_available'] = ', '.join(sizes_available)
        count += 1
    context = {'products': product_dict,
               'category': category, 'sub_category': sub_category}
    return render(request, 'view_products.html', context)


def view_customized_products(request, category, sub_category):
    if request.method == 'POST':
        if request.POST.get('sort_type') != '' and request.POST.get('range') == '':
            sort_type = request.POST.get('sort_type')
            if sort_type == 'Product name : A to Z':
                products = Products.objects.filter(
                    category=category, sub_category=sub_category).order_by('title')
            elif sort_type == 'Product name : Z to A':
                products = Products.objects.filter(
                    category=category, sub_category=sub_category).order_by('-title')
            elif sort_type == 'Price : Low to High':
                products = Products.objects.filter(
                    category=category, sub_category=sub_category).order_by('discounted_price')
            elif sort_type == 'Price : High to Low':
                products = Products.objects.filter(
                    category=category, sub_category=sub_category).order_by('-discounted_price')
            else:
                products = Products.objects.filter(
                    category=category, sub_category=sub_category).order_by('title')
        elif(request.POST.get('range') != '' and request.POST.get('sort_type') == ''):
            filter_type = request.POST.get('filter_type')
            if filter_type == 'Brand':
                brand_name = request.POST.get('range')
                products = Products.objects.filter(
                    category=category, sub_category=sub_category, brand=brand_name).all()
            else:
                price_range = request.POST.get('range')
                min_price, max_price = price_range.split(" - ")
                min_price = int(min_price)
                max_price = int(max_price)
                products = Products.objects.filter(category=category, sub_category=sub_category,
                                                   discounted_price__lte=max_price, discounted_price__gte=min_price).all()
        else:
            products = Products.objects.all().order_by('title')
            filter_type = request.POST.get('filter_type')
            if filter_type == 'Brand':
                brand_name = request.POST.get('range')
                products = Products.objects.filter(
                    category=category, sub_category=sub_category, brand=brand_name).all()
            else:
                price_range = request.POST.get('range')
                min_price, max_price = price_range.split(" - ")
                min_price = int(min_price)
                max_price = int(max_price)
                products = Products.objects.filter(category=category, sub_category=sub_category,
                                                   discounted_price__lte=max_price, discounted_price__gte=min_price).all()

            sort_type = request.POST.get('sort_type')
            if sort_type == 'Product name : A to Z':
                products = products.order_by('title')
            elif sort_type == 'Product name : Z to A':
                products = products.order_by('-title')
            elif sort_type == 'Price : Low to High':
                products = products.order_by('discounted_price')
            elif sort_type == 'Price : High to Low':
                products = products.order_by('-discounted_price')
            else:
                products = products.order_by('title')

        product_dict = {}
        count = 0
        for product in products:
            product_dict[count] = {}
            product_dict[count]['id'] = 'productdetail\\'+str(product.id)
            product_dict[count]['title'] = product.title
            product_dict[count]['brand'] = product.brand
            product_dict[count]['market_price'] = product.market_price
            product_dict[count]['discounted_price'] = product.discounted_price
            product_dict[count]['discount'] = round((
                product.market_price - product.discounted_price)/product.market_price*100)
            product_dict[count]['image'] = "/"+str(product.image)
            sub_category = product.sub_category
            sizes_available = []
            if category == 'Men\'s' or category == 'Women\'s':
                if sub_category == 'Top-wear':
                    if product.size_1 == True:
                        sizes_available.append('S')
                    if product.size_2 == True:
                        sizes_available.append('M')
                    if product.size_3 == True:
                        sizes_available.append('L')
                    if product.size_4 == True:
                        sizes_available.append('XL')
                elif sub_category == 'Bottom-wear':
                    if product.size_1 == True:
                        sizes_available.append('28')
                    if product.size_2 == True:
                        sizes_available.append('30')
                    if product.size_3 == True:
                        sizes_available.append('32')
                    if product.size_4 == True:
                        sizes_available.append('34')
                    if product.size_5 == True:
                        sizes_available.append('36')
                else:
                    if product.size_1 == True:
                        sizes_available.append('UK-6')
                    if product.size_2 == True:
                        sizes_available.append('UK-7')
                    if product.size_3 == True:
                        sizes_available.append('UK-8')
                    if product.size_4 == True:
                        sizes_available.append('UK-9')
                    if product.size_5 == True:
                        sizes_available.append('UK-10')
                    if product.size_6 == True:
                        sizes_available.append('UK-11')
            else:
                if sub_category == 'Top-wear' or sub_category == 'Bottom-wear':
                    if product.size_1 == True:
                        sizes_available.append('1-2Y')
                    if product.size_2 == True:
                        sizes_available.append('2-3Y')
                    if product.size_3 == True:
                        sizes_available.append('3-4Y')
                    if product.size_4 == True:
                        sizes_available.append('4-5Y')
                    if product.size_5 == True:
                        sizes_available.append('5-6Y')
                    if product.size_6 == True:
                        sizes_available.append('6-7Y')
                    if product.size_7 == True:
                        sizes_available.append('7-8Y')
                    if product.size_8 == True:
                        sizes_available.append('8-9Y')
                    if product.size_9 == True:
                        sizes_available.append('9-10Y')
                    if product.size_10 == True:
                        sizes_available.append('10-11Y')
                    if product.size_11 == True:
                        sizes_available.append('11-12Y')
                else:
                    if product.size_1 == True:
                        sizes_available.append('1-1.5Y')
                    if product.size_2 == True:
                        sizes_available.append('1.5-2Y')
                    if product.size_3 == True:
                        sizes_available.append('2-2.5Y')
                    if product.size_4 == True:
                        sizes_available.append('2.5-3Y')
                    if product.size_5 == True:
                        sizes_available.append('3-3.5Y')
                    if product.size_6 == True:
                        sizes_available.append('3.5-4Y')
                    if product.size_7 == True:
                        sizes_available.append('4-4.5Y')
                    if product.size_8 == True:
                        sizes_available.append('4.5-5Y')
                    if product.size_9 == True:
                        sizes_available.append('5-6Y')
                    if product.size_10 == True:
                        sizes_available.append('6-7Y')
                    if product.size_11 == True:
                        sizes_available.append('7-8Y')
                    if product.size_12 == True:
                        sizes_available.append('8-9Y')
                    if product.size_13 == True:
                        sizes_available.append('9-10Y')
                    if product.size_14 == True:
                        sizes_available.append('10-11Y')
                    if product.size_15 == True:
                        sizes_available.append('11-12Y')
            product_dict[count]['sizes_available'] = ', '.join(sizes_available)
            count += 1
        return JsonResponse(product_dict)
    else:
        return redirect('/view_products')


def filter_load(request):
    filter = request.POST.get('filter')
    category = request.POST.get('category')
    sub_category = request.POST.get('sub_category')
    range_list = []
    if filter == 'Brand':
        products = Products.objects.filter(
            category=category, sub_category=sub_category).all()
        for product in products:
            brand = product.brand
            if brand not in range_list:
                range_list.append(brand)
        range_list = sorted(range_list)
    else:
        products = Products.objects.filter(
            category=category, sub_category=sub_category).all()
        max_price = -1
        for product in products:
            price = int(product.discounted_price)
            if max_price < price:
                max_price = price
        for i in range(0, max_price, 1000):
            range_list.append(str(i)+' - '+str(i+999))

    range_dict = {'ranges': range_list}
    return JsonResponse(range_dict)


def select_an_address_detailed(request, type, product_id, size):
    if request.user.is_authenticated == False or request.user.is_staff == True:
        return redirect('/')
    user_object = User.objects.filter(username=request.user).first()
    if user_object is None:
        return redirect('/')

    user_id = User.objects.filter(username=request.user).first().id
    customer_object = Customer_model.objects.filter(
        user=user_id).all()
    address_dict = {}
    count = 1
    for customer in customer_object:
        address_dict[count] = {}
        address_dict[count]['id'] = customer.id
        address_dict[count]['name'] = customer.name
        address_dict[count]['address1'] = customer.address1
        address_dict[count]['address2'] = customer.address2
        address_dict[count]['city'] = customer.city
        address_dict[count]['zip'] = customer.zip
        address_dict[count]['country'] = customer.country.country
        address_dict[count]['state'] = customer.state.state
        count += 1
    context = {'addresses': address_dict,
               'order_type': type, 'product_id': product_id, 'size': size}
    return render(request, 'select_an_address.html', context)


def select_an_address(request):
    if request.user.is_authenticated == False or request.user.is_staff == True:
        return redirect('/')
    if request.method == 'POST':
        type = request.POST.get('order_type')
        size = ''
        product_id = -1
        if type == 'direct':
            product_id = request.POST.get('product_id')
            size = request.POST.getlist('inlineRadioOptions')[0]
    else:
        return redirect('/')
    user_object = User.objects.filter(username=request.user).first()
    if user_object is None:
        return redirect('/')

    user_id = User.objects.filter(username=request.user).first().id
    customer_object = Customer_model.objects.filter(
        user=user_id).all()
    address_dict = {}
    count = 1
    for customer in customer_object:
        address_dict[count] = {}
        address_dict[count]['id'] = customer.id
        address_dict[count]['name'] = customer.name
        address_dict[count]['address1'] = customer.address1
        address_dict[count]['address2'] = customer.address2
        address_dict[count]['city'] = customer.city
        address_dict[count]['zip'] = customer.zip
        address_dict[count]['country'] = customer.country.country
        address_dict[count]['state'] = customer.state.state
        count += 1
    context = {'addresses': address_dict,
               'order_type': type, 'product_id': product_id, 'size': size}
    return render(request, 'select_an_address.html', context)


def placeorder(request, step):
    if request.user.is_authenticated == False or request.user.is_staff == True:
        return redirect('/')
    if step == 1:
        if request.method == 'POST':
            if 'select_an_address' in request.POST:
                type = request.POST.get('order_type')
                try:
                    address_id = request.POST.getlist('inlineRadioOptions')[0]
                except:
                    messages.info(request, 'Please select an Address')
                    order_type = request.POST.get('order_type')
                    if type == 'cart':
                        product_id = -1
                        size = 'not_applicable'
                    else:
                        product_id = request.POST.get('product_id')
                        size = request.POST.get('size')
                    return redirect('/select_an_address_detailed'+'/'+order_type+'/'+str(product_id)+'/'+size)
                user_id = Customer_model.objects.filter(
                    id=address_id).first().user_id
                if type == "cart":
                    cart_items = Cart_Items.objects.filter(
                        user_id=request.user).all()
                    cart_dict = {}
                    count = 0
                    total_sum = 0
                    for item in cart_items:
                        cart_dict[count] = {}
                        product = item.product_id
                        cart_dict[count]['title'] = product.title
                        cart_dict[count]['description'] = list(
                            product.description.split("\r\n"))
                        cart_dict[count]['image'] = "/"+str(product.image)
                        cart_dict[count]['price'] = product.discounted_price
                        cart_dict[count]['quantity'] = item.quantity
                        cart_dict[count]['size'] = item.size
                        cart_dict[count]['product_id'] = product.id
                        cart_dict[count]['total_price'] = item.quantity * \
                            product.discounted_price
                        total_sum += item.quantity * product.discounted_price
                        count += 1
                    context = {'cart': cart_dict, 'total_sum': total_sum,
                               'total_sum_with_delivery': total_sum+70,
                               'type': type, 'address_id': address_id}
                    return render(request, 'placeorder_1.html', context)
                else:
                    count = 0
                    product_id = request.POST.get('product_id')
                    size = request.POST.get('size')
                    product = Products.objects.filter(id=product_id).first()
                    cart_dict = {}
                    cart_dict[count] = {}
                    cart_dict[count]['title'] = product.title
                    cart_dict[count]['description'] = list(
                        product.description.split("\r\n"))
                    cart_dict[count]['image'] = "/"+str(product.image)
                    cart_dict[count]['price'] = product.discounted_price
                    print("Price", cart_dict[count]['price'])
                    cart_dict[count]['quantity'] = 1
                    cart_dict[count]['size'] = size
                    cart_dict[count]['product_id'] = product.id
                    cart_dict[count]['total_price'] = product.discounted_price
                    total_sum = product.discounted_price

                    context = {'cart': cart_dict, 'total_sum': total_sum,
                               'total_sum_with_delivery': total_sum+70,
                               'type': type, 'address_id': address_id, 'user_id': user_id,
                               'size': size, 'price': cart_dict[count]['price'],
                               'quantity': 1, 'product_id': product_id}
                    print("Type", context['type'])
                    print("Address ID", context['address_id'])
                    print("Seller User ID", user_id)
                    return render(request, 'placeorder_1.html', context)
            else:
                print("1")
                return redirect('/view_products/Men\'s/Top-wear')
        else:
            print("2")
            return redirect('/view_products/Women\'s/Top-wear')
    else:
        type = request.POST.get('type')
        if type == 'direct':
            product_id = request.POST.get('product_id')
            product = Products.objects.filter(id=product_id).first()
            size = request.POST.get('size')
            quantity = int(request.POST.get('quantity'))
            address_id = request.POST.get('address_id')
            address = Customer_model.objects.filter(id=address_id).first()
            type = request.POST.get('type')
            price = int(request.POST.get('price'))
            order_object = Orders(address_id=address, product_id=product, size=size, quantity=quantity,
                                  price=price, total_price=quantity*price, status='Order Placed')
            order_object.save()
            messages.info(request, "Order Placed Successfully")
            count = 0
            cart_dict = {}
            cart_dict[count] = {}
            cart_dict[count]['title'] = product.title
            cart_dict[count]['description'] = list(
                product.description.split("\r\n"))
            cart_dict[count]['image'] = "/"+str(product.image)
            cart_dict[count]['price'] = product.discounted_price
            print("Price", cart_dict[count]['price'])
            cart_dict[count]['quantity'] = 1
            cart_dict[count]['size'] = size
            cart_dict[count]['product_id'] = product.id
            cart_dict[count]['total_price'] = product.discounted_price
            total_sum = product.discounted_price
            context = {'cart': cart_dict, 'total_sum': total_sum,
                       'total_sum_with_delivery': total_sum+70}

            # Update Product Quantity & Product sold quantity
            category = product.category
            sub_category = product.sub_category
            mapped_size = size_mapping(category, sub_category, size)
            if mapped_size == 1:
                if(product.size_1_quantity > 0):
                    product.size_1_quantity = product.size_1_quantity - 1  # change field
                    product.size_1_quantity_sold = product.size_1_quantity_sold + 1
                    product.save()
            elif mapped_size == 2:
                if(product.size_2_quantity > 0):
                    product.size_2_quantity = product.size_2_quantity - 1  # change field
                    product.size_2_quantity_sold = product.size_2_quantity_sold + 1
                    product.save()
            elif mapped_size == 3:
                if(product.size_3_quantity > 0):
                    product.size_3_quantity = product.size_3_quantity - 1  # change field
                    product.size_3_quantity_sold = product.size_3_quantity_sold + 1
                    product.save()
            elif mapped_size == 4:
                if(product.size_4_quantity > 0):
                    product.size_4_quantity = product.size_4_quantity - 1  # change field
                    product.size_4_quantity_sold = product.size_4_quantity_sold + 1
                    product.save()
            elif mapped_size == 5:
                if(product.size_5_quantity > 0):
                    product.size_5_quantity = product.size_5_quantity - 1  # change field
                    product.size_5_quantity_sold = product.size_5_quantity_sold + 1
                    product.save()
            elif mapped_size == 6:
                if(product.size_6_quantity > 0):
                    product.size_6_quantity = product.size_6_quantity - 1  # change field
                    product.size_6_quantity_sold = product.size_6_quantity_sold + 1
                    product.save()
            elif mapped_size == 7:
                if(product.size_7_quantity > 0):
                    product.size_7_quantity = product.size_7_quantity - 1  # change field
                    product.size_7_quantity_sold = product.size_7_quantity_sold + 1
                    product.save()
            elif mapped_size == 8:
                if(product.size_8_quantity > 0):
                    product.size_8_quantity = product.size_8_quantity - 1  # change field
                    product.size_8_quantity_sold = product.size_8_quantity_sold + 1
                    product.save()
            elif mapped_size == 9:
                if(product.size_9_quantity > 0):
                    product.size_9_quantity = product.size_9_quantity - 1  # change field
                    product.size_9_quantity_sold = product.size_9_quantity_sold + 1
                    product.save()
            elif mapped_size == 10:
                if(product.size_10_quantity > 0):
                    product.size_10_quantity = product.size_10_quantity - 1  # change field
                    product.size_10_quantity_sold = product.size_10_quantity_sold + 1
                    product.save()
            elif mapped_size == 11:
                if(product.size_11_quantity > 0):
                    product.size_11_quantity = product.size_11_quantity - 1  # change field
                    product.size_11_quantity_sold = product.size_11_quantity_sold + 1
                    product.save()
            elif mapped_size == 12:
                if(product.size_12_quantity > 0):
                    product.size_12_quantity = product.size_12_quantity - 1  # change field
                    product.size_12_quantity_sold = product.size_12_quantity_sold + 1
                    product.save()
            elif mapped_size == 13:
                if(product.size_13_quantity > 0):
                    product.size_13_quantity = product.size_13_quantity - 1  # change field
                    product.size_13_quantity_sold = product.size_13_quantity_sold + 1
                    product.save()
            elif mapped_size == 14:
                if(product.size_14_quantity > 0):
                    product.size_14_quantity = product.size_14_quantity - 1  # change field
                    product.size_14_quantity_sold = product.size_14_quantity_sold + 1
                    product.save()
            elif mapped_size == 15:
                if(product.size_15_quantity > 0):
                    product.size_15_quantity = product.size_15_quantity - 1  # change field
                    product.size_15_quantity_sold = product.size_15_quantity_sold + 1
                    product.save()
            product.total_quantity_sold = product.total_quantity_sold + 1
            return render(request, 'placeorder_2.html', context)
        else:
            # cart
            address_id = request.POST.get('address_id')
            address = Customer_model.objects.filter(id=address_id).first()
            user_id = User.objects.filter(username=request.user).first()
            cart_items = Cart_Items.objects.filter(user_id=user_id).all()
            count = 0
            total_sum = 0
            cart_dict = {}
            for cart_item in cart_items:
                product = cart_item.product_id
                size = cart_item.size
                quantity = int(cart_item.quantity)
                price = int(product.discounted_price)

                # Update Product Quantity & Product sold quantity
                category = product.category
                sub_category = product.sub_category
                mapped_size = size_mapping(category, sub_category, size)
                if mapped_size == 1:
                    if(product.size_1_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+str(size)+' size'+';'+str(product.id))
                        return redirect('/addtocart')
                elif mapped_size == 2:
                    if(product.size_2_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_3_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 3:
                    if(product.size_3_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_3_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+str(product.id))
                        return redirect('/addtocart')
                elif mapped_size == 4:
                    if(product.size_4_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_4_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 5:
                    if(product.size_5_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_5_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 6:
                    if(product.size_6_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_6_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 7:
                    if(product.size_7_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_7_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 8:
                    if(product.size_8_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_8_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 9:
                    if(product.size_9_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_9_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 10:
                    if(product.size_10_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_10_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 11:
                    if(product.size_11_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_11_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 12:
                    if(product.size_12_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_12_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 13:
                    if(product.size_13_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_13_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 14:
                    if(product.size_14_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_14_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 15:
                    if(product.size_15_quantity >= quantity):
                        continue
                    else:
                        messages.error(request, 'Only '+str(product.size_15_quantity) +
                                       ' items are available in stock for '+size+' size'+';'+product.id)
                        return redirect('/addtocart')
                product.total_quantity_sold = product.total_quantity_sold + quantity

                # product = Products.objects.filter(id=product_id).first()

            for cart_item in cart_items:
                product = cart_item.product_id
                size = cart_item.size
                quantity = int(cart_item.quantity)
                price = int(product.discounted_price)

                # Update Product Quantity & Product sold quantity
                category = product.category
                sub_category = product.sub_category
                mapped_size = size_mapping(category, sub_category, size)
                if mapped_size == 1:
                    if(product.size_1_quantity >= quantity):
                        product.size_1_quantity = product.size_1_quantity - quantity  # change field
                        product.size_1_quantity_sold = product.size_1_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+str(size)+' size'+';'+str(product.id))
                        return redirect('/addtocart')
                elif mapped_size == 2:
                    if(product.size_2_quantity >= quantity):
                        product.size_2_quantity = product.size_2_quantity - quantity  # change field
                        product.size_2_quantity_sold = product.size_2_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 3:
                    if(product.size_3_quantity >= quantity):
                        product.size_3_quantity = product.size_3_quantity - quantity  # change field
                        product.size_3_quantity_sold = product.size_3_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 4:
                    if(product.size_4_quantity >= quantity):
                        product.size_4_quantity = product.size_4_quantity - quantity  # change field
                        product.size_4_quantity_sold = product.size_4_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 5:
                    if(product.size_5_quantity >= quantity):
                        product.size_5_quantity = product.size_5_quantity - quantity  # change field
                        product.size_5_quantity_sold = product.size_5_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 6:
                    if(product.size_6_quantity >= quantity):
                        product.size_6_quantity = product.size_6_quantity - quantity  # change field
                        product.size_6_quantity_sold = product.size_6_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 7:
                    if(product.size_7_quantity >= quantity):
                        product.size_7_quantity = product.size_7_quantity - quantity  # change field
                        product.size_7_quantity_sold = product.size_7_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 8:
                    if(product.size_8_quantity >= quantity):
                        product.size_8_quantity = product.size_8_quantity - quantity  # change field
                        product.size_8_quantity_sold = product.size_8_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 9:
                    if(product.size_9_quantity >= quantity):
                        product.size_9_quantity = product.size_9_quantity - quantity  # change field
                        product.size_9_quantity_sold = product.size_9_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 10:
                    if(product.size_10_quantity >= quantity):
                        product.size_10_quantity = product.size_10_quantity - quantity  # change field
                        product.size_10_quantity_sold = product.size_10_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 11:
                    if(product.size_11_quantity >= quantity):
                        product.size_11_quantity = product.size_11_quantity - quantity  # change field
                        product.size_11_quantity_sold = product.size_11_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 12:
                    if(product.size_12_quantity >= quantity):
                        product.size_12_quantity = product.size_12_quantity - quantity  # change field
                        product.size_12_quantity_sold = product.size_12_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 13:
                    if(product.size_13_quantity >= quantity):
                        product.size_13_quantity = product.size_13_quantity - quantity  # change field
                        product.size_13_quantity_sold = product.size_13_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 14:
                    if(product.size_14_quantity >= quantity):
                        product.size_14_quantity = product.size_14_quantity - quantity  # change field
                        product.size_14_quantity_sold = product.size_14_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                elif mapped_size == 15:
                    if(product.size_15_quantity >= quantity):
                        product.size_15_quantity = product.size_15_quantity - quantity  # change field
                        product.size_15_quantity_sold = product.size_15_quantity_sold + quantity
                    else:
                        messages.error(request, 'Only '+str(product.size_1_quantity) +
                                       ' items are available in stock for '+size+' size'+'-'+product.id)
                        return redirect('/addtocart')
                product.total_quantity_sold = product.total_quantity_sold + quantity
                product.save()

                # product = Products.objects.filter(id=product_id).first()

                order_object = Orders(address_id=address, product_id=product, size=size, quantity=quantity,
                                      price=price, total_price=quantity*price, status='Order Placed')
                order_object.save()

                cart_dict[count] = {}
                cart_dict[count]['title'] = product.title
                cart_dict[count]['description'] = list(
                    product.description.split("\r\n"))
                cart_dict[count]['image'] = "/"+str(product.image)
                cart_dict[count]['price'] = product.discounted_price
                print("Price", cart_dict[count]['price'])
                cart_dict[count]['quantity'] = quantity
                cart_dict[count]['size'] = size
                cart_dict[count]['product_id'] = product.id
                cart_dict[count]['total_price'] = quantity * \
                    product.discounted_price
                total_sum += cart_dict[count]['total_price']
                count += 1
            messages.info(request, "Order Placed Successfully")
            context = {'cart': cart_dict, 'total_sum': total_sum,
                       'total_sum_with_delivery': total_sum+70}
            return render(request, 'placeorder_2.html', context)


def size_mapping(category_, sub_category_, size_):
    print(category_)
    print(sub_category_)
    print(size_)
    size_mapping_dict = {}
    category_list = ['Men\'s', 'Women\'s', 'Kid\'s']
    sub_category_list = ['Top-wear', 'Bottom-wear', 'Foot-wear']
    for category in category_list:
        size_mapping_dict[category] = {}
        for sub_category in sub_category_list:
            size_mapping_dict[category][sub_category] = {}
    for category in category_list:
        for sub_category in sub_category_list:
            if category == 'Men\'s' or category == 'Women\'s':
                if sub_category == 'Top-wear':
                    size_mapping_dict[category][sub_category]['S'] = 1
                    size_mapping_dict[category][sub_category]['M'] = 2
                    size_mapping_dict[category][sub_category]['L'] = 3
                    size_mapping_dict[category][sub_category]['XL'] = 4
                elif sub_category == 'Bottom-wear':
                    size_mapping_dict[category][sub_category]['28'] = 1
                    size_mapping_dict[category][sub_category]['30'] = 2
                    size_mapping_dict[category][sub_category]['32'] = 3
                    size_mapping_dict[category][sub_category]['34'] = 4
                    size_mapping_dict[category][sub_category]['36'] = 5
                else:
                    size_mapping_dict[category][sub_category]['UK-6'] = 1
                    size_mapping_dict[category][sub_category]['UK-7'] = 2
                    size_mapping_dict[category][sub_category]['UK-8'] = 3
                    size_mapping_dict[category][sub_category]['UK-9'] = 4
                    size_mapping_dict[category][sub_category]['UK-10'] = 5
                    size_mapping_dict[category][sub_category]['UK-11'] = 6
            else:
                if sub_category == 'Top-wear' or sub_category == 'Bottom-wear':
                    size_mapping_dict[category][sub_category]['1-2Y'] = 1
                    size_mapping_dict[category][sub_category]['2-3Y'] = 2
                    size_mapping_dict[category][sub_category]['3-4Y'] = 3
                    size_mapping_dict[category][sub_category]['4-5Y'] = 4
                    size_mapping_dict[category][sub_category]['5-6Y'] = 5
                    size_mapping_dict[category][sub_category]['6-7Y'] = 6
                    size_mapping_dict[category][sub_category]['7-8Y'] = 7
                    size_mapping_dict[category][sub_category]['8-9Y'] = 8
                    size_mapping_dict[category][sub_category]['9-10Y'] = 9
                    size_mapping_dict[category][sub_category]['10-11Y'] = 10
                    size_mapping_dict[category][sub_category]['11-12Y'] = 11
                else:
                    size_mapping_dict[category][sub_category]['1-1.5Y'] = 1
                    size_mapping_dict[category][sub_category]['1.5-2Y'] = 2
                    size_mapping_dict[category][sub_category]['2-2.5Y'] = 3
                    size_mapping_dict[category][sub_category]['2.5-3Y'] = 4
                    size_mapping_dict[category][sub_category]['3-3.5Y'] = 5
                    size_mapping_dict[category][sub_category]['3.5-4Y'] = 6
                    size_mapping_dict[category][sub_category]['4-4.5Y'] = 7
                    size_mapping_dict[category][sub_category]['4.5-5Y'] = 8
                    size_mapping_dict[category][sub_category]['5-6Y'] = 9
                    size_mapping_dict[category][sub_category]['6-7Y'] = 10
                    size_mapping_dict[category][sub_category]['7-8Y'] = 11
                    size_mapping_dict[category][sub_category]['8-9Y'] = 12
                    size_mapping_dict[category][sub_category]['9-10Y'] = 13
                    size_mapping_dict[category][sub_category]['10-11Y'] = 14
                    size_mapping_dict[category][sub_category]['11-12Y'] = 15
            print(category, sub_category)
            for key, value in size_mapping_dict.items():
                for key1, value1 in value.items():
                    print(key, key1, value1)
            print("\n")
    return size_mapping_dict[category_][sub_category_][size_]


def myorders(request):
    if request.user.is_authenticated == False or request.user.is_staff == True:
        return redirect('/')
    user_object = User.objects.filter(username=request.user).first()
    addresses = Customer_model.objects.filter(user=user_object).all()
    cart_dict = {}
    count = 0
    for address in addresses:
        orders = Orders.objects.filter(address_id=address).all()
        for order in orders:
            product = order.product_id
            cart_dict[count] = {}
            cart_dict[count]['title'] = product.title
            cart_dict[count]['description'] = list(
                product.description.split("\r\n"))
            cart_dict[count]['image'] = "/"+str(product.image)
            cart_dict[count]['price'] = product.discounted_price
            cart_dict[count]['quantity'] = order.quantity
            cart_dict[count]['size'] = order.size
            cart_dict[count]['product_id'] = product.id
            cart_dict[count]['total_price'] = order.quantity * \
                product.discounted_price
            cart_dict[count]['timestamp'] = order.timestamp
            cart_dict[count]['status'] = order.status
            count += 1
    context = {'cart': cart_dict}
    return render(request, 'myorders.html', context)


def get_cart_items(request):
    user_object = User.objects.filter(username=request.user).first()
    cart_objects = Cart_Items.objects.filter(user_id=user_object).all()
    cart_items_dict = {'cart_items': len(cart_objects)}
    return JsonResponse(cart_items_dict)
