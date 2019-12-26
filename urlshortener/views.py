import os
from django.http import HttpResponse, JsonResponse
from .models import Register,Shortner
import datetime,random
from django.shortcuts import redirect
import re
from rest_framework.views import APIView

class user_reg(APIView):

    def post(self,request):
        try:
            x=request.data
            newuser = Register()
            newuser.username = x["username"]
            newuser.pwd = x["pwd"]
            newuser.save()
            return JsonResponse({"Status":"Registered Successfully"})
        except:
            return JsonResponse({"Status":"Sorry user not created,may already exist"})

class login(APIView):
    def post(self,request):
       url_get = os.environ.get('SERVER_NAME')
       if(Register.objects.filter(username=request.data["username"],pwd=request.data["pwd"])):
           todays_urls=Shortner.objects.filter(userid=request.data["username"],date=datetime.date.today()).values_list('url','urlshort')
           data=dict(todays_urls)
           val=[url_get+'/'+i for i in data.values()]
           res_data=dict(zip(data.keys(),val))
           return JsonResponse(res_data)
       else:
           return JsonResponse({"Status":"Invalid username or pwd"})

class generate_shorturl(APIView):
    def shortenfun(self,url):
        r1 = re.split(r"www.",url)
        url1=r1[1][0:2]+str(random.randint(1,1000))
        return url1

    def post(self,request):
        reqdata=request.data
        if (Register.objects.filter(username=reqdata["username"])):
             if (Shortner.objects.filter(userid=reqdata["username"],url=reqdata["url"],date=datetime.date.today())):
                return JsonResponse({"Status":"You have already created shorturl for this url today"})
             else:
                reg_user = Register.objects.get(username=reqdata["username"])
                shorten=Shortner()
                shorten.userid = reg_user
                shorten.url=reqdata["url"]
                shorten.date=datetime.date.today()
                shorten.urlshort=self.shortenfun(reqdata["url"])
                url_get = os.environ.get('SERVER_NAME')
                result=url_get+'/'+shorten.urlshort
                try:
                    shorten.save()
                    return JsonResponse({'Shorturl':result})
                except:
                    shorten.urlshort+='1'
                    result=result+'1'
                    shorten.save()
                    return JsonResponse({'Shorturl':result})


        else:
            return JsonResponse({"Error":"User doesnot exists.Pls register"})


def geturl_browser(self,shorturl):
      try:
        x=Shortner.objects.get(urlshort=shorturl)
        return redirect(x.url)
      except:
        return HttpResponse("Invalid short url")
