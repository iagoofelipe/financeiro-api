from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Wallet, WalletLimitChange

class WalletCreateTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='wallet-create-user',
			password='test-password',
		)
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)

	def test_create_card_wallet_with_valid_limit(self):
		response = self.client.post(
			'/wallets/',
			{
				'name': 'Cartao principal',
				'cardType': True,
				'cardDateReference': '2026-10-01',
				'cardLimit': 2500.0,
			},
			format='json',
		)

		self.assertEqual(response.status_code, 201)
		wallet = Wallet.objects.get(name='Cartao principal')
		limit_change = WalletLimitChange.objects.get(wallet=wallet)
		self.assertEqual(wallet.user, self.user)
		self.assertTrue(wallet.cardType)
		self.assertEqual(limit_change.date.isoformat(), '2026-10-01')
		self.assertEqual(limit_change.limit, 2500.0)
		self.assertEqual(response.json()['cardLimit'], 2500.0)

	def test_create_card_wallet_requires_date_and_limit(self):
		response = self.client.post(
			'/wallets/',
			{'name': 'Cartao incompleto', 'cardType': True},
			format='json',
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(Wallet.objects.count(), 0)
		self.assertEqual(WalletLimitChange.objects.count(), 0)

	def test_invalid_limit_does_not_create_wallet(self):
		response = self.client.post(
			'/wallets/',
			{
				'name': 'Cartao invalido',
				'cardType': True,
				'cardDateReference': '2026-13-01',
				'cardLimit': 'invalido',
			},
			format='json',
		)

		self.assertEqual(response.status_code, 400)
		self.assertIn('date', response.json())
		self.assertIn('limit', response.json())
		self.assertEqual(Wallet.objects.count(), 0)
		self.assertEqual(WalletLimitChange.objects.count(), 0)
