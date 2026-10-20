from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Registry
from ..wallet.models import Wallet


class RegistryCreateTests(TestCase):
    def test_create_uses_pending_status_when_omitted(self):
        user = get_user_model().objects.create_user(username='registry-default-status', password='test-password')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(
            '/registry/create',
            {
                'title': 'Registro sem status',
                'value': 12.0,
                'occurrence': '2026-10-20T09:30:00',
                'reference': '2026-10',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        registry = Registry.objects.get(title='Registro sem status')
        self.assertEqual(registry.status, 'PENDING')

    def test_create_assigns_authenticated_user(self):
        user = get_user_model().objects.create_user(username='registry-user', password='test-password')
        wallet = Wallet.objects.create(name='Carteira de teste', user=user)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(
            '/registry/create',
            {
                'title': 'Conta de teste',
                'value': 25.5,
                'occurrence': '2026-10-20T09:30:00',
                'reference': '2026-10',
                'status': 'ACCOUNTED',
                'walletId': wallet.id,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        registry = Registry.objects.get(title='Conta de teste')
        self.assertEqual(registry.user, user)
        self.assertEqual(registry.wallet, wallet)
        self.assertEqual(registry.status, 'ACCOUNTED')
        self.assertEqual(response.json()['walletId'], wallet.id)
        self.assertEqual(response.json()['status'], 'ACCOUNTED')

    def test_create_rejects_wallet_owned_by_another_user(self):
        user = get_user_model().objects.create_user(username='registry-user', password='test-password')
        other_user = get_user_model().objects.create_user(username='other-user', password='test-password')
        wallet = Wallet.objects.create(name='Carteira alheia', user=other_user)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(
            '/registry/create',
            {
                'title': 'Conta inválida',
                'value': 25.5,
                'occurrence': '2026-10-20T09:30:00',
                'reference': '2026-10',
                'walletId': wallet.id,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('walletId', response.json()['detail'])
        self.assertFalse(Registry.objects.filter(title='Conta inválida').exists())
