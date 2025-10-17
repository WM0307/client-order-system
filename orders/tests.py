from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Client as ClientModel, Order

# =====================
#  MODEL TESTS
# =====================
class ClientModelTest(TestCase):
    def test_create_client(self):
        client = ClientModel.objects.create(name="John Doe", email="john@example.com", phone="123456")
        self.assertEqual(client.name, "John Doe")
        self.assertEqual(ClientModel.objects.count(), 1)


class OrderModelTest(TestCase):
    def setUp(self):
        self.client_obj = ClientModel.objects.create(name="Alice", email="alice@example.com", phone="987654")

    def test_create_order(self):
        order = Order.objects.create(
            client=self.client_obj,
            title="Test Order",
            status="Pending",
            amount=100.00,
        )
        self.assertEqual(order.title, "Test Order")
        self.assertEqual(order.client.name, "Alice")
        self.assertEqual(order.status, "Pending")
        self.assertEqual(Order.objects.count(), 1)


# =====================
#  VIEW TESTS
# =====================
class ViewTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client = Client()
        self.client.login(username="testuser", password="12345")

        # Create test clients
        self.client1 = ClientModel.objects.create(name="Client A", email="a@mail.com", phone="111", company="ABC Co")
        self.client2 = ClientModel.objects.create(name="Client B", email="b@mail.com", phone="222", company="XYZ Co")

        # Create test orders
        self.order1 = Order.objects.create(
            client=self.client1,
            title="Test Order 1",
            description="First order",
            amount=100,
            status="Pending",
            created_by=self.user
        )
        self.order2 = Order.objects.create(
            client=self.client2,
            title="Test Order 2",
            description="Second order",
            amount=200,
            status="Completed",
            created_by=self.user
        )

    def test_order_list_view(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')
        self.assertContains(response, "Test Order 1")
        self.assertContains(response, "Test Order 2")

    def test_client_list_view(self):
        response = self.client.get(reverse('client_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/client_list.html')
        self.assertContains(response, "Client A")
        self.assertContains(response, "Client B")

    def test_export_clients_csv(self):
        response = self.client.get(reverse('export_clients_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Client A', content)
        self.assertIn('Client B', content)

    def test_export_orders_csv(self):
        response = self.client.get(reverse('export_orders_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Test Order 1', content)
        self.assertIn('Test Order 2', content)
