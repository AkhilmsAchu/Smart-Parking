from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from datetime import datetime 

# Create your models here.
class property(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	mapurl = models.CharField(max_length=500,default='')
	img1 = ResizedImageField(size=[500, 500],crop=['middle', 'center'],upload_to='property/pics',null=False)
	img2 = ResizedImageField(size=[500, 500],crop=['middle', 'center'],upload_to='property/pics', null=False)
	img3 = ResizedImageField(size=[500, 500],crop=['middle', 'center'],upload_to='property/pics', null=False)
	isactive = models.BooleanField(default=True)
	upi = models.CharField(max_length=30,null=True,blank=True,default = None)
	place = models.CharField(max_length=200,default='')
	district = models.CharField(max_length=200,default='')
	created_at = models.DateField(auto_now_add=True)
	owner = models.ForeignKey(User,default=None,on_delete=models.CASCADE)#for now to pass form validation,will remove later

	def __str__(self):
		return self.name

class pslot(models.Model):
	propertyid = models.ForeignKey(property,default=None,on_delete=models.CASCADE)
	isfw = models.BooleanField(default=False)
	istw = models.BooleanField(default=False)
	isavailable = models.BooleanField(default=True)
	isroofed = models.BooleanField(default=True)
	isfenced = models.BooleanField(default=True)
	rate = models.IntegerField(default=2)

	def __str__(self):
		return self.propertyid.name+str(self.id)

class userProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	state = models.CharField(max_length=200,default='')
	house = models.CharField(max_length=200,default='')
	town = models.CharField(max_length=200,default='')
	pincode = models.CharField(max_length=12,default='')
	phone = models.CharField(max_length=12,default='')
	isvendor = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username


class bookingDetails(models.Model):
	userid = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	pslotid = models.ForeignKey(pslot,default=None,on_delete=models.CASCADE)
	bdate = models.DateTimeField(auto_now_add=True)
	cdate = models.DateTimeField(default=datetime.now, blank=True)
	vtype = models.IntegerField(default=2)
	regnum = models.CharField(max_length=12,default='')
	amt = models.IntegerField(default=0)
	status = models.BooleanField(default=True)

class reportDetails(models.Model):
	userid = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	reportedby  = models.ForeignKey(User,default=None,on_delete=models.CASCADE,related_name='+')
	rdate = models.DateTimeField(default=datetime.now, blank=True)
	status = models.BooleanField(default=True)

def mark_pslot_unavailable(pid):
	slot=pslot.objects.get(id=pid)
	book=bookingDetails.objects.get(pslotid=slot,status=True)
	if book:
		slot.isavailable=False
		slot.save()
		print("marked unavailable")

def mark_pslot_available(pid):
	slot=pslot.objects.get(id=pid)
	book=bookingDetails.objects.get(pslotid=slot,status=True)
	if book:
		slot.isavailable=True
		slot.save()
		print("marked available")

class reviewDetails(models.Model):
	userid = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	propertyid = models.ForeignKey(property,default=None,on_delete=models.CASCADE)
	review = models.CharField(max_length=200,default='')
		
'''		
def check_product_stock(pid):
	product=products.objects.get(id=pid)
	if product.stock==0:
		product.isactive=False
		product.save()
		print("marked inactive")

class wishlist(models.Model):
	userid = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	productid = models.ForeignKey(products,default=None,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

class orderDetails(models.Model):
	userid = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	productid = models.ForeignKey(products,default=None,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	date = models.DateTimeField(auto_now_add=True)
	address = models.TextField()
	status = models.BooleanField(default=False)
	paymode = models.CharField(max_length=20,default=None)

class reviewDetails(models.Model):
	userid = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	productid = models.ForeignKey(products,default=None,on_delete=models.CASCADE)
	stars = models.IntegerField(default=1)
	review = models.CharField(max_length=200,default='')	

'''