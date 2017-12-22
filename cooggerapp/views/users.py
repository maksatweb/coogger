# kullanıcıların yaptıkları tüm işlemler
from PIL import Image
import os

from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib import messages as ms

from cooggerapp.models import ContentList,OtherInformationOfUsers,Content,UserFollow
from cooggerapp.forms import UserFollowForm
from cooggerapp.views.tools import hmanynotifications
from cooggerapp.views.home import content_cards


def user(request,username):
    "herhangi kullanıcının anasayfası"
    user = User.objects.filter(username = username)[0]
    nav_category = ContentList.objects.filter(user = user)
    try:
        user_follow = UserFollow.objects.filter(user = user)
    except:
        user_follow = []
    # yaptığı paylaşımlar
    queryset = Content.objects.filter(user = user)
    info_of_cards = content_cards(request,queryset)
    facebook = get_facebook(user)
    elastic_search = dict(
     title = username+" | coogger",
     keywords =username+","+user.first_name+" "+user.last_name,
     description =user.first_name+" "+user.last_name+", "+username+" adı ile coogger'da",
     author = facebook,
    )
    output = dict(
        users = True,
        username = user,
        blog = info_of_cards[0],
        paginator = info_of_cards[1],
        user_follow = user_follow,
        nav_category = nav_category,
        ogurl = request.META["PATH_INFO"],
        elastic_search = elastic_search,
        hmanynotifications = hmanynotifications(request),
    )
    return render (request,"users/user.html",output)

def upload_pp(request):
    "kullanıcılar profil resmini  değiştirmeleri için"
    request_username = request.user.username
    if request.method == "POST":
        try:
            image=request.FILES['u-upload-pp']
        except:
            ms.error(request,"Dosya alma sırasında bir sorun oluştu")
            return HttpResponseRedirect("/@"+request_username)

        with open(os.getcwd()+"/coogger/media/users/pp/pp-"+request_username+".jpg",'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        im = Image.open(os.getcwd()+"/coogger/media/users/pp/pp-"+request_username+".jpg")
        im.thumbnail((350,350))
        try: # resim yükleme sırasında bir hata olursa pp = False olacak hata olmaz ise True
            im.save(os.getcwd()+"/coogger/media/users/pp/pp-"+request_username+".jpg", "JPEG")
            user_id = User.objects.filter(username = request_username)[0].id
            OtherInformationOfUsers.objects.filter(user_id = user_id).update(pp = True)
        except:
            OtherInformationOfUsers.objects.filter(user_id = user_id).update(pp = False)
        return HttpResponseRedirect("/@"+request_username)

def u_topic(request,username,utopic):
    "kullanıcıların kendi hesaplarında açmış olduğu konulara yönlendirme"
    user = User.objects.filter(username = username)[0]
    queryset = Content.objects.filter(user = user,content_list = utopic)
    if not queryset.exists():
        ms.error(request,"{} adlı kullanıcı nın {} adlı bir içerik listesi yoktur".format(username,utopic))
        return HttpResponseRedirect("/")
    info_of_cards = content_cards(request,queryset)
    nav_category = ContentList.objects.filter(user = user)
    facebook = get_facebook(user)
    try:
        user_follow = UserFollow.objects.filter(user = user)
    except:
        user_follow = []
    elastic_search = dict(
     title = username+" - "+utopic+" | coogger",
     keywords = username+" "+utopic+","+utopic,
     description = username+" kullanıcımızın "+utopic+" adlı içerik listesi",
     author = facebook,
    )
    output = dict(
        blog = info_of_cards[0],
        general = True,
        paginator = info_of_cards[1],
        nav_category = nav_category,
        ogurl = request.META["PATH_INFO"],
        nameoftopic = utopic,
        username = username,
        nameoflist = "Listeler",
        elastic_search = elastic_search,
        hmanynotifications = hmanynotifications(request),
        user_follow = user_follow,
    )
    return render (request,"users/user.html",output)

def get_facebook(user):
    facebook = None
    try:
        for f in UserFollow.objects.filter(user = user):
            if f.choices  == "facebook":
                facebook = f.adress
    except:
        pass
    return facebook
