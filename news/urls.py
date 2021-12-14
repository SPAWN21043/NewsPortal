from django.urls import path
from .views import PostList, PostDetail, SearchList, AddList, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='product_detail'),
    path('search', SearchList.as_view()),
    path('add', AddList.as_view()),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='product_delete'),
]