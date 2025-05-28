from django.contrib import admin
# from .models import OrderDetails
# from .models import Order
from .models import *

# # Register your models here.
admin.site.site_header = " speed Futhur "
admin.site.site_title = " speed Futhur "
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','user_group','order_date','statusu','statusu','user_updete','Orderpartener','is_Orderpartener','posta')
    # list_display = ('user__username')
    search_fields = ('id','user__username','user_group__name',)

class PaymentAdmin(admin.ModelAdmin):
    list_display= ( 'id','order')
    search_fields = ( 'id','order__id')
    list_display_links = ( 'id','order')
    

admin.site.register(OrderDetails)
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Mo)
admin.site.register(Mr)
admin.site.register(Tp)
admin.site.register(Namepartener)
admin.site.register(Reportpartener)
admin.site.register(Clint)





