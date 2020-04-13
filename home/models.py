from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Take from here username, password, email, first:_name, last_name
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    address = models.CharField(max_length = 128)
    city = models.CharField(max_length = 20)
    postcode = models.CharField(max_length = 10)
    description = models.TextField(help_text = "Tell us something about you")
    picture = models.ImageField(upload_to='profile_images', default='media/profile_images/default-user.png')
    dob = models.DateField(null=True)
    isGiver = models.BooleanField(default = False)
    slug = models.SlugField(unique = True)
    date_reg = models.DateField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length = 128, unique = True)
    slug = models.SlugField(unique = True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name
class Subcategory(models.Model):
    name = models.CharField(max_length = 128, unique = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    slug = models.SlugField(unique = True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "subcategories"
        
    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length = 128, help_text = "eg.cute cat")
    subcategory = models.ForeignKey(Subcategory, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete = models.CASCADE)
    description = models.TextField(help_text = "Tell something about the pet")
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    slug = models.SlugField(unique = True)
    
    image1 = models.ImageField(upload_to='pet_images', default='pet_images/default.png')
    
    def save(self, *args, **kwargs):
           self.slug = slugify(self.name)
           super(Pet, self).save(*args, **kwargs)
        
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name

class CurrentPet(Pet):
    image2 = models.ImageField(upload_to='pet_images', blank = True)
    image3 = models.ImageField(upload_to='pet_images', blank = True)
    image4 = models.ImageField(upload_to='pet_images', blank = True)
    image5 = models.ImageField(upload_to='pet_images', blank = True)
    owner = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name="owner")
class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    pets = models.ManyToManyField(CurrentPet)
class GivenPet(Pet):
    adopter = models.ForeignKey(UserProfile, on_delete=models.SET("This user no longer exists"), blank = False, related_name="adopter" )
    giver = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name="given_by")

class Review(models.Model):
    title = models.CharField(max_length = 128, help_text = "Insert title here")
    text = models.TextField(help_text = "Tell us how the owner was")
    giver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reviewed")
    adopter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reviewer")
    on_date = models.DateField(auto_now_add=True, blank=True, null=True)
    rating = models.IntegerField(blank = False)
    def __str__(self):
        return self.title
