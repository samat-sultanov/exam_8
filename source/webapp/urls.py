from django.urls import path

from webapp.views import IndexView, ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView
from webapp.views import ReviewCreateView, ReviewUpdateView, ReviewDeleteView, NotModeratedReview

app_name = "webapp"

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('products/add/', ProductCreateView.as_view(), name="create_product"),
    path('products/<int:pk>/', ProductDetailView.as_view(), name="product_view"),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name="update_product"),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name="delete_product"),
    path('products/<int:pk>/review/add/', ReviewCreateView.as_view(), name="review_create"),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name="update_review"),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name="delete_review"),
    path('reviews/no-moderation/', NotModeratedReview.as_view(), name="not_moderated_reviews"),
]
