from django.contrib import admin
from app1.models import OtherUser, Category, Item, ItemImageAndVideos, Offers, Searches, Message, Notifications, ShipmentDetails, ContactUs

# Register your models here.
admin.site.register(OtherUser)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemImageAndVideos)
admin.site.register(Offers)
admin.site.register(Searches)
admin.site.register(Message)
admin.site.register(Notifications)
admin.site.register(ShipmentDetails)
admin.site.register(ContactUs)
