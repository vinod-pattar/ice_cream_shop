from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect
from django.http import Http404
from django.http import FileResponse
from django.http import StreamingHttpResponse
from django.http import HttpResponseForbidden
import os
from django.conf import settings
from django.template import loader
from django.urls import reverse
from .models import Product, CartItem, Order, OrderItem
from .forms import EnquiryForm, AddressForm
from django.contrib import messages

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from pyairtable import Api
import requests
from django.contrib.auth.decorators import login_required
from authentication.models import Address
import uuid
import razorpay
import secrets
import string

# Create your views here.
def home(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your enquiry has been submitted successfully!')
            return redirect('home')
    else: 
        products = Product.objects.all() 
        form = EnquiryForm()
    return render(request, "home.html", {"products": products, 'enquiry': form})

def ice_creams(request):
    products = Product.objects.all()

    # Pagination settings
    paginator = Paginator(products, 6)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "ice_creams.html", {'page_obj': page_obj})


def ice_cream_detail(request, ice_cream_id):
    ice_cream = Product.objects.get(id=ice_cream_id)
    return render(request, "ice_cream_detail.html", {'ice_cream': ice_cream})

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        # Add code to store form data to the store 

        
        # api = Api(os.environ['AIRTABLE_API_KEY'])
        # table = api.table('appdocnsZazAsunAA', 'tblGXz4VVlflM0VdG')
        # table.create({'Name': request.POST.get('name'), 'Email': request.POST.get('email'), 'Message': request.POST.get('message')})
        url = "https://api.airtable.com/v0/appdocnsZazAsunAA/Table%201"
        data = {
            "records": [
                {
                    "fields": {
                        "Name": request.POST.get('name'),
                        "Email": request.POST.get('email'),
                        "Message": request.POST.get('message')
                    }
                }
            ]
        }
        headers = {
            "Authorization": f"Bearer {os.environ['AIRTABLE_API_KEY']}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            messages.success(request, 'Your message has been submitted successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Something went wrong. Please try again later.')
            return redirect('contact')
        
    return render(request, "contact.html")

def confirm_enquiry_email(instance):
    subject = 'Your Product Enquiry Confirmation'
    from_email = 'vinod@example.com'
    to = instance.email

    # Render the HTML email template
    html_content = render_to_string('emails/confirm_enquiry.html', {
        'enquiry': instance,
    })
    text_content = strip_tags(html_content)  # Fallback to plain text content

    # Create the email
    email = EmailMultiAlternatives(subject, text_content, from_email, [to])
    email.attach_alternative(html_content, "text/html")

    # Send the email
    email.send()


@login_required(login_url='login')
def add_to_cart(request, ice_cream_id):
    product = Product.objects.get(id=ice_cream_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    
    cart_item.price = product.price

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()
        
    return redirect('cart')

@login_required(login_url="login")
def update_cart(request):
    if request.method == 'POST':
        # Handle removing an item
        if 'remove' in request.POST:
            item_id = request.POST['remove']
            # Logic to remove item from cart
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            cart_item.delete()

        else:
             # Handle updating quantities
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    item_id = key.split('_')[1]
                    new_quantity = int(value)
                    # Logic to update the quantity of the item in the cart
                    cart_item = CartItem.objects.get(id=item_id, user=request.user)
                    cart_item.quantity = new_quantity
                    cart_item.save()

    return redirect('cart')

@login_required(login_url='login') 
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    grand_total = sum(item.price * item.quantity for item in cart_items)
    return render(request, "cart.html", {'cart_items': cart_items, 'grand_total': grand_total})

def generate_unique_string(length=8):
    # Define the characters to use (you can customize this)
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    # Generate a random string of the specified length
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

@login_required(login_url='login')
def checkout(request):
    if request.method == "POST":
        action = request.POST.get('action')
        address_id = request.POST.get('address')
        address = Address.objects.get(id=address_id, user=request.user)

        cart_items = CartItem.objects.filter(user=request.user)
        grand_total = sum(item.price * item.quantity for item in cart_items)

        order = Order.objects.create(
                user=request.user,
                total=grand_total,
                status='pending',
                address=address, 
                currency='INR',
                receipt='receipt_' + generate_unique_string(),
                payment_status="Pending",
                amount_paid=0.0,
                amount_due=grand_total)
            
        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            ) for item in cart_items
        ])

        cart_items.delete()

        if action == "cod":
            # Handle Cash on Delivery
            return redirect('order_details', order_id=order.id)

        elif action == "pay_online":
            # Handle Online Payment
            # Create razorpay order
            client = razorpay.Client(auth=(os.environ['RAZORPAY_KEY'], os.environ['RAZORPAY_SECRET']))
            razorpay_order = client.order.create({
                "amount": grand_total * 100,
                "currency":'INR',
                "receipt": order.receipt,
                "partial_payment": False,
                "notes" : {
                    "order_id": order.id,
                    "user_id": request.user.id
                    }
                })
            
            # Transaction.objects.create(
            #     user=request.user,
            #     order=order,
            #     transaction_id=razorpay_order['id'],
            #     amount=grand_total,
            #     currency='INR',
            #     status='Pending'
            #     )
            order.razorpay_order_id = razorpay_order['id']
            order.save()


            return redirect('payment', order_id=order.id)
        else:
            return HttpResponse("Invalid action")
        
    addresses = Address.objects.filter(user=request.user).order_by('-id')
    return render(request, "checkout.html", {'addresses': addresses})

@login_required(login_url='login')
def payment(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user,)
    if order.payment_status == "Paid" or order.status == "Canceled":
        return redirect('order_details', order_id=order.id)
    return render(request, "payment.html", {'order': order})

@login_required(login_url='login')
def verify_payment(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        order = Order.objects.get(id=order_id, user=request.user)
        client = razorpay.Client(auth=(os.environ['RAZORPAY_KEY'], os.environ['RAZORPAY_SECRET']))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order.razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            order.payment_status = 'Paid'
            order.amount_paid = order.total
            order.amount_due = 0.0
            order.save()
            return redirect('order_details', order_id=order.id)
        except Exception as e:
            order.payment_status = 'Failed'
            order.save()
            return HttpResponse("Payment Failed")
    else:
        return HttpResponse("Invalid Request")


@login_required(login_url="login")
def order_details(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, "order_details.html", {'order': order, 'order_items': order_items})

@login_required(login_url="login")
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order.status = 'canceled'
    order.payment_status = 'canceled'
    order.save()
    return redirect('orders_list')

@login_required(login_url='login')
def orders_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "orders_list.html", {'page_obj': page_obj})

@login_required(login_url='login')
def addresses(request):
    addresses = Address.objects.filter(user=request.user).order_by('-id')
    return render(request, "addresses.html", {'addresses': addresses})

@login_required(login_url='login')
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)  # Pass the user_id to the form
        print(form.errors)
        print(form.is_valid())
        print(form.cleaned_data)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('checkout')
        else:
            print(form.errors)
            
    else:
        form = AddressForm(initial={'user': request.user})
    return render(request, "add_address.html", {'form': form} )

@login_required(login_url='login')
def edit_address(request, address_id):
    address = Address.objects.get(id=address_id, user=request.user)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('checkout')
    else:
        form = AddressForm(instance=address)
    return render(request, "edit_address.html", {'form': form})


@login_required(login_url='login')
def delete_address(request, address_id):
    address = Address.objects.get(id=address_id, user=request.user)
    address.delete()
    return redirect('checkout')


# def file_iterator(file_name, chunk_size=8192):
#     with open(file_name, 'rb') as f:
#         while True:
#             c = f.read(chunk_size)
#             if c:
#                 yield c
#             else:
#                 break


def api_home(request, id):
    # return JsonResponse({"message": "Hello, World!"})
    # return HttpResponseRedirect("/")
    # return HttpResponsePermanentRedirect("/")
    # raise Http404("Page not found")
    # file_path = os.path.join(settings.MEDIA_ROOT, 'products/images/th.jpeg')
    # if os.path.exists(file_path):
    #     return FileResponse(open(file_path, "rb"), filename="th.jpeg", content_type="image/jpeg", as_attachment=True)
    # else:
    #     raise Http404("File not found")
    # file_path = os.path.join(settings.MEDIA_ROOT, 'products/images/th.jpeg')
    # if os.path.exists(file_path):
    #     response = StreamingHttpResponse(file_iterator(file_path))
    #     response['Content-Type'] = 'image/jpeg'
    #     response['Content-Disposition'] = f'attachment; filename="th.jpeg"'
    #     return response
    # else:
    #     raise Http404("File not found")
    # return HttpResponseForbidden("You are not allowed to access this page")
    # template = loader.get_template('home.html')
    # return HttpResponse(template.render({"name": "ABC"}, request))
    # return HttpResponseRedirect(reverse("about"))

    return HttpResponse(f"API Home Page: {id}")

def api_home2(request, id):
    return HttpResponse(f"API Home Page 2: {id}")


def page_not_found(request, exception):
    return HttpResponse("404 Page Not Found")

def server_error(request):
    return HttpResponse("500 Internal Server Error")