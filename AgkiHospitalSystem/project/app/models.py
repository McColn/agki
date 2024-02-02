from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.contrib.auth import get_user_model
import random
import string
import geoip2.database
from django.utils import timezone
from django.urls import reverse
from twilio.rest import Client


class Department(models.Model):
    name = models.CharField(max_length=20)
    descrption = models.CharField(max_length=20)


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, null=True,blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True,blank=True)
    reg_no = models.CharField(max_length=10, unique=True)
    age = models.IntegerField(null=True)
    position = models.CharField(max_length=40, null=True,blank=True)
    district = models.CharField(max_length=40, null=True,blank=True)
    ward = models.CharField(max_length=40, null=True,blank=True)
    street = models.CharField(max_length=40, null=True,blank=True)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
    is_doctor = models.BooleanField(default=False)
    is_laboratorist = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)
    is_pharmacist = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    sms_sent_payment = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generate unique registration number if not already set
        if not self.reg_no:
            initials = ''.join(word[0] for word in self.first_name.split()) + ''.join(word[0] for word in self.last_name.split())
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            self.reg_no = initials.upper() + random_string

        # Send SMS only if registration number is set and hasn't been sent before
        if self.reg_no and not self.sms_sent:
            url = "https://messaging-service.co.tz/api/sms/v1/text/single"
            payload = {
                "from": "RMNDR",
                "to": self.phone,  # Assuming the phone number is stored in 'phone' field
                "text": f"Dear {self.username}, you registered successfully to Agki Dispensary. Your registration number is {self.reg_no}",
                "reference": "aswqetgcv"
            }
            headers = {
                'Authorization': 'Basic QWdraWxhYjpLaW13ZXJpJjIwMjI=',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response = requests.post(url, headers=headers, data=json.dumps(payload))

            # Check if the request was successful (status code 2xx)
            if response.ok:
                print("SMS sent successfully")
            else:
                print(f"Failed to send SMS. Status code: {response.status_code}, Response: {response.text}")

            # Set sms_sent to True to avoid sending the SMS multiple times
            self.sms_sent = True

        # Check if payment_status changed to True
        if self.payment_status and not self.sms_sent_payment:
            url = "https://messaging-service.co.tz/api/sms/v1/text/single"
            payload_payment = {
                "from": "RMNDR",
                "to": self.phone,  # Assuming the phone number is stored in 'phone' field
                "text": "Your payment has been processed. You can now start chatting on our website. http://127.0.0.1:8000/create-thread",
                "reference": "aswqetgcv"
            }
            headers_payment = {
                'Authorization': 'Basic QWdraWxhYjpLaW13ZXJpJjIwMjI=',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response_payment = requests.post(url, headers=headers_payment, data=json.dumps(payload_payment))

            # Check if the request was successful (status code 2xx)
            if response_payment.ok:
                print("Payment SMS sent successfully")
            else:
                print(f"Failed to send payment SMS. Status code: {response_payment.status_code}, Response: {response_payment.text}")

            # Set sms_sent_payment to True to avoid sending the SMS multiple times
            self.sms_sent_payment = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username



class HospitalRegistrationModel(models.Model):
    name = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    location = models.CharField(max_length=20,null=True,blank=True)
    region = models.CharField(max_length=20,null=True,blank=True)
    district = models.CharField(max_length=20,null=True,blank=True)
    ward = models.CharField(max_length=20,null=True,blank=True)
    street = models.CharField(max_length=20,null=True,blank=True)
    service = models.CharField(max_length=20,null=True,blank=True)
    registerd_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.name


class SickInfoModel(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    mtaa = models.CharField(max_length=15)
    kata = models.CharField(max_length=30)
    wilaya = models.CharField(max_length=30)
    maelezo = models.TextField(max_length=1000)
    mda = models.DateTimeField(auto_now_add=True)
    service = models.CharField(max_length=20,null=True,blank=True)
    hospital = models.ForeignKey(HospitalRegistrationModel, on_delete=models.CASCADE,null=True,blank=True)
    hospital_assigned = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username


class ContactModel(models.Model):
    jina = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    ujumbe = models.CharField(max_length=200)

    def __str__(self):
        return self.jina


class Medicine(models.Model):
    medicineName = models.CharField(max_length=20)
    amount = models.IntegerField()
    remainAmount = models.IntegerField()
    unitCost = models.FloatField()
    
    receivedDate = models.DateTimeField(auto_now_add=True)
    expireDate= models.DateField()

    @property
    def totalCost(self):
        # Calculate and return total cost dynamically
        return round(self.amount * self.unitCost, 2)
    
    def save(self, *args, **kwargs):
        # Set a default value for remainAmount if not provided
        if self.remainAmount is None:
            self.remainAmount = self.amount

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.medicineName


class Patient(models.Model):
    fullname = models.CharField(max_length=30)
    age = models.IntegerField()
    address = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    height = models.IntegerField(null=True,blank=True)
    pressure = models.CharField(max_length=10,null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    dalili = models.TextField(max_length=500,null=True,blank=True)
    possibleDiseases = models.TextField(max_length=500,null=True,blank=True)
    testConducted = models.TextField(max_length=500,null=True,blank=True)
    labResults = models.TextField(max_length=500,null=True,blank=True)
    actualDiseases = models.TextField(max_length=500,null=True,blank=True)
    otherRecomendation = models.TextField(max_length=500,null=True,blank=True)
    
    def __str__(self):
        return self.fullname


class Prescription(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(null=True,blank=True)
    dosage = models.CharField(max_length=100,null=True,blank=True)
    cost = models.FloatField(null=True,blank=True)
    totalCost = models.FloatField(null=True, blank=True) 
    medicineStatus = models.BooleanField(default=False)
    prescription_date = models.DateField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    @property
    def day_of_week(self):
        # Assuming prescription_date is an attribute of type datetime.datetime
        return self.prescription_date.strftime('%A')

    def __str__(self):
        return f"Prescription for {self.medicine.medicineName} to {self.patient.fullname}"

    def save(self, *args, **kwargs):
        # Set the cost to the unitCost of the selected medicine
        self.cost = self.medicine.unitCost if self.medicine else None

        # Ensure that self.amount is a numeric value before attempting multiplication
        try:
            if self.amount:
                self.amount = int(self.amount)  # Try converting to integer
        except (ValueError, TypeError):
            self.amount = None

        # Calculate the total cost based on cost and amount
        self.totalCost = round(self.cost * self.amount, 2) if self.cost and self.amount else None

        # Decrease remainAmount of associated Medicine
        if self.amount and self.medicine.remainAmount >= self.amount:
            self.medicine.remainAmount -= self.amount
            self.medicine.save()
            
        super().save(*args, **kwargs)



# for index as a home page
class Faqs(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=1000)
    
    def __self__(self):
        return self.question
    
class News(models.Model):
    header = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
    
    def __self__(self):
        return self.header

class Portfolio(models.Model):
    image1 = models.ImageField(upload_to ='media/',blank=True,null=True)
    image2 = models.ImageField(upload_to ='media/',blank=True,null=True)
    image3 = models.ImageField(upload_to ='media/',blank=True,null=True)
    image4 = models.ImageField(upload_to ='media/',blank=True,null=True)
    image5 = models.ImageField(upload_to ='media/',blank=True,null=True)
    image6 = models.ImageField(upload_to ='media/',blank=True,null=True)
    
class IntroVideo(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    def __str__(self):
        return self.title

class Review(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
    body = models.CharField(max_length=500)
    time_posted = models.CharField(max_length=50)
    views = models.CharField(max_length=5,blank=True,null=True)
    likes = models.CharField(max_length=5,blank=True,null=True)
    comments = models.CharField(max_length=5,blank=True,null=True)
    share = models.CharField(max_length=5,blank=True,null=True)
    link = models.CharField(max_length=500,blank=True,null=True)
    
    def __self__(self):
        return self.name
    
class Service(models.Model):
    header = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    
    def __self__(self):
        return self.header
    
class FrontPage(models.Model):
    header = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
    
    def __self__(self):
        return self.header
    
class WhyUseAgki(models.Model):
    header = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
    
    def __self__(self):
        return self.header




# ////////////////////////////////////////////chat with doctor////////////////////////
class ThreadModel(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='+')
	receiver = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='+')

class MessageModel(models.Model):
	thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE,blank=True,null=True)
	sender_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='+')
	receiver_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='+')
	body = models.CharField(max_length=1000,blank=True,null=True)
	image = models.ImageField(blank=True,null=True,upload_to="media/")
	date = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)

################### order medication ###############################
    
class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    slug=models.SlugField(unique=True)
    description = models.TextField()
    is_latest=models.BooleanField(default=False)

    def __str__(self):
        return self.name

    #HII NI KWA AJILI YA KUPATA PRODUCT ZILIZOPO KWENYE CATEGORY HUSIKA
    def get_absolute_url(self):
        return reverse('product_by_category', args=[self.slug])

class Item(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField()
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    manufactured_date = models.DateField()
    expire_date = models.DateField()
    is_latest=models.BooleanField(default=False)
    is_featured=models.BooleanField(default=False)
    

    def __str__(self):
        return self.title
    #HII NI KWA AJILI YA KUADI ITEM TO A CART
    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'id': self.id})

    #HII NI KWA AJILI YA KUREMOVE ITEM FROMA CART
    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'id': self.id})
    #HII NI KWA AJILI YA KUREMOVE ITEM MOJAMOJA FROM A CART ENDAPO UTACLICK MINUS SIGN
    def get_remove_single_from_cart_url(self):
        return reverse('remove_single_from_cart', kwargs={'id': self.id})


class OrderItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_final_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()


class Order(models.Model):
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
    	return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()

        return total


import requests
import json

class BookDoctor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    district = models.CharField(max_length=200, db_index=True)
    ward = models.CharField(max_length=200, db_index=True)
    street = models.CharField(max_length=200, db_index=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    period = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.period:
            url = "https://messaging-service.co.tz/api/sms/v1/text/single"
            payload = {
                "from": "RMNDR",
                "to": self.user.phone,  # Update with the desired phone number
                "text": f"Dear - {self.user.username} we receive your request we will come on  - {self.period}",
                "reference": "aswqetgcv"
            }
            headers = {
                'Authorization': 'Basic QWdraWxhYjpLaW13ZXJpJjIwMjI=',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response = requests.post(url, headers=headers, data=json.dumps(payload))

            # Check if the request was successful (status code 2xx)
            if response.ok:
                print("SMS sent successfully")
            else:
                print(f"Failed to send SMS. Status code: {response.status_code}, Response: {response.text}")

        return super().save(*args, **kwargs)

    
# purpose section
class PurposeTop(models.Model):
    video_file = models.FileField(upload_to='media/',null=True, blank=True)
    header = models.CharField(max_length=500)
    subheader = models.CharField(max_length=500)
    description = models.TextField(max_length=5000)
    descriptionSecond = models.TextField(max_length=5000)
    problem = models.TextField(max_length=5000)
    solution = models.TextField(max_length=5000)

class Purpose(models.Model):
    description = models.TextField(max_length=5000)

class Success(models.Model):
    description = models.TextField(max_length=5000)

class FooterContact(models.Model):
    phonenumber = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

class FeaturedPage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
    
class LaboratoryTestCategory(models.Model):
    title = models.CharField(max_length=100)
    cost = models.IntegerField()
    def __str__(self):
        return self.title

class LaboratoryTest(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(LaboratoryTestCategory, on_delete=models.CASCADE)

class Team(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)

class ChatPay(models.Model):
    header = models.CharField(max_length=200)
    lipanamba = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    cost = models.CharField(max_length=100)
    notification = models.CharField(max_length=200)


class OrderConfirmation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(LaboratoryTestCategory, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.category.title} - {self.timestamp}"