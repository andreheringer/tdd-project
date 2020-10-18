from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError

def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    my_list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': my_list})

def new_list(request):
    my_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=my_list)
    return redirect(f'/lists/{my_list.id}/')

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(f'/lists/{list_.id}/')