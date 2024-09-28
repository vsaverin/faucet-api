from django.db import models


class Transaction(models.Model):
    wallet_address = models.CharField(max_length=255)
    tx_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
