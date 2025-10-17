import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
@login_required
def dashboard(request):
    total_clients = Client.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="Pending").count()
    inprogress_orders = Order.objects.filter(status="In Progress").count()  
    completed_orders = Order.objects.filter(status="Completed").count()
    recent_orders = Order.objects.select_related('client').order_by('-created_at')[:5]

    context = {
        'total_clients': total_clients,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'inprogress_orders': inprogress_orders,  
        'completed_orders': completed_orders,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/dashboard.html', context)

# CLIENT VIEWS
def client_list(request):
    clients = Client.objects.all().order_by('id')

    # Pagination — show 10 clients per page
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'clients/client_list.html', context)

def client_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company = request.POST.get('company')
        Client.objects.create(name=name, email=email, phone=phone, company=company)
        return redirect('client_list')
    return render(request, 'clients/client_form.html')

def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.company = request.POST.get('company')
        client.save()
        return redirect('client_list')
    return render(request, 'clients/client_form.html', {'client': client})

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('client_list')

# ORDER VIEWS
def order_list(request):
    orders = Order.objects.select_related('client').order_by('-created_at')

    paginator = Paginator(orders, 10)  # show 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'orders/order_list.html', context)

def order_create(request):
    clients = Client.objects.all()
    statuses = ["Pending", "In Progress", "Completed"]  
    if request.method == 'POST':
        client_id = request.POST.get('client')
        title = request.POST.get('title')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        status = request.POST.get('status')
        client = Client.objects.get(pk=client_id)
        Order.objects.create(
            client=client,
            title=title,
            description=description,
            amount=amount,
            status=status,
            created_by=request.user if request.user.is_authenticated else None
        )
        return redirect('order_list')
    return render(request, 'orders/order_form.html', {'clients': clients, 'statuses': statuses})

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    clients = Client.objects.all()
    statuses = ["Pending", "In Progress", "Completed"]  
    if request.method == 'POST':
        order.client_id = request.POST.get('client')
        order.title = request.POST.get('title')
        order.description = request.POST.get('description')
        order.amount = request.POST.get('amount')
        order.status = request.POST.get('status')
        order.save()
        return redirect('order_list')
    return render(request, 'orders/order_form.html', {'order': order, 'clients': clients, 'statuses': statuses})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('order_list')

def export_clients_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Company', 'Created At'])

    for client in Client.objects.all():
        writer.writerow([
            client.id,
            client.name,
            client.email,
            client.phone,
            client.company,
            client.created_at.strftime('%Y-%m-%d %H:%M'),
        ])

    return response

def export_orders_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Client', 'Title', 'Status', 'Amount', 'Created By', 'Created At'])

    for order in Order.objects.all():
        writer.writerow([
            order.id,
            order.client.name,
            order.title,
            order.status,
            order.amount,
            order.created_by.username if order.created_by else '',
            order.created_at.strftime('%Y-%m-%d %H:%M'),
        ])

    return response