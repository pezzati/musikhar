from financial.models import BusinessPackage
from mediafiles.serializers import MediaFileSerializer
from musikhar.abstractions.serializers import MySerializer


class BusinessPackageSerializer(MySerializer):
    icon = MediaFileSerializer(many=False, required=False)

    class Meta:
        model = BusinessPackage
        fields = ('name', 'price', 'icon', 'serial_number')
