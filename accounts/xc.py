from django.db.models import OuterRef,Subquery,Exists
from orders.models import *
def orderOrder(request):
   
    
    orser = Order.objects.all()
    g = OrderDetails.objects.filter(order=OuterRef('pk')).order_by('pk')
    orser = orser.annotate(
        price= Subquery(g.values('price')[:1])
    )
    for v in orser:
        print(f"{v.pk} -   {v.price}")