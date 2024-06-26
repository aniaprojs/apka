from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Hashtag, Comment
from .forms import PostForm, CommentForm
from django.http import JsonResponse
import os
from replicate.client import Client
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
import requests
from django.contrib.auth.decorators import login_required
import uuid
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
import nltk
from collections import Counter
import spacy

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
    
    user = request.user
    generated_image_url = request.session.pop('generated_image_url', None)

    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            posts = Post.search_by_hashtag(query).order_by('-created_at')
        else:
            posts = Post.objects.all().order_by('-created_at')
        return render(request, 'apka/index.html', {'posts': posts})
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if generated_image_url:
                post.image = generated_image_url
            post.save()
            
            hashtags_input = form.cleaned_data.get('hashtags')
            if hashtags_input:
                hashtags_list = [tag.strip() for tag in hashtags_input.split(',')]
                for tag in hashtags_list:
                    hashtag, created = Hashtag.objects.get_or_create(name=tag)
                    post.hashtags.add(hashtag)
            
            return redirect('index')
    else:
        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')

    context = {
        'user': user,
        'posts': posts,
        'form': form
    }
    return render(request, 'apka/index.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('index')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('/apka')
    else:
        form = CommentForm()
    return render(request, 'your_template.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
        return redirect('/apka')
    else:
        return JsonResponse({'status': 'error'}, status=403)

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

def get_hashtags(request):
    if request.method == 'POST':
        text = request.POST.get('content', '')
        print(text)
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)    
        nouns = [token.text for token in doc if token.pos_ == "NOUN"]
        adjectives = [token.text for token in doc if token.pos_ == "ADJ"]
        noun_counts = Counter(nouns)
        adjective_counts = Counter(adjectives)
        top_nouns = noun_counts.most_common(4)
        top_adjectives = adjective_counts.most_common(4)
        hashtags = [noun[0] for noun in top_nouns] + [adj[0] for adj in top_adjectives]
        print(hashtags)
        return JsonResponse({'hashtags': hashtags})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_title(request):
    if request.method == 'POST':
        text = request.POST.get('content', '')
        nltk.download('punkt')
        stopWords = set(stopwords.words("english")) 
        words = word_tokenize(text)
        
        # Creating a frequency table to keep the  score of each word    
        freqTable = dict() 
        for word in words: 
            word = word.lower() 
            if word in stopWords: 
                continue
            if word in freqTable: 
                freqTable[word] += 1
            else: 
                freqTable[word] = 1

        # Creating a dictionary to keep the score of each sentence 
        sentences = sent_tokenize(text) 
        sentenceValue = dict() 
        
        for sentence in sentences: 
            for word, freq in freqTable.items(): 
                if word in sentence.lower(): 
                    if sentence in sentenceValue: 
                        sentenceValue[sentence] += freq
                    else: 
                        sentenceValue[sentence] = freq 
        
        sumValues = 0
        for sentence in sentenceValue: 
            sumValues += sentenceValue[sentence] 
        
        # Highest value sentence will be the summary. 
        summary = max(sentenceValue, key=sentenceValue.get)
        return JsonResponse({'title': summary})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
