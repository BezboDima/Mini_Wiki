from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from . import util

markdowner = Markdown()

#Form class with title and context(body) for creating a new page and editing
class NewTitle(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : "form-control col-lg-9 col-md-10"}))
    body= forms.CharField(widget=forms.Textarea(attrs={'class' : "form-control col-lg-9 col-md-10"}))
    
#Rebders a list of all existing entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#Renders entry page if such exists, if not gives an error to the user 
def entry(request, name):
    
    try:
        entry = util.get_entry(f"{name}")
        html_converted = markdowner.convert(entry)
        
    except TypeError:
        return render(request, "encyclopedia/error.html")
        
    return render(request, "encyclopedia/entry.html",{
        "entry_code": html_converted,
        "entry_name" : name
    })
    
# If user searches for a specific page and wries the whole name of the page, gets him to that page directly. 
# If user input is partly in the page's name, gives him a list of possible choices to pick 
# If nothing was found gives an error to the user 
def search(request):
    
    name = str(request.GET.get("q",""))
    list = util.list_entries()
    list_to_display = []
    
    for page in list:
        if page.casefold() == name.casefold():
            return HttpResponseRedirect(reverse("entry", kwargs={'name' : name}))
           
        elif name.casefold() in page.casefold():
            list_to_display.append(page)
    
    if  len(list_to_display) == 0:
        return render(request, "encyclopedia/error.html")
    
    else:
        return render(request, "encyclopedia/search.html", {
        "entries": list_to_display
    })
# Creates a form that is able to create a new page. If the page title already exists or form is  not valid gives error, but lets user to try again
# If everything is valid creates a new page and redirects usre to that page
def new(request):

    if request.method == "POST":
        title = NewTitle(request.POST)
        
        if (title.is_valid()):
            name = title.cleaned_data["title"]
            list = util.list_entries()
            if (name.casefold() in list):
                print("here")
                return render(request, "encyclopedia/new.html",{
                "title" : title,
                "exist" : True,
                "page" : name
                })
            else:
                context = title.cleaned_data["body"]
            
                name.split()
                name = name.replace(" ", "-")
            
                util.save_entry(name, context)

                return HttpResponseRedirect(reverse("entry", kwargs={'name' : name}))
        else:
            return render(request, "encyclopedia/new.html",{
            "title" : title,
            "exist" : False
        })
    
    return render(request, "encyclopedia/new.html", {
        "title" : NewTitle()
    })
    
# Lets user to edit an existing page. If the for is valid the page is replaced with the new one
def edit(request, name):
    if request.method == "POST":
        edited = NewTitle(request.POST)
        
        if (edited.is_valid()):
            context = edited.cleaned_data["body"]
            
            util.save_entry(name, context)
            
            return HttpResponseRedirect(reverse("entry", kwargs={'name' : name}))
        else:
            return render(request, "encyclopedia/edit.html",{
            "form" : edited,
            "entry_name" : name
        })      
        
    else:
        try:
            entry = util.get_entry(f"{name}")
        
        except TypeError:
            return render(request, "encyclopedia/error.html")
    
        # Hides the title from the user and lets him to edit context only 
        form = NewTitle()
        form.fields["title"].initial = name
        form.fields["body"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
    
    
        return render(request, "encyclopedia/edit.html", {
            "form" : form,
            "entry_name" : name
        })

# Gets a random page to display
def rand(request):
    list = util.list_entries()
    rand = random.randint(0, list.__len__() - 1)
    name = list[rand]
            
    return HttpResponseRedirect(reverse("entry", kwargs={'name' : name}))
    
    
    
    
    