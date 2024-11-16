from django.urls import path ,include
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register(r'menu-items',MenuItemCRUD,basename='menu-items')
router.register(r'categories',CategoriesCRUD,basename='categories')
router.register(r'reservations',ReservationViewSet,basename='reservations')
router.register(r'orders',OrderViewSet,basename='orders')
router.register(r'cart', CartViewSet, basename='cart')
urlpatterns = [
    path('',include(router.urls)),
    path('groups/managers/users/', ManagerGroupViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='manager-group-list'),

    path('groups/managers/users/<int:pk>/', ManagerGroupViewSet.as_view({
        'delete': 'destroy'
    }), name='manager-group-delete'),

    path('groups/delivery-crew/users/', DeliveryCrewGroupViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='delivery-crew-list'),
    path('groups/delivery-crew/users/<int:pk>/', DeliveryCrewGroupViewSet.as_view({
        'delete': 'destroy'
    }), name='delivery-crew-delete'),
    path('api-auth-token/',obtain_auth_token),
]

