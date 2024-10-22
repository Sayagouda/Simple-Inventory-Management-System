from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from .models import Item
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

User = get_user_model()

class UserSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLogin(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ItemListCreate(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    permission_classes = []  # No authentication required

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        description = request.data.get('description')
        print(name)

        # Validate that both fields are provided
        if not name or not description:
            return Response(
                {'detail': 'Both name and description are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the item without using a serializer
        item = Item.objects.create(name=name, description=description)
        item.save()  # Optionally, you can just call create

        return Response(
            {
                'id': item.id,
                'name': item.name,
                'description': item.description
            },
            status=status.HTTP_201_CREATED
        )

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    permission_classes = []  # No authentication required

    def get(self, request, *args, **kwargs):
        item = self.get_object()
        return Response({
            'id': item.id,
            'name': item.name,
            'description': item.description
        })

    def put(self, request, *args, **kwargs):
        item = self.get_object()
        name = request.data.get('name')
        description = request.data.get('description')

        if name:
            item.name = name
        if description:
            item.description = description

        item.save()
        return Response({
            'id': item.id,
            'name': item.name,
            'description': item.description
        })

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
