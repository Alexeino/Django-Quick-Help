from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(ModelSerializer):
    password_confirm = serializers.CharField(max_length=50,write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','email','password','password_confirm','first_name','last_name']
        extra_kwargs = {
            'password': {'write_only': True}
                    }
    
    def create(self, validated_data): # Triggered by save() method, before saving an instance.
        print("CREATE METHOD ")
        password = validated_data.get('password',None)
        print(validated_data)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance

    def save(self, **kwargs): #Triggered by serializer.save() after APIView post method
        print("SAVE METHOD MODEL SERIALIZER")
        self.validated_data.pop('password_confirm')
        return super().save(**kwargs)