from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Get the CustomUser model we created earlier
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    This handles creating a new user account.
    """
    # Password fields - write_only means they won't be returned in responses
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]  # Uses Django's built-in password validation
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'monthly_income', 'currency')
    
    def validate(self, attrs):
        """
        Check that the two password entries match.
        This is called automatically before creating the user.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        """
        Create and return a new user with encrypted password.
        We remove password2 since it's only used for validation.
        """
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user information.
    Used when sending user data to the frontend.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'monthly_income', 'currency', 'created_at')
        read_only_fields = ('id', 'created_at')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    Users can update their username, monthly income, and currency.
    """
    class Meta:
        model = User
        fields = ('username', 'monthly_income', 'currency')