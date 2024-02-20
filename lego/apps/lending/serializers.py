from datetime import timedelta
from rest_framework import serializers
from lego.apps.files.fields import ImageField


from lego.apps.lending.models import LendableObject, LendingInstance
from lego.apps.users.serializers.users import PublicUserSerializer


class LendableObjectSerializer(serializers.ModelSerializer):
    image = ImageField(required=False, options={"height": 500})
    class Meta:
        model = LendableObject
        fields = "__all__"


class LendingInstanceSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = LendingInstance
        fields = "__all__"

    def validate(self, data):
        # Check if 'lendable_object', 'start_date', and 'end_date' are provided in the data.
        lendable_object = data.get("lendable_object")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # Ensure all necessary fields are present
        if lendable_object and start_date and end_date:
            user = self.context["request"].user
            # Check if the user is in one of the responsible groups
            if not user.abakus_groups.filter(
                id__in=lendable_object.responsible_groups.values_list("id", flat=True)
            ).exists():
                # Calculate the lending period and compare
                lending_period = end_date - start_date
                max_lending_period = timedelta(days=lendable_object.max_lending_period)
                if lending_period > max_lending_period:
                    raise serializers.ValidationError(
                        "Lending period exceeds maximum allowed duration"
                    )

        return data
