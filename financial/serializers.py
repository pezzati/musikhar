from financial.models import BusinessPackage, CoinTransaction, BazzarTransaction, GiftCode
from mediafiles.serializers import MediaFileSerializer
from musikhar.abstractions.serializers import MySerializer


class BusinessPackageSerializer(MySerializer):

    class Meta:
        model = BusinessPackage
        fields = ('name', 'price', 'icon', 'serial_number', 'package_type')


class BazzarTransactionSerializer(MySerializer):

    class Meta:
        model = BazzarTransaction
        fields = ('serial_number', 'ref_id', 'state')


class CoinTransactionSerializer(MySerializer):

    class Meta:
        model = CoinTransaction
        fields = ('serial_number', 'date', 'applied', 'coins', 'amount')


class GiftCodeSerializer(MySerializer):

    class Meta:
        model = GiftCode
        fields = ('name', 'capacity', 'deadline')
