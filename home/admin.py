from django.contrib import admin
from home.models import Category, Subcategory,CurrentPet,GivenPet,Favorite,Review,UserProfile
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
  
class CurrentPetAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class GivenPetAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Subcategory,SubcategoryAdmin)
admin.site.register(CurrentPet,CurrentPetAdmin)
admin.site.register(GivenPet,GivenPetAdmin)
