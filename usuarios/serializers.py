from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Permission
from django.contrib.auth.password_validation import get_default_password_validators
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from utils.messages import Error


class PasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=254)
    password2 = serializers.CharField(max_length=254)

    def validate(self, data):
        self.validate_password(data)
        return data

    def validate_password(self, data):
        password_validators = get_default_password_validators()
        errors = []
        for validator in password_validators:
            try:
                validator.validate(data.get('password1'))
            except (ValidationError, DjangoValidationError) as error:
                errors.append(" ".join(error.messages))
        if errors:
            raise serializers.ValidationError(detail={'errors': errors})

    def validate_password2(self, password2):
        password1 = self.initial_data['password1']
        if password1 and password2:
            if password1 != password2:
                raise serializers.ValidationError(Error.CAMPOS_CONTRASENHA)
        return password2


class UserSerializer(serializers.ModelSerializer):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name']
    table_columns = ['id', 'username', 'email']

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'first_name','last_name',
                  'is_staff', 'is_superuser', 'is_active',
                  'groups', 'user_permissions']


    def get_filters(self, filters):
        fields = self.get_fields()
        fieldnames = fields.keys()
        filter_list = []
        for fieldname in fieldnames:
            if fieldname in filters:

                field = getattr(self, fieldname, False) or fields[fieldname]
                if field:
                    value = field.to_representation(field.initial)
                    filter_list.append(value)
        return filter_list


    def get_table_columns(self):
        table_columns = []
        for field in self.table_columns:
            table_columns.append({"value": field, "text": self.get_fields()[field].label or field.capitalize()})
        return table_columns


class MyRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        user_id = getattr(user, api_settings.USER_ID_FIELD)
        if not isinstance(user_id, int):
            user_id = str(user_id)

        token = cls()
        token[api_settings.USER_ID_CLAIM] = user_id
        token["username"] = user.username
        token["groups"] = list(user.groups.all().values_list('name', flat=True))
        token["is_superuser"] = user.is_superuser
        # token['rules'] = cls.get_user_permissions(user)
        return token

    @staticmethod
    def get_user_permissions(user):
        data = {}
        l1 = 'content_type__app_label'
        l2 = 'codename'

        apps = ["admin", "contenttypes", "notifications", "sessions"]
        queryset = Permission.objects.exclude(content_type__app_label__in=apps)
        if user.is_superuser:
            permissions = queryset.values(l1, l2)
        else:
            permissions = Permission.objects.filter(user=user).values(l1, l2)
        rules = []
        for item in permissions:
            rules.append(item[l2])
        return rules


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    username_field = User.USERNAME_FIELD
    user = None

    @classmethod
    def get_token(cls, user):
        return MyRefreshToken.for_user(user)


    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise ValidationError({
                'detail': 'Usuario o Contraseña incorrecta'
            })

        data = {}
        # https://stackoverflow.com/questions/28583565/str-object-has-no-attribute-decode-python-3-error
        # se debe usar PyJWT==1.7.1
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class AsistenciaSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        user= User.objects.filter(username=attrs['username']).first()

        if user:
            from django.contrib.auth.hashers import check_password
            if check_password(attrs['password'], user.password):
                return True
        #
        raise ValidationError({
            'detail': 'Usuario o Contraseña incorrecta'
        })
