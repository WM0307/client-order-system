from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Order
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Create your views here.
def dashboard(request):
    total_clients = Client.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="Pending").count()
    completed_orders = Order.objects.filter(status="Completed").count()
    recent_orders = Order.objects.select_related('client').order_by('-created_at')[:5]

    context = {
        'total_clients': total_clients,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/dashboard.html', context)

# CLIENT VIEWS
def client_list(request):
    clients = Client.objects.all().order_by('-created_at')
    return render(request, 'clients/client_list.html', {'clients': clients})

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
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_create(request):
    clients = Client.objects.all()
    statuses = ["Pending", "In Progress", "Completed"]  # 👈 Add this
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
    statuses = ["Pending", "In Progress", "Completed"]  # 👈 Add this
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
