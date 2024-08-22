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


def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def ice_creams(request):
    return render(request, "ice_creams.html")

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