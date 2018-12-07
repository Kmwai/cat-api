from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/cats/<int:pk>', views.get_delete_update_cat, name='get_delete_update_cat'),
    path('api/v1/cats/', views.get_post_cats, name='get_post_cats'),
    path('api/v1/schema_view', views.schema_view)
]