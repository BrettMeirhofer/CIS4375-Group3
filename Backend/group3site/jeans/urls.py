from django.urls import path
from django.urls import path, include
from . import models
from rest_framework import routers, serializers, viewsets
from . import views

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ProductStatus
        fields = ['status_name']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.ProductStatus.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('jeans/', include(router.urls)),
    path('', views.index, name='index'),
    path('dd', views.dict3, name='datadictionary'),
    path('create', views.generate_create, name='create'),
    path('drop', views.generate_drop, name='drop'),
    path('delete', views.generate_delete, name='delete'),
    path('sql', views.generate_sql_all, name='sqlall'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]