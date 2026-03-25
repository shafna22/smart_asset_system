from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import AssetAssignment
from asset_management.models import Asset
from django.contrib.auth.decorators import login_required

User = get_user_model()


def assign_list(request):
    assignments = AssetAssignment.objects.select_related('employee', 'asset')
    return render(request, 'assign_list.html', {
        'assignments': assignments
    })


def assign_asset(request):
    employees = User.objects.filter(role='Employee')
    assets = Asset.objects.filter(status='Available')

    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        asset_id = request.POST.get('asset')

        employee = get_object_or_404(User, id=employee_id)
        asset = get_object_or_404(Asset, id=asset_id)

        # Create assignment
        AssetAssignment.objects.create(
            employee=employee,
            asset=asset
        )

        # Change asset status
        asset.status = 'Assigned'
        asset.save()

        return redirect('assign_list')

    return render(request, 'assign_asset.html', {
        'employees': employees,
        'assets': assets
    })


def return_asset(request, id):
    assignment = get_object_or_404(AssetAssignment, id=id)

    if not assignment.is_returned:
        assignment.is_returned = True
        assignment.return_date = timezone.now()
        assignment.save()

        asset = assignment.asset
        asset.status = 'Available'
        asset.save()

    return redirect('assign_list')



@login_required
def my_assets(request):
    assignments = AssetAssignment.objects.filter(
        employee=request.user,
        is_returned=False
    ).select_related('asset')

    return render(request, 'my_assets.html', {
        'assignments': assignments
    })