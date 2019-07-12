from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class OtherUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.CharField(max_length=59)
    phone_no = models.CharField(max_length=59, default="")
    role = models.IntegerField(default=0)
    profile_pic = models.CharField(max_length=255, default="")
    gender = models.CharField(max_length=1, default="m")
    user_auth = models.ForeignKey(User, on_delete=models.CASCADE, null="True")
    otp = models.IntegerField(default=0)
    otp_senttime = models.DateTimeField(null=True)
    otp_verify = models.IntegerField(default=0)
    address = models.CharField(max_length=255, default="")
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=255, default="")
    save_search = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    deviceId = models.CharField(max_length=191, default="")
    deviceType = models.CharField(max_length=1, default="")
    timezone = models.CharField(max_length=191, default="")
    onOffNotification = models.IntegerField(default=1)
    timezone = models.CharField(max_length=191, default="")
    created_date = models.DateField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'otheruser'


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)    
    
    class Meta:
        db_table = 'category'


class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    user = models.ForeignKey(OtherUser, blank=True, on_delete=models.CASCADE)
    added_date = models.DateField(blank=True, null=True)
    
    class Meta:
        db_table = 'item'

    
class ItemImageAndVideos(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Item, blank=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, blank=True, null=True)
    path = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'itemimageandvideos'

    
class Offers(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Item, blank=True, on_delete=models.CASCADE)
    price = models.CharField(max_length=20, blank=True, null=True) 
    offered_by = models.ForeignKey(OtherUser, blank=True, on_delete=models.CASCADE)
    offer_status = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'offers'

    
class Searches(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(OtherUser, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    
    class Meta:
        db_table = 'searches'


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(OtherUser, blank=True, related_name='sender_message', on_delete=models.CASCADE)
    receiver = models.ForeignKey(OtherUser, blank=True, related_name='receiver_message', on_delete=models.CASCADE)
    message = models.TextField()
    msg_time = models.DateTimeField(null=True)
    is_read = models.IntegerField(default=0)
    sender_status = models.IntegerField(default=1)
    receiver_status = models.IntegerField(default=1)

    class Meta:
        db_table = 'message'

    
class Notifications(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(OtherUser, related_name='sender_notification', on_delete=models.CASCADE)
    receiver = models.ForeignKey(OtherUser, blank=True, related_name='receiver_notification', on_delete=models.CASCADE)
    table_id = models.CharField(max_length=100, blank=True, null=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    notificationDate = models.DateTimeField(null="True")
    sender_status = models.IntegerField(default=1)
    receiver_status = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'notifications'

     
class ShipmentDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    shippername = models.CharField(max_length=255)
    package_id = models.IntegerField()
    user = models.ForeignKey(OtherUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'shipmentdetails'

    
class ContactUs(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(OtherUser, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'contactus'

