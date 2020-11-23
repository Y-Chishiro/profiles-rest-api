from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile  # これでModelSerializerのポインタが設定される
        fields = ('id', 'email', 'name', 'password')  # このままではpasswordが閲覧可能で危ない
        extra_kwargs = {
            'password': {
                'write_only': True,  # 書き込みオンリーにする
                'style': {'input_type': 'password'}  # これで入力したパスワードが隠して表示される？
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        """デフォルトのupdate()はフィールドを自動更新するだけなので、
        パスワードがハッシュ化されない。そのため、オーバーライドする"""
        if 'passwowrd' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)
