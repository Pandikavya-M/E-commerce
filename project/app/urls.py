from django.urls import path
from . import views

urlpatterns = [

    path('remove_wish/<str:wid>',views.remove_wish,name='remove_wish'),
    path('wishlist',views.whishlist,name='wishlist'),
    path('addtowishlist',views.addtowishlist,name='addtowishlist'),


    path('cart',views.add_cart,name='acart'),
    path('view_cart',views.view_cart,name='view_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('close',views.close,name='close'),

    
    path('product-description/<str:cat_name>/<str:prod_name>',views.prod_view,name='prodview'),
    path('Product-view/<str:name>',views.product,name='product'),
    path('Product-view-off/<slug:slug>/', views.productoff, name='productoff'),

    path('shop-by-category',views.category,name='shop'),
    path('signup',views.signup,name='signup'),
    path('login',views.log_pg,name='login'),
    path('logout',views.logout_pg,name='logout'),
    path('about-wallet',views.about,name='about'),
    path('',views.home,name='home'),
]