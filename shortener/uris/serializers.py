from rest_framework import serializers
from rest_framework.exceptions import APIException


from uris.models import Link
from uris.models import SHORT_CODE_LEN


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["target_url", "short_code", "short_url"]
        read_only_fields = ["short_url"]
    
    target_url = serializers.URLField(write_only=True) 
    short_code = serializers.CharField(
        max_length=SHORT_CODE_LEN, write_only=True, default="" 
    )
    short_url = serializers.SerializerMethodField()

    def validate_short_code(self, value: str) -> str:
        if not value:
            short_code = Link.generate_short_code()
        else:
            short_code = value

        if Link.objects.filter(short_code=short_code).exists():
            if value:
                raise serializers.ValidationError("Short Code is already taken!")
            else:
                i = 0
                while not Link.objects.filter(short_code=short_code).exists():
                    i += 1
                    short_code = Link.generate_short_code()
                    if i == 20:
                        raise APIException("Unable to generate short code at the moment!")

        return short_code 
    
    def get_short_url(self, obj: Link) -> str:
        request = self.context["request"]

        return request.build_absolute_uri(obj.short_path)

