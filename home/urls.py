from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('upload_file',views.upload_file,name='upload_file'),
    path('search',views.search,name='search'),
    path('to_edit',views.to_edit,name='to_edit'),
    path('edit',views.edit,name='edit'),
    path('delete',views.delete,name='delete')
]