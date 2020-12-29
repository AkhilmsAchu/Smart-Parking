from django.shortcuts import render
from property_vendor.models import property,pslot,userProfile

# Create your views here.
def index(request):
	return render(request,'public/index.html')

def search(request):
	results=property.objects.all()
	return render(request,'public/search.html',{'results':results})
