from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory
from django.db.models import Q


# Inventory list with search
def inventory_list(request):
    query = request.GET.get('q')

    items = Inventory.objects.all().order_by('id')

    if query:
        items = items.filter(
            Q(item_name__icontains=query)
        )

    return render(request, 'inventory_list.html', {
        'items': items,
        'query': query
    })


# Add new inventory item
def add_inventory(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        quantity = request.POST.get('quantity')

        if item_name and quantity:
            Inventory.objects.create(
                item_name=item_name,
                quantity=int(quantity)
            )
        return redirect('inventory_list')

    return render(request, 'add_inventory.html')


# Edit inventory item
def edit_inventory(request, id):
    item = get_object_or_404(Inventory, id=id)

    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        quantity = request.POST.get('quantity')

        if item_name and quantity:
            item.item_name = item_name
            item.quantity = int(quantity)
            item.save()

        return redirect('inventory_list')

    return render(request, 'edit_inventory.html', {'item': item})


# Delete inventory item
def delete_inventory(request, id):
    item = get_object_or_404(Inventory, id=id)
    item.delete()
    return redirect('inventory_list')