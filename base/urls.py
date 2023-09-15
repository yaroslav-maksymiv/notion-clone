from django.urls import path
from rest_framework import routers

from .views import (
    PageListView,
    PageSingleView,
    PageFavouriteListView,
    add_page_to_favourite,
    change_page_title,
    create_page,
    change_page_icon,
    get_page_children,
    get_first_page_id,
    PageSearchView,
    PageElementViewSet, 
    PageDeleteView,
    set_page_full_width,
    set_page_locked
)

urlpatterns = [
    path('pages/', PageListView.as_view(), name='pages'),
    path('pages/first-id/', get_first_page_id, name='pages-first-id'),
    path('pages/create/', create_page, name='page-create'),
    path('pages/delete/<int:pk>/', PageDeleteView.as_view(), name='page-delete'),
    path('pages/change-title/<int:pk>/', change_page_title, name='change-title'),
    path('pages/change-icon/<int:pk>/', change_page_icon, name='change-icon'),
    path('pages/locked/<int:pk>/', set_page_locked, name='set-is-locked'),
    path('pages/full-width/<int:pk>/', set_page_full_width, name='sete-full-width'),
    path('pages/favourite/', PageFavouriteListView.as_view(), name='pages-favourite'),
    
    path('page/<int:pk>/', PageSingleView.as_view(), name='page'),
    path('page/<int:pk>/toggle-favourite/', add_page_to_favourite, name='page-toggle-favourite'),
    path('page/<int:pk>/children/', get_page_children, name='page-children'),

    path('search/', PageSearchView.as_view(), name='page-text-search'),
] 

router = routers.DefaultRouter()
router.register(r'page-elements', PageElementViewSet, basename='page-elements')

urlpatterns += router.urls