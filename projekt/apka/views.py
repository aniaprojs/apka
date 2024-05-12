from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.http import JsonResponse
import os
from replicate.client import Client
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.shortcuts import HttpResponse
import requests

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/apka')
        else:
            return render(request, 'apka/login.html', {'error': 'Invalid username or password'})
    return render(request, 'apka/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            print("VALID")
            form.save()
            return redirect('apka/login')
    else:
        form = SignUpForm()
    return render(request, 'apka/signup.html', {'form': form})

def index(request):
    if 'sessionid' not in request.COOKIES:
        return redirect('logout')
    
    generated_image_url = request.session.pop('generated_image_url', None)
    print(generated_image_url)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if generated_image_url:
                post.image = generated_image_url
            post.save()
            return redirect('index')
    else:
        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')

    context = {
        'posts': posts,
        'form': form
    }
    return render(request, 'apka/index.html', context)

def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        try:
            post = Post.objects.get(pk=post_id)
            post.delete()
            return HttpResponse('Post deleted successfully', status=200)
        except Post.DoesNotExist:
            return HttpResponse('Post does not exist', status=404)
    return HttpResponse('Invalid request method', status=405)


def generate_image(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        client = Client(api_token=os.environ.get('REPLICATE_API_TOKEN'))
        input = {
            "prompt": prompt,
            "scheduler": "K_EULER"
        }
        output = client.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input=input
        )
        
        image_url = output[0]
        
        image_response = requests.get(image_url)
        
        image_name = os.path.basename(image_url)
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        with open(image_path, 'wb') as f:
            f.write(image_response.content)
        
        relative_image_path = os.path.join(image_name)
        print(relative_image_path)
        request.session['generated_image_url'] = relative_image_path
        
        return JsonResponse({'image_url': image_url})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)