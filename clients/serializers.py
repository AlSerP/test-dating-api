from django.contrib.auth import get_user_model
from rest_framework import serializers
import PIL.Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from dating_api.settings import STATIC_ROOT


class UserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        if validated_data.get('avatar', None):
            origin_image = PilImage.open(validated_data.get('avatar', None))
            new_image = self.__image_prep(origin_image)
            validated_data['avatar'] = InMemoryUploadedFile(
                self.__image_prep(origin_image),
                None,
                'avatar.png',
                'image/png',
                new_image.tell,
                None
            )
            origin_image.close()

        User = self.Meta.model
        user = User.objects.create_user(**validated_data)

        return user

    def __image_prep(self, image):
        """
        Resizing image and adding watermark
        """
        size = self.Meta.model.AVATAR_SIZE

        resized_image = image.resize(size)
        watermark_image = PilImage.open(str(STATIC_ROOT) + '/images/watermark.png')

        resized_image = resized_image.convert("RGBA")
        watermark_image = watermark_image.convert("RGBA")
        
        result_image = PilImage.alpha_composite(resized_image, watermark_image)
        watermark_image.close()

        buffer = BytesIO()
        result_image.save(fp=buffer, format='PNG')

        return ContentFile(buffer.getvalue())
        

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'avatar', 'is_male', 'password', 'long', 'lat')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }
