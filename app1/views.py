from django.shortcuts import render
from .models import OtherUser, Category, Item, ItemImageAndVideos, Offers, Searches, Message, Notifications, ShipmentDetails, ContactUs
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, connection
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from datetime import datetime, timedelta, tzinfo
import requests
import codecs
import traceback
from django.http import HttpRequest  
from django.utils import timezone
import base64, random, pytz
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail , EmailMessage
from zenoo import settings 
from django.db.models import Q 
from app1.serializers import UserSerializer, OtherUserSerializer, CategorySerializer, ItemSerializer, ItemImageAndVideosSerializer, OffersSerializer, SearchesSerializer, MessageSerializer, NotificationsSerializer, ShipmentDetailsSerializer, contactUsSerializer
# Create your views here.

errorMessage = "Something went wrong, please try after sometime."
addSuccessMessage = "Successfully added"
updateSuccessMessage = "Successfully updated"
removeSuccessMessage = "Deleted successfully"
searchSuccessMessage = "search completed"
sendSuccessMessage = "sent message"


# Create your views here.
@api_view(['POST'])
def addZenoAdmin(request):
    try:
        with transaction.atomic():
            timeZone = request.META.get('HTTP_TIMEZONE')
            if timeZone is not None:
            # serializer.save()
                email = request.data['email']
                password = request.data['password']
                phone_no = request.data['phone_no']
                firstname = request.data['firstname']
                lastname = request.data['lastname']
                gender = request.data['gender']
                username = request.data['username']
                address = request.data['address']
                
                timeZone = pytz.timezone(request.META.get('HTTP_TIMEZONE'))
                nowTime = timezone.now().replace(microsecond=0)
                authuser = User.objects.create(username=phone_no,
                                               email='',
                                               first_name='',
                                               last_name='',
                                               password=make_password(password),
                                               is_superuser=0,
                                               is_staff=0,
                                               is_active=1,)
    #                                 date_joined=timezone.now())
                print(authuser.id, "id", type(authuser.id))
                g = Group.objects.get(name='Superuser')
                g.user_set.add(authuser)
                print(g)
                user1 = OtherUser.objects.create(
                                                email=email,
                                                phone_no=phone_no,
                                                firstname=firstname,
                                                lastname=lastname,
                                                gender=gender,
                                                user_auth_id=authuser.id,
                                                role=1,
                                                password=password,
                                                address=address
                                                        
                                                )
                print(user1)
                     
                token = Token.objects.create(user=authuser)
                        
                userDetail = {
                                'token': token.key,
                                'id': user1.id,
                                'firstname': user1.firstname,
                                'lastname' : user1.lastname,
                                'email': user1.email,
                                'notificationStatus': user1.onOffNotification,
                                'address':user1.address,
    #                                         'phone_no' :phone_no,
                                             
                            }
                    
                return Response({"status": "1", 'message': 'User has been successfully registered.', 'data': userDetail}, status=status.HTTP_200_OK)
            
            else:
                return Response({'status': "0", 'message': 'Timezone is missing!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : str(e), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def LoginZenoAdmin(request):
    try:
        with transaction.atomic():
            phone_no = request.data['phone_no']
            password = request.data['password']
            timeZone = request.META.get('HTTP_TIMEZONE')
            if timeZone is not None:
                timeZone = pytz.timezone(request.META.get('HTTP_TIMEZONE'))
                nowTime = timezone.now().replace(tzinfo=None).replace(microsecond=0)
                if phone_no != "":
                        try:
                            existedUser = OtherUser.objects.get(phone_no=phone_no, password=password, role=1)
                            print(existedUser)
                        except Exception as e3:
                            existedUser = None
                        if existedUser is not None:
                            authUser = authenticate(username=phone_no, password=password)
                            print(authUser)
                            if authUser is not None:
                                checkGroup = authUser.groups.filter(name='Superuser').exists()
                                if checkGroup:
                                    
                                    OtherUser.objects.filter(id=existedUser.id).update(timezone=timeZone)
                                    token = ''
                                    try:
                                        user_with_token = Token.objects.get(user=authUser)
                                    except:
                                        user_with_token = None
                                    if user_with_token is None:
                                        token1 = Token.objects.create(user=authUser)
                                        token = token1.key
                                    else:
                                        token = user_with_token.key
                                    
                                    userDetail = {
                                              'token': token,
                                              # 'id': existedUser.id,
                                              'firstname': existedUser.firstname,
                                              'lastname': existedUser.lastname,
                                              'email': existedUser.email,
                                              'notificationStatus': existedUser.onOffNotification,
                                              'address':existedUser.address,
                                            
                                                }
    
                                    return Response({"status": "1", 'message': 'Login successfully!', 'data': userDetail}, status=status.HTTP_200_OK)
                                else:
                                    return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)
                
                            else:
                                return Response({"message": "Email linked with another account", "status": "0"}, status=status.HTTP_200_OK)
                        else:
                            return Response({"message": "Email or password incorrect", "status": "0"}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': "0", 'message': 'Email is missing.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'status': "0", 'message': 'Timezone is missing!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def SignUpZenoUser(request):
    try:
        with transaction.atomic():
            timeZone = request.META.get('HTTP_TIMEZONE')
            if timeZone is not None:
            # serializer.save()
                email = request.data['email']
                password = request.data['password']
                phone_no = request.data['phone_no']
                firstname = request.data['firstname']
                lastname = request.data['lastname']
                gender = request.data['gender']
                latitude = request.data['latitude']
                longitude = request.data['longitude']
                username = request.data['username']
                deviceId = request.data['deviceId']
                deviceType = request.data['deviceType']
                address = request.data['address']
                
                timeZone = pytz.timezone(request.META.get('HTTP_TIMEZONE'))
                nowTime = timezone.now().replace(microsecond=0)
                if phone_no != "":
                    try:
                        existedUser = OtherUser.objects.get(phone_no=phone_no)
                    except Exception as e1:
                        existedUser = None
                    if existedUser is None:
                 
                        authuser = User.objects.create(username=phone_no,
                                    email='',
                                    first_name='',
                                    last_name='',
                                    password=make_password(password),
                                    is_superuser=0,
                                    is_staff=0,
                                    is_active=1,)
    #                                 date_joined=timezone.now())
                        print(authuser.id, "id", type(authuser.id))
                        g = Group.objects.get(name='User')
                        g.user_set.add(authuser)
                        print(g)
                        user1 = OtherUser.objects.create(
                                                        email=email,
                                                        phone_no=phone_no,
                                                        firstname=firstname,
                                                        lastname=lastname,
                                                        gender=gender,
                                                        latitude=latitude,
                                                        longitude=longitude,
                                                        user_auth_id=authuser.id,
                                                        deviceId=deviceId,
                                                        deviceType=deviceType,
                                                        role=2,
                                                        password=password,
                                                        address=address
                                                        
                                                          )
                        print(user1)
                     
                        token = Token.objects.create(user=authuser)
                        if deviceId != "" and deviceType != "":
                                OtherUser.objects.filter(id=user1.id).update(deviceId=deviceId, deviceType=deviceType)
                        userDetail = {
                                            'token': token.key,
                                            'id': user1.id,
                                            'firstname': user1.firstname,
                                            'lastname' : user1.lastname,
                                            'email': user1.email,
                                            'notificationStatus': user1.onOffNotification,
                                            'address':user1.address,
    #                                         'phone_no' :phone_no,
                                             
                                          }
                    
                        return Response({"status": "1", 'message': 'User has been successfully registered.', 'data': userDetail}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message" : "Sorry Something Went Wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'status': "0", 'message': 'phone_no is missing!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'status': "0", 'message': 'Timezone is missing!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : str(e), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def LoginZenoUser(request):
    try:
        with transaction.atomic():
            phone_no = request.data['phone_no']
            password = request.data['password']
            deviceId = request.data['deviceId']
            deviceType = request.data['deviceType']
            timeZone = request.META.get('HTTP_TIMEZONE')
            if timeZone is not None:
                timeZone = pytz.timezone(request.META.get('HTTP_TIMEZONE'))
                nowTime = timezone.now().replace(tzinfo=None).replace(microsecond=0)
                if phone_no != "":
                        try:
                            existedUser = OtherUser.objects.get(phone_no=phone_no, password=password, role=2)
                            print(existedUser)
                        except Exception as e3:
                            existedUser = None
                        if existedUser is not None:
                            authUser = authenticate(username=phone_no, password=password)
                            print(authUser)
                            if authUser is not None:
                                checkGroup = authUser.groups.filter(name='User').exists()
                                if checkGroup:
                                    if deviceId != "" and deviceType != "":
                                        OtherUser.objects.filter(id=existedUser.id).update(deviceId=deviceId, deviceType=deviceType)
                                    OtherUser.objects.filter(id=existedUser.id).update(timezone=timeZone)
                                    token = ''
                                    try:
                                        user_with_token = Token.objects.get(user=authUser)
                                    except:
                                        user_with_token = None
                                    if user_with_token is None:
                                        token1 = Token.objects.create(user=authUser)
                                        token = token1.key
                                    else:
                                        token = user_with_token.key
                                    
                                    userDetail = {
                                              'token': token,
                                              # 'id': existedUser.id,
                                              'firstname': existedUser.firstname,
                                              'lastname': existedUser.lastname,
                                              'email': existedUser.email,
                                              'notificationStatus': existedUser.onOffNotification,
                                              'address':existedUser.address,
                                              'latitude':existedUser.latitude,
                                              'longitude':existedUser.longitude,
                                            
                                                }
    
                                    return Response({"status": "1", 'message': 'Login successfully!', 'data': userDetail}, status=status.HTTP_200_OK)
                                else:
                                    return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)
                
                            else:
                                return Response({"message": "Email linked with another account", "status": "0"}, status=status.HTTP_200_OK)
                        else:
                            return Response({"message": "Email or password incorrect", "status": "0"}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': "0", 'message': 'Email is missing.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'status': "0", 'message': 'Timezone is missing!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def SendContactUsEmail(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='User').exists()
                except:
                    return Response({"message": "Session expired!! please login again", "status": "0"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                if checkGroup :
                    authuser = OtherUser.objects.get(user_auth_id=user.id)
                    authUserName = authuser.firstname
                    email = request.data['email']
                    subject = request.data['subject']
                    message = request.data['message']
                    user_id = request.data["user"]
                    u1 = OtherUser.objects.get(id=user_id)
                    user1 = ContactUs.objects.create(email=email,
                                                        name=authUserName,
                                                        user_id=u1.id,

                                                        );
                    
                    email_body = """\
                            <html>
                              <head></head>
                              <body>
                                <h2>%s</h2>
                                <p>%s</p>
                                <p> This email was sent from: </p>
                                <h5>%s</h5>
                                <h5>email:%s</h5>
                                <h5>address:%s</h5>
                              </body>
                            </html>
                            """ % (subject, message, authUserName, email, authuser.address)
                    recipient = []
                    recipient.append(settings.EMAIL_HOST_USER)
                    email = EmailMessage('Contact Us Mail ! ', email_body, to=recipient)
                    email.content_subtype = "html"  # this is the crucial part
                    response = email.send()
                    if response:
                        return Response({"status": "1", 'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET']) 
def LogOutZenoUser(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                except:
                    token1 = None
                    user = None
                if user is not None:
                    user.auth_token.delete()
                    return Response({"message": "Logged out successfully", "status": "1"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "session Expired ! Please Login Again.", "status": "0"},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        # transaction.rollback()
        return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def addCategory(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            print(API_key)
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='Superuser').exists()
                    
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                if checkGroup:
                    permissions = Permission.objects.filter(user=user)
                    if user.has_perm('app1.add_category'):
                        name = request.data["name"]
                        authuser = Category.objects.create(
                                                            name=name,
                                             );
                        if authuser is not None:
                            return Response({"message" : addSuccessMessage, "status" : "1", "object" : {"name" : Category.name}}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 # return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : str(e), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def addItems(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            print(API_key)
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    print(user)
                    checkGroup = user.groups.filter(name='User').exists()
                    print(checkGroup)
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                if checkGroup:
                    permissions = Permission.objects.filter(user=user)
                    if user.has_perm('app1.add_item'):
                        title = request.data["title"]
                        category_id = request.data["category"]
                        description = request.data["description"]
                        price = request.data["price"]
                        user_id = request.data["user"] 
                        added_date = request.data["added_date"]      
                    
                        print("category_id = ", category_id)
                        print("user_id = ", user_id)
                        u = Category.objects.get(id=category_id)
                        u1 = OtherUser.objects.get(id=user_id)
                        authuser = Item.objects.create(title=title,
                                                        category_id=u.id,
                                                        description=description,
                                                        price=price,
                                                        user_id=u1.id,
                                                        added_date=added_date,
                                                        );
                        if authuser is not None:
                            return Response({"message" : addSuccessMessage, "status" : "1", "object" : {"id" : Item.id}}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
                    else:
                        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : str(e), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def addItemsImageAnsVideos(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='User').exists()
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                if checkGroup:
                    permissions = Permission.objects.filter(user=user)
                    print(permissions)
                    if user.has_perm('app1.add_itemimageandvideos'):
                        item_id = request.data["item"]
                        type = request.data["type"]
                        path = request.data["path"]     
                    
                        print("item_id = ", item_id)
                        u = Item.objects.get(id=item_id)
                        authuser = ItemImageAndVideos.objects.create(item_id=u.id,
                                                        type=type,
                                                        path=path,
                                                        );
                        if authuser is not None:
                            return Response({"message" : addSuccessMessage, "status" : "1", "object" : {"id" : ItemImageAndVideos.id}}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
                    else:
                        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : str(e), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def zenoSearch(request):
    try:
        with transaction.atomic():
            API_key = request.META.get("HTTP_AUTHORIZATION")
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='User').exists()
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                if checkGroup:
                    permissions = Permission.objects.filter(user=user)
                    if user.has_perm('app1.add_searches'):
                        user_id = request.data["user"]
                        category_id = request.data["category"]
#                         latitude = request.data["latitude"]
#                         longitude = request .data["longitude"]
                        min_price = request.data["min_price"]
                        max_price = request.data["max_price"]
                        
#                         condition = ""
#                         if min_price != "-1" and max_price != -1:
#                             condition = " where price between " + str(min_price) + " and " + str(max_price)
#                         elif max_price != "-1":
#                             condition = " where price = " + str(max_price) 
#                         elif min_price != -1:
#                             condition = " where price = " + str(min_price)
                        cursor = connection.cursor()
                        cursor.execute("select item.title,item.category_id ,item.price,( 3959 * acos(cos(radians(37)) * cos(radians(otheruser.latitude)) * cos(radians(otheruser.longitude) - radians(-122)) + sin(radians(37)) * sin(radians(otheruser.latitude)))) As distance from item inner join otheruser on item.user_id = otheruser.id where item.price between " + str(min_price) + " AND " + str(max_price) + " and category_id=" + str(category_id) + " having distance<8000")
                        itemsRaw = dictfetchall(cursor)
                        cursor.close()
                        print(itemsRaw)
                        
                        u = Category.objects.get(id=category_id)
                        u1 = OtherUser.objects.get(id=user_id)
                        u2 = OtherUser.objects.get(id=user_id)
                        rr = u2.save_search
                        if rr == 1:
                            authuser = Searches.objects.create(user_id=u1.id,
                                                        category_id=u.id,
                                                        min_price=min_price,
                                                        max_price=max_price
                                                        );
                                                          
                            return Response({"message" : addSuccessMessage, "status" : "1", "object" : {"id" : Searches.id}}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"Cursor":itemsRaw}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : str(e), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


@api_view(['GET'])
def getUserList(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
        if API_key is not None:
            try:
                token1 = Token.objects.get(key=API_key)
                user = token1.user
                checkUser = user.groups.filter(name='User').exists()
                print(checkUser)
            except:
                return Response({'message' : "Session expired! Please login again", "status":"0"}, status=status.HTTP_401_UNAUTHORIZED)
                
            if checkUser is not None:
                user1 = OtherUser.objects.get(user_auth_id=user.id)
                userdetail = {
                    "firstname":user1.firstname,
                    "lastname":user1.lastname,
                    "phone_no" : user1.phone_no,
                    "gender" : user1.gender,
                    "username" : user1.username,
                    "email" : user1.email,
                    "address" : user1.address
                    }
                return Response({"status": "1", 'message': 'Get successfully.', 'data':userdetail}, status=status.HTTP_200_OK)

            else:
                return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        # print(e)
        return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def getItemList(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
        if API_key is not None:
            try:
                token1 = Token.objects.get(key=API_key)
                user = token1.user
                print(user)
                checkGroup = user.groups.filter(name='User').exists()
            except:
                return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            if checkGroup:
                    # if user.has_perm('appadmin.can_view_busTypes'):
                        user1 = OtherUser.objects.get(user_auth_id=user.id)
                        items = Item.objects.filter(user_id=user1.id)
                        itemsSerializer = ItemSerializer(items, many=True)
#                                 
                        return Response(itemsSerializer.data, status=status.HTTP_200_OK)
                    # else:
                        # return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        print(traceback.format_exc())
        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def makeOffer(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='User').exists()
                    print(checkGroup)
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                if checkGroup:
                    permissions = Permission.objects.filter(user=user)
                    if user.has_perm('app1.add_offers'):
                        item_id = request.data["item"]
                        price = request.data["price"]
                    
                        print("item_id = ", item_id)
                        u = Item.objects.get(id=item_id)
                        u1 = OtherUser.objects.get(user_auth_id=user.id)
                        print(u.id)
                        print(u1.id)
                        authuser = Offers.objects.create(item_id=u.id,
                                                        offer_status=1,
                                                        offered_by_id=u1.id,
                                                        price=price,
                                                        )
                        if authuser is not None:
                            return Response({"message" : addSuccessMessage}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
                    else:
                        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : str(e), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def sendMessage(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='User').exists()
                    print(checkGroup)
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                if checkGroup:
                    permissions = Permission.objects.filter(user=user)
                    if user.has_perm('app1.add_message'):
                        receiver_id = request.data["receiver"]
                        message = request.data["message"]
                    
                        u1 = OtherUser.objects.get(user_auth_id=user.id)
                        print(u1.id)
                        authuser = Message.objects.create(sender_id=u1.id,
                                                        receiver_id=receiver_id,
                                                        message=message,
                                                        )
                        if authuser is not None:
                            return Response({"message" : sendSuccessMessage}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : str(e), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def getMessage(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='User').exists()
                    print(checkGroup)
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                if checkGroup:
                    u1 = OtherUser.objects.get(user_auth_id=user.id)
#                     msg = Message.objects.filter(sender_id=u1.id).order_by('-msg_time')
#                     msgSerializer = MessageSerializer(msg, many=True)
#                     return Response(msgSerializer.data, status=status.HTTP_200_OK)
                    cursor = connection.cursor()
                    cursor.execute("select * from message where ((sender_id =" + str(u1.id) + "  and sender_status = 1) and (receiver_id = " + str(u1.id) + " or receiver_status = 1)) and id in (select max(id) from message group by if(sender_id = " + str(u1.id) + ", concat(sender_id,' ',receiver_id), concat(receiver_id, ' ', sender_id)));")
                    itemsRaw = dictfetchall(cursor)
                    cursor.close()
                    print(itemsRaw)
                    return Response(itemsRaw, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : str(e), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def receiveMessage(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkUser = user.groups.filter(name='User').exists()
                    print(checkUser)
                except:
                    return Response({'message' : "Session expired! Please login again", "status":"0"}, status=status.HTTP_401_UNAUTHORIZED)
                if checkUser is not None:
                    u = OtherUser.objects.get(user_auth_id=user.id)
                    
                    authuser = Message.objects.filter(receiver_id=u.id).update(is_read=1)
                    print(authuser)
                    return Response({"message": "received successfully", "status":"1"}, status=status.HTTP_200_OK)
                
                else:
                    return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print(traceback.format_exc())
        return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def deteteMessage(request, pk=None):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkUser = user.groups.filter(name='User').exists()
                    print(checkUser)
                except:
                    return Response({'message' : "Session expired! Please login again", "status":"0"}, status=status.HTTP_401_UNAUTHORIZED)
                if checkUser is not None:
                    u = OtherUser.objects.get(user_auth_id=user.id)
                    if pk:
                        cursor = connection.cursor()
                        cursor.execute(" update message SET sender_status = 0 where (sender_id=" + str(u.id) + " and receiver_id=" + str(pk) + ")")
                        # itemsRaw = dictfetchall(cursor)
                        cursor.execute("update message SET receiver_status = 0 where ( receiver_id = " + str(u.id) + " and sender_id = " + str(pk) + ")")
                        cursor.close()
                        # print(itemsRaw)
                        
                    return Response({"message": "delete successfully", "status":"1"}, status=status.HTTP_200_OK)
                
                else:
                    return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print(traceback.format_exc())
        return Response({"message": errorMessage, "status": "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def getNotification(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='User').exists()
                    print(checkGroup)
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                if checkGroup:
                    permissions = Permission.objects.filter(user=user)
                    if user.has_perm('app1.add_notifications'):
                        receiver_id = request.data["receiver"]
                        table_id = request.data['table_id']
                        tag = request.data['tag']
                        message = request.data["message"]
                        u1 = OtherUser.objects.get(user_auth_id=user.id)
                        print(u1.id)
                        authuser = Notifications.objects.create(sender_id=u1.id,
                                                        receiver_id=receiver_id,
                                                        message=message,
                                                        table_id=table_id,
                                                        tag=tag,
                                                        )
                        if authuser is not None:
                            return Response({"message" : sendSuccessMessage}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : str(e), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def sendShipmentDetail(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='User').exists()
                    print(checkGroup)
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                if checkGroup:
                    permissions = Permission.objects.filter(user=user)
                    if user.has_perm('app1.add_shipmentdetails'):
                        shippername = request.data["shippername"]
                        package_id = request.data['package_id']
                        item_id = request.data['item']
                        u1 = OtherUser.objects.get(user_auth_id=user.id)
                        u = Item.objects.get(id=item_id)
                        
                        authuser = ShipmentDetails.objects.create(user_id=u1.id,
                                                        item_id=item_id,
                                                        shippername=shippername,
                                                        package_id=package_id,
                                                        )
                        if authuser is not None:
                            return Response({"message" : sendSuccessMessage}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : errorMessage, "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"message" : str(e), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

