from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group,User

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        queryset = Category.objects.all(),
        slug_field = 'slug',
        )
    
    class Meta:
        model = MenuItem
        fields = [ 'name', 'price', 'category', 'image', 'description','id']

class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())  # Expecting menuitem as an ID

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['user', 'unit_price', 'total_price']

    def create(self, validated_data):
        user = self.context['request'].user
        menuitem = validated_data['menuitem']
        quantity = validated_data['quantity']
        
        unit_price = menuitem.price
        total_price = unit_price * quantity


        cart_item = Cart.objects.create(
            user=user,
            menuitem=menuitem,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price
        )
        return cart_item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class ReservationSerializer(serializers.ModelSerializer):
    username= serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Reservation
        fields = ['id','party_size','notes','username','time']
        
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source="menu_item.name",read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    username = serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = Order
        fields = ['username','id', 'address', 'phone_number', 'total_price', 'items']

    def create(self, validated_data):
        request = self.context.get('request')
        items_data = request.data.get('items')
        
        # Create the order first without items
        order = Order.objects.create(
            user=request.user,
            address=validated_data.get('address', ''),
            phone_number=validated_data.get('phone_number', ''),
            total_price=0
        )
        
        # Initialize total price to accumulate the prices of items
        total_price = 0

        # Create each OrderItem and associate it with the order
        for item_data in items_data:
            menu_item_id = item_data.get('menu_item')
            quantity = item_data.get('quantity', 1)

            # Retrieve the MenuItem instance
            menu_item = MenuItem.objects.get(id=menu_item_id)
            price = menu_item.price * quantity

            # Create the OrderItem
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                price=price
            )

            # Accumulate total price
            total_price += price

        # Update the order's total price after all items are added
        order.total_price = total_price
        order.save()

        return order

    def to_representation(self, instance):
        """Custom representation to include items data."""
        representation = super().to_representation(instance)
        # Fetch the related OrderItems and serialize them using OrderItemSerializer
        items = OrderItem.objects.filter(order=instance)
        representation['items'] = OrderItemSerializer(items, many=True).data
        return representation


    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']
class GroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True,read_only=True,source='user_set')
    class Meta:
        model = Group
        fields = ['name','users']
