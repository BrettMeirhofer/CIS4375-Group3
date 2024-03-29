from django.urls import path
from django.urls import path, include
from . import models
from rest_framework import routers, serializers, viewsets
from . import views


# Serializers define the API representation.
class ProductStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ProductStatus
        fields = ['status_name']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Product
        fields = ['product_name']


# ViewSets define the view behavior.
class ProductStatusViewSet(viewsets.ModelViewSet):
    queryset = models.ProductStatus.objects.all()
    serializer_class = ProductStatusSerializer


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'productstatus', ProductStatusViewSet)
router.register(r'product', ProductViewSet)


urlpatterns = [
    path('delete_rows/', views.delete_rows, name='delete_rows'),
    path('jeans/', include(router.urls)),
    path('', views.index, name='index'),
    path('send_email', views.promo_email_page, name='send_email'),
    path('dd', views.dict3, name='datadictionary'),
    path('create', views.generate_create, name='create'),
    path('altar', views.generate_alter, name='altar'),
    path('drop', views.generate_drop, name='drop'),
    path('delete', views.generate_delete, name='delete'),
    path('sql', views.generate_sql_all, name='sqlall'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('listall/<table>/', views.view_products_list, name='listall'),
    path('delete_row/<table>/<int:id>/', views.delete_single, name='delete_row'),
    path('create_row/<table>/', views.create_single, name='create_row'),
    path('edit_row/<table>/<int:id>/', views.edit_single, name='edit_row'),
    path('graph', views.top5_cust, name='graph'),
    path('graph2', views.top5_promos, name='graph2'),
    path('graph3', views.uniq_cust_month, name='graph3'),
    path('preview_promo/', views.preview_promo, name='preview_promo'),
    path('report/', views.report, name='report'),
    path('top_promos/', views.top_promos, name='top_promos'),
    path('top_customers/', views.top_customers, name='top_customers'), 
    path('print_promo/<int:id>/', views.print_promo, name='print_promo'),
    path('print_report/<int:row_id>/<start_date>/<end_date>/', views.html_report, name='print_report'),
    path('get_product_promo_prices/<int:product_id>/<int:promo_id>/', views.get_product_promo_prices, name='get_product_promo_prices'),
    path('get_promo_products/<int:row_id>/', views.get_promo_products, name='get_promo_products'),
]