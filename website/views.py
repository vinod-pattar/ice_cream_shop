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
from .models import Product
from .forms import EnquiryForm
from django.contrib import messages

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from pyairtable import Api
import requests
from django.contrib.auth.decorators import login_required

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