from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView): 
    template_name = 'pages/about.html' 
 
     
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: Moises Arturo Vergara Garces", 
        }) 
 
        return context
 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.objects.all() 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError()
        except ValueError:
            return HttpResponseRedirect(reverse('home'))

        product = get_object_or_404(Product, pk=product_id)
        comments = product.comments.all()

        viewData = {}
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
        viewData["comments"] = comments

        return render(request, self.template_name, viewData)

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Price must be greater than zero')
        return price
 
class ProductCreateView(View): 
    template_name = 'products/create.html' 
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'