from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.db.models import Q
from .forms import EditUserForm
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'home.html')

# Sign Up
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Employee'   # force role
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.role == 'Admin':
                    return redirect('admin_dashboard')
                return redirect('employee_dashboard')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

def admin_dashboard(request):
    if request.user.is_authenticated and request.user.role == 'Admin':
        return render(request, 'admin_dashboard.html')
    return redirect('login')

def employee_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'employee_dashboard.html')
    return redirect('login')



#manage_users

@login_required
def manage_users(request):
   
    if request.user.role != 'Admin':
        return redirect('login')

    query = request.GET.get('q')

    users = CustomUser.objects.all().order_by('-date_joined')

    
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(role__icontains=query)
        )

    context = {
        'users': users,
        'query': query
    }
    return render(request, 'manage_users.html', context)



@login_required
def deactivate_user(request, user_id):
    if request.user.role != 'Admin':
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('manage_users')


@login_required
def activate_user(request, user_id):
    if request.user.role != 'Admin':
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('manage_users')


@login_required
def edit_user(request, user_id):
    if request.user.role != 'Admin':
        return redirect('login')

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = EditUserForm(instance=user)

    return render(request, 'edit_user.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from asset_management.models import Asset
from asset_assignment.models import AssetAssignment
from tickets.models import Ticket
from inventory_management.models import Inventory
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def reports_view(request):
    # Summary stats
    total_users = User.objects.count()
    total_inventory = Inventory.objects.count()
    total_assets = Asset.objects.count()
    assigned_assets = AssetAssignment.objects.filter(is_returned=False).count()
    total_tickets = Ticket.objects.count()
    
    # Ticket status counts
    pending_tickets = Ticket.objects.filter(status="Pending").count()
    in_progress_tickets = Ticket.objects.filter(status="In Progress").count()
    resolved_tickets = Ticket.objects.filter(status="Resolved").count()
    retired_tickets = Ticket.objects.filter(status="Retired").count()
    
    # Low stock items (using quantity < 10 as threshold)
    low_stock_items = Inventory.objects.filter(quantity__lt=10)
    
    context = {
        'total_users': total_users,
        'total_inventory': total_inventory,
        'total_assets': total_assets,
        'assigned_assets': assigned_assets,
        'total_tickets': total_tickets,
        'pending_tickets': pending_tickets,
        'in_progress_tickets': in_progress_tickets,
        'resolved_tickets': resolved_tickets,
        'retired_tickets': retired_tickets,
        'low_stock_items': low_stock_items,
    }
    
    return render(request, 'reports.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def report_employee_view(request):
    user = request.user  # logged-in employee

    # Assets assigned to this employee
    assigned_assets_qs = AssetAssignment.objects.filter(employee=user)
    assigned_assets = [assignment.asset for assignment in assigned_assets_qs]
    total_assets = len(assigned_assets)

    # Tickets for this employee
    tickets = Ticket.objects.filter(employee=user)
    total_tickets = tickets.count()
    pending_tickets = tickets.filter(status='Pending').count()

    context = {
        'assigned_assets': assigned_assets,
        'total_assets': total_assets,
        'tickets': tickets,
        'total_tickets': total_tickets,
        'pending_tickets': pending_tickets,
    }

    return render(request, 'report_employee.html', context)