from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TicketForm
from .models import Ticket
from asset_assignment.models import AssetAssignment
from django.contrib.admin.views.decorators import staff_member_required



@login_required
def raise_ticket(request):

    # Get assigned asset IDs
    assigned_assets = AssetAssignment.objects.filter(
        employee=request.user,
        is_returned=False
    ).values_list('asset', flat=True)

    form = TicketForm(request.POST or None)

    # Limit asset dropdown to assigned assets only
    form.fields['asset'].queryset = form.fields['asset'].queryset.filter(
        id__in=assigned_assets
    )

    if request.method == 'POST' and form.is_valid():

        selected_asset = form.cleaned_data['asset']

        # ✅ Optional: Prevent duplicate open ticket
        if Ticket.objects.filter(
            employee=request.user,
            asset=selected_asset,
            status__in=['Pending', 'In Progress']
        ).exists():

            messages.error(request, "A ticket is already open for this asset.")
            return redirect('ticket_list')

        ticket = form.save(commit=False)
        ticket.employee = request.user
        ticket.save()

        messages.success(request, "Ticket raised successfully!")
        return redirect('ticket_list')  # 👈 better UX than dashboard

    return render(request, 'raise_ticket.html', {
        'form': form
    })


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(
        employee=request.user
    ).order_by('-created_at')

    return render(request, 'ticket_list.html', {
        'tickets': tickets
    })






@staff_member_required
def admin_ticket_list(request):
    tickets = Ticket.objects.all().order_by('-created_at')

    return render(request, 'admin_ticket_list.html', {
        'tickets': tickets
    })


@staff_member_required
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        new_status = request.POST.get('status')
        ticket.status = new_status
        ticket.save()

        messages.success(request, "Ticket status updated successfully!")

    return redirect('admin_ticket_list')