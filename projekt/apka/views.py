from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

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