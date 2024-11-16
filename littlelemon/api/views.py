from rest_framework import generics, permissions,viewsets,status,filters
from .models import *
from .serializers import *
from django.contrib.auth.models import Group ,User
from rest_framework.response import Response
from .permissions import *
from django.utils import timezone
class MenuItemCRUD(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrRead]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['category']
    def get_queryset(self):
        queryset = MenuItem.objects.all()
        price = self.request.query_params.get('price',None)
        name = self.request.query_params.get('name',None)
        categories = self.request.query_params.getlist('category',None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        if price is not None:
            queryset = queryset.filter(price__lt=price)

        if categories:
            queryset = queryset.filter(category__slug__in = categories).distinct()
        return queryset
        

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Reservation.objects.all()
        else:
            queryset = Reservation.objects.filter(user=self.request.user)
            
        return queryset
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoriesCRUD(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrRead]
    lookup_field = 'slug'

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        # Staff can see all orders; users see only their own
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        menuitem = MenuItem.objects.get(pk=data.get('menuitem'))

        cart_item = Cart.objects.filter(user=user, menuitem=menuitem).first()
        if cart_item:
            cart_item.quantity += int(data['quantity'])
            cart_item.total_price = cart_item.unit_price * cart_item.quantity
            cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        Cart.objects.filter(user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ManagerGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsManager]

    def list(self, request):
        group = Group.objects.get(name='managers')
        users = group.user_set.all()
        users_data = [{"id": user.id, "username": user.username} for user in users]
        return Response(users_data, status=status.HTTP_200_OK)

    def create(self, request):
        user_id = request.data.get("user_id")
        try:
            user = User.objects.get(id=user_id)
            manager_group = Group.objects.get(name='managers')
            manager_group.user_set.add(user)
            return Response({"detail": "User added to manager group"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            manager_group = Group.objects.get(name='managers')
            manager_group.user_set.remove(user)
            return Response({"detail": "User removed from manager group"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class DeliveryCrewGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsManager]

    def list(self, request):
        group = Group.objects.get(name='Delivery Crew')
        users = group.user_set.all()
        users_data = [{"id": user.id, "username": user.username} for user in users]
        return Response(users_data, status=status.HTTP_200_OK)

    def create(self, request):
        user_id = request.data.get("user_id")
        try:
            user = User.objects.get(id=user_id)
            delivery_group = Group.objects.get(name='Delivery Crew')
            delivery_group.user_set.add(user)
            return Response({"detail": "User added to delivery crew group"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            delivery_group = Group.objects.get(name='Delivery Crew')
            delivery_group.user_set.remove(user)
            return Response({"detail": "User removed from delivery crew group"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)