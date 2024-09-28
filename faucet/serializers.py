from rest_framework import serializers

from web3 import Web3


class FaucetSerializer(serializers.Serializer):
    wallet_address = serializers.CharField()

    def validate_wallet_address(self, value):
        web3 = Web3()
        if not web3.is_address(value):
            raise serializers.ValidationError("Invalid wallet address")
        return value
