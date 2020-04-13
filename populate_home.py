import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TMH_project.settings')

import django
django.setup()
from home.models import Category,Subcategory,CurrentPet, GivenPet, UserProfile, Review

def populate():

    Dogs = [{'name':'Bulldog'},
            {'name':'Pug'},
            {'name':'German Shepherd'},
            {'name':'Samoyed'},
            {'name':'Pointer'},
            {'name':'Chihuahua'},
            ]
        
    Cats= [{'name':'British Shorthair'},
            {'name':'Maine Coon'},
            {'name':'Ragdoll'},
            {'name':'Scottish Fold'},
            {'name':'Norweigian Forest cat'},
            {'name':'American Shorthair'},]
        
        
    categories = {'Dogs':{'subcategories':Dogs},
       'Cats': {'subcategories':Cats},}
       
    for cat, cat_data in categories.items():
        c = add_cat(cat)
        for p in cat_data['subcategories']:
            add_subcat(c, p['name'])
            
    for c in Category.objects.all():
        for p in Subcategory.objects.filter(category=c):
            print(f'- {c}: {p}')
            
            
def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c
    
def add_subcat(cat, name):
    s = Subcategory.objects.get_or_create(category=cat, name=name)[0]
    s.save()
    return s

if __name__ == '__main__':
    print('Starting home population script...')
    populate()
    
