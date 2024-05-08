from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.http import JsonResponse
import os
from replicate.client import Client
from django.conf import settings

def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()

    posts = Post.objects.all()

    context = {
        'posts': posts,
        'form': form
    }
    return render(request, 'apka/index.html', context)

def generate_image(request):
    print(request)
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
        print(output)
        return JsonResponse({'image_url': output[0]})
