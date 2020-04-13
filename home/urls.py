from django.urls import path
from home import views
app_name = 'home'
urlpatterns = [
path('', views.homepage, name='homepage'),
path('about/',views.about,name='about'),
path('register/',views.register,name='register'),
path('logout/',views.user_logout,name='user_logout'),
path('login/',views.user_login,name='user_login'),
path('restricted/',views.restricted,name='restrcited'),
path('edit_profile/',views.edit_profile,name='edit_profile'),
path('view_profile/',views.view_profile,name='view_profile'),
path('view_profile/change_password',views.change_password,name='change_password'),
path('<slug:category_name_slug>/',views.show_category,name='show_category'),
path('<slug:category_name_slug>/<slug:subcategory_name_slug>',views.show_sub,name='show_subcategory'),
path('<slug:category_name_slug>/<slug:subcategory_name_slug>/<slug:pet_name_slug>',views.show_pet,name='show_pet'),
path('<slug:category_name_slug>/<slug:subcategory_name_slug>/<slug:pet_name_slug>/add a pet',views.add_pet,name='add_pet'),





]