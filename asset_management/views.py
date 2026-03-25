from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .models import Asset
from inventory_management.models import Inventory


# ===============================
# Asset List (with search)
# ===============================
def asset_list(request):
    query = request.GET.get('q')

    assets = Asset.objects.all().order_by('asset_id')

    if query:
        assets = assets.filter(
            Q(name__icontains=query) |
            Q(asset_id__icontains=query) |
            Q(brand__icontains=query)
        )

    return render(request, 'asset_list.html', {
        'assets': assets,
        'query': query
    })


# ===============================
# Add Asset
# ===============================
def add_asset(request):
    inventory_items = Inventory.objects.all()

    if request.method == 'POST':
        asset_id = request.POST.get('asset_id')
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        inventory_id = request.POST.get('inventory_item')

        inventory_item = get_object_or_404(Inventory, id=inventory_id)

        if inventory_item.quantity <= 0:
            messages.error(request, "No stock available for this item.")
            return redirect('add_asset')

        # Reduce inventory quantity
        inventory_item.quantity -= 1
        inventory_item.save()

        Asset.objects.create(
            asset_id=asset_id,
            name=name,
            brand=brand,
            inventory_item=inventory_item,
            status='Available'
        )

        messages.success(request, "Asset added successfully.")
        return redirect('asset_list')

    return render(request, 'add_asset.html', {
        'inventory_items': inventory_items
    })


# ===============================
# Edit Asset
# ===============================
def edit_asset(request, id):
    asset = get_object_or_404(Asset, id=id)
    inventory_items = Inventory.objects.all()

    if request.method == 'POST':
        asset.asset_id = request.POST.get('asset_id')
        asset.name = request.POST.get('name')
        asset.brand = request.POST.get('brand')

        inventory_id = request.POST.get('inventory_item')
        asset.inventory_item = get_object_or_404(Inventory, id=inventory_id)

        asset.status = request.POST.get('status')
        asset.save()

        messages.success(request, "Asset updated successfully.")
        return redirect('asset_list')

    return render(request, 'edit_asset.html', {
        'asset': asset,
        'inventory_items': inventory_items
    })


# ===============================
# Delete Asset
# ===============================
def delete_asset(request, id):
    asset = get_object_or_404(Asset, id=id)

    # Return stock to inventory
    inventory_item = asset.inventory_item
    inventory_item.quantity += 1
    inventory_item.save()

    asset.delete()

    messages.success(request, "Asset deleted and stock updated.")
    return redirect('asset_list')