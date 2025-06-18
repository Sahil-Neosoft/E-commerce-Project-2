from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('product/', include('apps.product.urls'), name='product'),
    path('cart/', include('apps.cart.urls'), name='cart'),
    path('checkout/', include('apps.order.urls'), name='checkout'),
]
# serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

