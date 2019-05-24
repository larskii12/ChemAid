from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^ChemAid/admin/home/items$', views.items, name="items"),
    url(r'^ChemAid/admin/home/categories$', views.categories, name="categories"),
    url(r'^ChemAid/admin/home/items/delete/(\d+)/$', views.delete_item, name="delete_item"),
    url(r'^ChemAid/admin/home/items/edit/(\d+)/$', views.edit_item, name="edit_item"),
    url(r'^ChemAid/admin/home/categories/edit/(\d+)/$', views.edit_category, name="edit_category"),
    url(r'^ChemAid/admin/home/categories/delete/(\d+)/$', views.delete_category, name="delete_category"),
    url(r'^ChemAid/admin/home/borrowed$', views.approveborrow, name="approve"),
    url(r'^ChemAid/admin/home/request$', views.request, name="request"),
    url(r'^ChemAid/admin/home/return$', views.returned, name="return"),
    url(r'^ChemAid/home/borrow$',views.options, name="options"),
    url(r'^ChemAid/home/borrow/(\d+)/$', views.borrow, name="borrow"),
    url(r'^ChemAid/admin/home/cancel/(\d+)/$', views.cancel, name="cancel"), 
]
if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)