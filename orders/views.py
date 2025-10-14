from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Order
from django.contrib.auth.decorators import login_required

# Create your views here.
# CLIENT VIEWS
def client_list(request):
    clients = Client.objects.all().order_by('-created_at')
    return render(request, 'orders/client_list.html', {'clients': clients})

def client_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company = request.POST.get('company')
        Client.objects.create(name=name, email=email, phone=phone, company=company)
        return redirect('client_list')
    return render(request, 'orders/client_form.html')

def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.company = request.POST.get('company')
        client.save()
        return redirect('client_list')
    return render(request, 'orders/client_form.html', {'client': client})

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('client_list')