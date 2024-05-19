from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(Hashtag, related_name='posts')

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return Like.objects.filter(post=self).count()
    
    def is_liked_by_user(self, user):
        return Like.objects.filter(post=self, user=user).exists()
    
    def get_hashtags(self):
        return self.hashtags.all()
    
    @staticmethod
    def search_by_hashtag(query):
        if query:
            return Post.objects.filter(hashtags__name__icontains=query)
        else:
            return Post.objects.all()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user} likes {self.post}"

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
