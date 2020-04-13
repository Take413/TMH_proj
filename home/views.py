from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from home.models import Category,Subcategory,CurrentPet,Pet
from home.forms import PetForm, UserForm, UserProfileForm,ProfileUpdateForm,UserUpdateForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

def homepage(request):
    category_list = Category.objects.order_by('name')
    context_dict = {}
    context_dict['title'] = 'Welcome'
    context_dict['categories'] = {}
    for cat in category_list:
        context_dict['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')
        
    response = render(request, 'home/homepage.html', context = context_dict)
    return response

def about(request):
    return render(request,'home/about.html')
def show_category(request,category_name_slug):
     context_dict = {}
     try:
         
         category_list = Category.objects.order_by('name')
         context_dict['categories'] = {}
    
         for cat in category_list:
             context_dict['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')
        
         category_chosen = Category.objects.get(slug=category_name_slug)
         context_dict['chosen_category']=category_chosen

         pets=CurrentPet.objects.filter(category=category_chosen).order_by('date')
         context_dict['pet'] = pets
     except Category.DoesNotExist:
         context_dict['subcategory'] = None
         context_dict['category'] = None
     return render(request,'home/category.html',context=context_dict)
def show_sub(request,category_name_slug,subcategory_name_slug):
     context_dict = {}
     try:
         subcategory=Subcategory.objects.get(slug=subcategory_name_slug)
         pets=CurrentPet.objects.filter(subcategory=subcategory).order_by('date')
         context_dict['subcategory'] = subcategory
         context_dict['category'] = subcategory.category
         context_dict['pets'] = pets
     except Subcategory.DoesNotExist:
         context_dict['subcategory'] = None
         context_dict['category'] = None
         context_dict['pets'] = None
     return render(request,'home/subcategory.html',context=context_dict)
def show_pet(request,category_name_slug,subcategory_name_slug,pet_name_slug):
     context_dict = {}
     try:
         pet=Pet.objects.get(slug=pet_name_slug)
         context_dict['subcategory'] = pet.subcategory
         context_dict['category'] = pet.category
         context_dict['pets'] = pet
     except Subcategory.DoesNotExist:
         context_dict['subcategory'] = None
         context_dict['category'] = None
         context_dict['pets'] = None
     return render(request,'home/pet.html',context=context_dict)
@login_required
def add_pet(request, category_name_slug,subcategory_name_slug):
    
    try:
        subcategory = Subcategory.objects.get(slug=subcategory_name_slug)
    except:
        subcategory = None
    
    # You cannot add a page to a Category that does not exist... DM
    if subcategory is None:
        return redirect(reverse('home:homepage'))
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None
    if category is None:
        return redirect(reverse('home:homepage'))

    form = PetForm()

    if request.method == 'POST':
        form = PetForm(request.POST)

        if form.is_valid():
            if category:
                pet = form.save(commit=False)
                pet.category = category
                pet.subcategory=subcategory
                pet.owner = owner
                pet.save()

                return redirect(reverse('home:show_category', kwargs={'category_name_slug': category_name_slug,'subcategory_name_slug': subcategory_name_slug,'pet':pet,'added':added}))
        else:
            print(form.errors)  # This could be better done; for the purposes of TwD, this is fine. DM.
    
    context_dict = {'form': form, 'category': category,'subcategory_name_slug': subcategory_name_slug,'pet':pet,'added':added}
    return render(request, 'home/add_pet.html', context=context_dict)
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request,'home/register.html',
    context = {'user_form': user_form,'profile_form': profile_form,
    'registered': registered})
@login_required
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'home/profile.html', args)
@login_required
def edit_profile(request):
    context_dict = {}
    changed = False
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            user_form =form.save()
            custom_form = profile_form.save(commit=False)
            custom_form.user = user_form
            if 'picture' in request.FILES:
                custom_form.picture = request.FILES['picture']
            custom_form.save()
            messages.success(request, f'Your account has been updated!')
            changed = True

    else:
        form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    context_dict['changed'] = changed
    context_dict ['form'] = form
    context_dict['profile_form'] = profile_form
    return render(request, 'home/edit_profile.html', context_dict)
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect (reverse ('home:homepage'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            print(f"Invalid login details:{username}, {password}")
            return HttpResponse ("Invalid login details supplied.")
    else:
        return render(request, 'home/login.html')
        
@login_required
def user_logout(request):
     logout(request)
     return redirect(reverse('home:homepage'))

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('home:view_profile'))
        else:
            return redirect(reverse('home:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'home/change_password.html', args)
@login_required
def restricted(request):
    return render(request, 'home/restricted.html')

