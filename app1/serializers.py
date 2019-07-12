from django.contrib.auth.models import User
from rest_framework import serializers
from .models import OtherUser, Category, Item, ItemImageAndVideos, Offers, Searches, Message, Notifications, ShipmentDetails, ContactUs


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class OtherUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OtherUser
        fields = ('__all__')

        
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('__all__')

        
class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ('__all__')


class ItemImageAndVideosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ItemImageAndVideos
        fields = ('__all__')

        
class OffersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Offers
        fields = ('__all__')


class SearchesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Searches
        fields = ('__all__')

        
class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ('__all__')

        
class NotificationsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notifications
        fields = ('__all__')

        
class ShipmentDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShipmentDetails
        fields = ('__all__')

        
class contactUsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContactUs
        fields = ('__all__')
        
