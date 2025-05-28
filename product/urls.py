from django.urls import path
from . import views



urlpatterns =[
    path('', views.prodects, name='prodects'),
    path('cat', views.cat, name='cat'),
    path('cattger/', views.cattger, name='cattger'),
    path('prodects/factrory/', views.prodectsfactrory, name='prodectsfactrory'),
    path('add/prodect/factory/', views.addprodectfactory, name='addprodectfactory'),
    path('addprodectfactorygx', views.addprodectfactorygx, name='addprodectfactorygx'),



    path('gx', views.gx, name='gx'),
    path('gxd', views.gxd, name='gxd'),
    path('gxproduct/<int:id>', views.gxproduct,name='gxproduct'),
    path('update/is_active/<int:id>', views.update_is_active,name='update_is_active'),

    path('update/factory/<int:id>', views.updatefactory,name='updatefactory'),
    path('delete/factory/<int:id>', views.deletefactory,name='deletefactory'),


    path('profintion/<int:id>', views.profintion,name='profintion'),
    path('ma/', views.mas,name='mas'),
    path('masd/', views.masd,name='masd'),

    path('deleteGx/<int:id>', views.deleteGx,name='deleteGx'),
    path('updateGx/<int:id>', views.updateGx,name='updateGx'),

    path('deletemasd/<int:id>', views.deletemasd,name='deletemasd'),
    path('updatemasd/<int:id>', views.updatemasd,name='updatemasd'),

    path('deleteGxqu/<int:id>/<int:ids>/', views.deleteGxqu,name='deleteGxqu'),
    path('updateGxqu/<int:id>/<int:ids>/', views.updateGxqu,name='updateGxqu'),
    path('dgxr/<int:id>', views.dgxr,name='dgxr'),
    path('Gxqu/<int:id>', views.gxqu,name='Gxqu'),
    path('<uuid:uuid>', views.prodect,name='prodect'),
    path('addimgs/<int:id>', views.addimgs,name='addimgs'),
    path('deleteimg/<int:id>/<int:idimg>/', views.deleteimg,name='deleteimg'),
    path('updateimg/<int:id>/<int:idimg>/', views.updateimg,name='updateimg'),
    path('delete/', views.delete_selected_products, name='delete_selected_products'),
    path('dimgs/<int:id>', views.dimgs,name='dimgs'),
    path('search', views.search,name='search'),
    path('index', views.index,name='index'),
    path('category', views.category,name='category'),
    path('addindex', views.addindex,name='addindex'),
    path('m', views.t404 ,name='t404'),
    path('update/<int:id>', views.update,name='updateb'),
    path('deletecattger/<int:id>', views.deletecattger,name='deletecattger'),
    path('updatecattger/<int:id>', views.updatecattger,name='updatecattger'),
    path('delete/<int:id>',views.delete ,name='deleteb'),
    path('passs',views.passs ,name='passs'),
    
]