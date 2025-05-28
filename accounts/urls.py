from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("reset-password/", views.send_reset_password_email, name="send-reset-password"),
    path("reset-password-confirm/<uidb64>/<token>/", views.reset_password_confirm, name="reset_password_confirm"),
    path('register',views.register ,name='register'),
    path('or/factory/',views.orfactrory ,name='orfactrory'),
    path('Shipping/companies/',views.Shipping_companies ,name='Shipping_companies'),

    path('prodects/factrory/se/<str:email>/',views.prodects__factrory__se ,name='prodects__factrory__se'),
    path('or/shipping/<str:email>/',views.or_shipping ,name='or_shipping'),



    path('ordercompleted',views.orderOrdercompleted ,name='orderOrdercompleted'),
    path('ordercolected',views.orderOrdercolected ,name='orderOrdercolected'),
    path('ordertoday',views.orderOrdertoday ,name='orderOrdertoday'),
    path('factory/',views.factory ,name='factory'),
    path('shipping/companies/',views.Shippingcompanies ,name='Shippingcompanies'),
    path('Shipping__companies/',views.Shipping__companies ,name='Shipping__companies'),

    path('Shipping/',views.shipping ,name='shipping'),
    path('order/shipping/<int:id>/',views.order__shipping ,name='order__shipping'),



    path('otp',views.otp ,name='otp'),
    path('order/now/',views.order__now ,name='order__now'),
    path('signupsignin',views.signupsignin ,name='signupsignin'),
    path('signupsignincastomar',views.signupsignincastomar ,name='signupsignincastomar'),

    path('signins',views.signins ,name='signins'),



    path('video',views.video ,name='video'),
    path('deletevideo',views.deletevideo ,name='deletevideo'),
    path('Videoss',views.Videoss ,name='Videoss'),
     path('posts/<int:id>/',views.posts, name='posts' ),
     path('Ordercsv/',views.Ordercsv, name='Ordercsv' ),
     path('prodects_id_user/<int:id>/',views.prodects_id_user, name='prodects_id_user' ),
    path('postvido/',views.postvido ,name='postvido'),
    path('live/<int:id>',views.live ,name='live'),
    path('orderOrderUser/<int:user_id>',views.orderOrderUser ,name='orderOrderUser'),
    path('updateviev/<int:id>',views.updateviev ,name='updateviev'),
    path('deletevideo/<int:id>',views.deletevideo ,name='deletevideo'),
   path('settings/change_password/',auth_views.PasswordChangeView.as_view(template_name='change_password.html') ,name='change_password'),
   path('settings/change_password/done/',auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html') ,name='password_change_done'),
    path('orderOrder/',views.orderOrder ,name='orderOrder'),
    path('updateorder/<int:id>',views.updateorder ,name='updateorder'),
    path('deleteorder/<int:id>',views.deleteorder ,name='deleteorder'),
    path('login',views.signin ,name='signin'),
     path('signup',views.signup ,name='signup'),
     path('signupcastomar',views.signupcastomar ,name='signupcastomar'),
     path('orderuser/<int:id>',views.orderuser ,name='orderuser'),
     path('totals/<int:id>',views.totals ,name='totals'),
     path('orderuser/<int:user_id>/order/<int:order_id>/',views.orderOrderDetails ,name='orderOrderDetails'),
    path('OrderDetails/<int:order_id>/orders/<int:OrderDetails_id>/',views.updateOrderDetailss ,name='updateOrderDetailss'),
    path ('profile',views.profile, name='profile'),
    path ('logout',views.logout, name='logout'),
    path ('prodect_favorite/<uuid:uuid>',views.prodect_favorite, name='prodect_favorite'),
    path ('updatecoun/<int:id>',views.updatecoun, name='updatecoun'),
    path ('fanth/<int:id>',views.fanth, name='fanth'),
    path ('show_prodect_favorite',views.show_prodect_favorite, name='show_prodect_favorite'),
    path ('p',views.p, name='p'),
     path('login',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
     path('password_reset',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),name='password_reset'), 
     path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    # path('password_reset<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    # path('reset_password_complete/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
    #      name="password_reset_complete"),

    # path('reset_password_complete/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
    #      name="password_reset_complete"),

]