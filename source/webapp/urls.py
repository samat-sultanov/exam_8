from django.urls import path

from webapp.views.products import IndexView, ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView

app_name = "webapp"

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('products/add/', ProductCreateView.as_view(), name="create_product"),
    path('products/<int:pk>/', ProductDetailView.as_view(), name="product_view"),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name="update_product"),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name="delete_product"),
]
