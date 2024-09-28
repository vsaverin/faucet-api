import datetime

from .models import Transaction


class FaucetRepository:
    def create_transaction(
        self, wallet_address: str, status: str, tx_id: str | None = None
    ) -> Transaction:
        return Transaction.objects.create(
            wallet_address=wallet_address, tx_id=tx_id, status=status
        )

    def get_transaction_stats(self) -> tuple[int, int]:
        one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        successful_transactions = Transaction.objects.filter(
            status="success", timestamp__gte=one_day_ago
        ).count()
        failed_transactions = Transaction.objects.filter(
            status="failed", timestamp__gte=one_day_ago
        ).count()
        return successful_transactions, failed_transactions
