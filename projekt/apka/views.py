from django.shortcuts import render, redirect, get_object_or_404
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
from django.contrib.auth.decorators import login_required
import uuid

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
        if form.is_valid():
            form.save()
            return render(request, 'apka/login.html')
    else:
        form = SignUpForm()
    return render(request, 'apka/signup.html', {'form': form})

def index(request):
    if 'sessionid' not in request.COOKIES:
        return redirect('logout')
    
    generated_image_url = request.session.pop('generated_image_url', None)
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

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
        return redirect('/apka')
    return JsonResponse({'status': 'error'}, status=403)

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
        image_uuid = str(uuid.uuid4())
        image_extension = os.path.splitext(image_url)[1]
        
        image_name = f"{image_uuid}{image_extension}"

        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        with open(image_path, 'wb') as f:
            f.write(image_response.content)
        
        relative_image_path = os.path.join(image_name)
        request.session['generated_image_url'] = relative_image_path
        
        return JsonResponse({'image_url': image_url})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)