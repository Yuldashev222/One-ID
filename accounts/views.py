from django.shortcuts import render, HttpResponse, redirect
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm  
# Create your views here.
from .models import User
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .forms import UserCr

# from .serializers import User


def loginReg(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('dashboard', request.user.username)
    
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard', user.username)
        else:
            return redirect('redirect_url')
        
    return render(request, 'login.html')


def code(request): 
    code = request.GET.get('code')
    grant_type = 'one_authorization_code'
    client_id = 'unicon_yagona_billing'
    client_secret = 'N3nk50XmyQFqijewiohDFZdB'
    redirect_uri = 'http://127.0.0.1:8000/code/'

    url = 'https://sso.egov.uz/sso/oauth/Authorization.do'
    data = {'code': code, 'grant_type': grant_type, 'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': redirect_uri,}
    
    req = requests.post(url=url, params=data)
    
    grant_type = 'one_access_token_identify'
    access_token = dict(req.json()).get('access_token')
    scope = dict(req.json()).get('scope')
    
    data = {'grant_type': grant_type, 'client_id': client_id, 'client_secret': client_secret, 'access_token': access_token, 'scope': scope,}
    
    req = requests.post(url=url, params=data)
    
    username = dict(req.json()).get('user_id')
      
    # password = dict(req.json()).get('sess_id')

    users = list(map(lambda item: item[0], User.objects.all().values_list('username')))
    
    try: 
        user = User.objects.get(username=username)
    except:
        user = None
    
    if not user:
        user = User.objects.create(username=username)
        user.first_name = dict(req.json()).get('first_name')
        user.last_name = dict(req.json()).get('sur_name')
        user.address = dict(req.json()).get('per_adr')
        user.save()
        
    login(request, user)
        
    return redirect('dashboard', user.username)        
        
    
def register(request):
    form = UserCr()
    if request.POST:
        form = UserCr(request.POST)

        if form.is_valid():
            form.save()
                    
            return redirect('redirect_url')

    return render(request, 'register.html', {'form': form})


def dashboard(request, username):

    user = User.objects.get(username=username)
    
    return render(request, 'index.html', {'user': user})
    
