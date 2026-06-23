from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Tüm ürünlerin listelendiği ana sayfa
    path('', views.product_list, name='product_list'),
    
    # Belirli bir kategoriye göre ürünleri filtrelemek için (slug parametresi eklendi)
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    
    # Sepete belirli bir ürünü eklemek için (product_id parametresi eklendi)
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    
    # Sepet detayı
    path('cart/', views.cart_detail, name='cart_detail'),
    
    # Sipariş oluşturma
    path('order/create/', views.order_create, name='order_create'),
    
    # Shopier ödeme geri dönüşü (callback)
    path('shopier-callback/', views.shopier_callback, name='shopier_callback'),
]