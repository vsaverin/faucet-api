import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample

from faucet_task import settings

from .service import FaucetService
from .serializers import FaucetSerializer


class FaucetView(APIView):
    serializer = FaucetSerializer
    service = FaucetService()

    @extend_schema(
        description=(
            "Fund the provided wallet address with 0.0001"
            " ETH. Rate-limited to 1 request per minute per IP."
        ),
        request=FaucetSerializer,
        responses={
            200: OpenApiExample(
                "Success Response",
                value={"tx_id": "0xTransactionHash"},
                response_only=True,
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        wallet_address = serializer.validated_data["wallet_address"]
        source_ip = request.META.get("REMOTE_ADDR")

        if source_ip in settings.rate_limit_tracker:
            last_request_time = settings.rate_limit_tracker[source_ip]
            if time.time() - last_request_time < 60:
                return Response(
                    {"error": "Rate limit exceeded. Please wait 1 minute."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )

        try:
            tx_id = self.service.fund_account(wallet_address)
            settings.rate_limit_tracker[source_ip] = time.time()
            return Response({"tx_id": tx_id})
        except Exception as e:
            self.service.create_error_transaction(wallet_address, str(e))
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FaucetStatsView(APIView):
    service = FaucetService()

    @extend_schema(
        description=(
            "Get the statistics for the faucet over the past 24 hours. "
            "Returns the count of successful and failed transactions."
        ),
        responses={
            200: OpenApiExample(
                "Stats Response",
                value={"successful_transactions": 123, "failed_transactions": 1},
                response_only=True,
            ),
        },
    )
    def get(self, request):
        success, failed = self.service.get_transaction_stats()
        return Response(
            {
                "successful_transactions": success,
                "failed_transactions": failed,
            }
        )
