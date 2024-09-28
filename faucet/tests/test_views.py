from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
import time

from django.urls import reverse
from faucet_task import settings


class FaucetViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("fund_faucet")
        self.wallet_address = "0xE4BF89Ee624c80fE6b27c7a406a34FDfAAaB7b40"
        settings.rate_limit_tracker = {}

    @patch("faucet.service.FaucetService.fund_account")
    def test_fund_wallet_success(self, mock_fund_account):
        """Test successful funding of wallet"""
        mock_fund_account.return_value = "0xTransactionHash"
        data = {"wallet_address": self.wallet_address}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tx_id": "0xTransactionHash"})

    @patch("faucet.service.FaucetService.fund_account")
    def test_invalid_wallet_address(self, mock_fund_account):
        """Test invalid wallet address"""
        data = {"wallet_address": "invalidAddress"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("wallet_address", response.data)  # Checking for validation errors

    @patch("faucet.service.FaucetService.fund_account")
    def test_rate_limit_exceeded(self, mock_fund_account):
        """Test rate limit exceeded scenario"""
        settings.rate_limit_tracker["127.0.0.1"] = time.time()
        data = {"wallet_address": self.wallet_address}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(
            response.data, {"error": "Rate limit exceeded. Please wait 1 minute."}
        )

    @patch("faucet.service.FaucetService.fund_account")
    def test_server_error_handling(self, mock_fund_account):
        """Test server error handling"""
        mock_fund_account.side_effect = Exception("Some error occurred")
        data = {"wallet_address": self.wallet_address}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {"error": "Some error occurred"})


class FaucetStatsViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("faucet_stats")

    @patch("faucet.service.FaucetService.get_transaction_stats")
    def test_get_faucet_stats(self, mock_get_transaction_stats):
        """Test fetching faucet stats"""
        mock_get_transaction_stats.return_value = (
            10,
            2,
        )  # 10 successful, 2 failed transactions

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "successful_transactions": 10,
                "failed_transactions": 2,
            },
        )
