from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .models import FF
from django.contrib import messages
from .decorators import allowedUsers,allowedCastomar
from accounts.models import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from .forms import Searchform,Productfrm,Categoryform,Gxform
from .models import Gxqu
from django.contrib.auth.models import Group
from accounts.backends import *
from .forms import *
from product.decorators import aminnUsers
from django.db.models import Sum,F,Count,Value
from django.contrib.auth.decorators import login_required
from datetime import datetime
from datetime import datetime
import pytz
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
r = pytz.timezone('Africa/Cairo')
eg = datetime.now(r) 
g = eg.strftime('%Y-%m-%d %H:%M:%M:%S')
def cat(request):
    bb = Cat.objects.all()
 
 
    return render(request, 'cat.html',{"all_orders":bb} )

def t404(request):
     return render(request, '404.html', )
# Create your views here.
from django_ratelimit.decorators import ratelimit
@allowedUsers(allowedGroups=['staff','hr'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def updatemasd(request,id,):
    gx = Ma.objects.get(id=id)
    if not gx.user == request.user:
        messages.error(request, ' يجب ان تكون ان ضايف القيمه المصرفيه  ')
        return redirect('masd')

   
    if request.method == 'POST' :
            qu = request.POST['qu']
            book_save = Maform(request.POST, request.FILES ,instance=gx)
            if int(qu) > int(10000) :
                messages.error(request, '  اضافة القيمه من 1 الى 10000')
                return redirect('masd')

    
            
            elif book_save.is_valid():
                book_save.save()
                messages.success(request, 'تم التعديل')
                return redirect('masd')

    else:
            book_save =Maform(instance=gx)

    context ={
            'form':book_save,
        }
    return render(request, 'pages/update.html',context)





@allowedUsers(allowedGroups=['staff','hr'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def deletemasd(request,id):     
     pro_delete = get_object_or_404(Ma, id=id)
     if not pro_delete.user == request.user:
        messages.error(request, ' يجب ان تكون  ضايف القيمه المصرفيه  ')
        return redirect('masd')
     if request.method == 'POST':
          pro_delete.delete()
          messages.success(request, 'تم الحذف')
          return redirect('masd')
     else:
         return render(request,'pages/delete.html',)

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['hr','staff'])
def masd(request):
    events = Ma.objects.all()
    context : None
    if request.method == 'POST':
        gr = request.POST.get('gr')
        mr =  request.POST.get('mr')
        name =  request.POST.get('name'),
        user =  request.POST.get('user'),
        if name:
            events = events.filter(name__icontains = name)
        if user:
            events = events.filter(user__username__icontains = user)
        
    
        if mr and gr:
            events = events.filter(publish_date__range = (mr, gr ))
        elif mr:
            events = events.filter(publish_date__gte = mr)
        elif gr:
                events = events.filter(publish_date__lte = gr)
        try:
            
            context = {
                'ma':events
            }
            messages.success(request, ' عملية بحث  ناجحه ')
            return render (request, 'prodects/masd.html', context)
        except:
            context = {
              "ma":events
             }
            messages.error(request, ' عملية بحث غير ناجحه ')
            return render (request, 'prodects/masd.html', context)
    else:
           context = {
              "ma":events
          }
    return render (request, 'prodects/masd.html', context)


@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['hr','staff'])
def mas(request):

    if request.method == 'POST' :
        if  request.POST.get('qu') == '': 
           messages.error(request, 'مربع القيمه الواصله فارغ')
           return redirect('mas')

        if  request.POST.get('name') == '': 
           messages.error(request, 'مربع  اسم المصرف فارغ')
           return redirect('mas') 

        if  request.POST.get('nots') == '': 
           messages.error(request, 'مربع  الملحوظه فارغ')
           return redirect('mas') 

        qu = request.POST.get('qu')
        if int(qu) > int(300) :
                messages.error(request, '  اضافة القيمه من 1 الى 300')
                return redirect('masd') 
        add_category= Maform(request.POST)
        if add_category.is_valid():
               f = add_category.save(commit=False)
               f.user = request.user
               f.save()
               messages.success(request, 'تم  اضافة قيمة صرف  ')
               return redirect('masd')
        else:
            messages.error(request, 'عمليه خاطْئه')
            return redirect('orderOrder',) 
    
    else:
       context = {
       'form':Maform(),
         }
       return render (request, 'prodects/gxqu.html', context)


@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['groadmin'])
def gxqu(request,id):
    gx = Gx.objects.get(id=id)
    gr = 0
    gsd = Gxqu.objects.filter(gx=gx.id)
    for igf in gsd:
       gr += int(igf.qu)
    # print(gr)
    if gr == None:
       gr = 0
    # v = Product.objects.filter(gx=gx.pk).aggregate(Sum("pricels"))['pricels__sum']
    vd = Product.objects.filter(gx=gx.pk)
    
    sd = 0
    for i in vd:
         iz = Fintion.objects.filter(fintion=i.pk, order_idsid__statusu='completed')
         for ig in iz:
            sd += int(ig.fintion.pricels) * int(ig.usus)

    if request.method == 'POST' :
        if  request.POST.get('qu') == '': 
           messages.error(request, 'مربع القيمه الواصله فارغ')
           return redirect('Gxqu',id=id) 
        tt = request.POST['qu']
        y =  int(gr) + int(tt)
        if not sd >= int(y):
            messages.error(request, ' القيمه الواصله اكبر من مجموع القيمه المسحوبه')
            return redirect('Gxqu',id=id)  

        
      
        add_category= Gxquform(request.POST)
        if add_category.is_valid():
               f = add_category.save(commit=False)
               f.name = request.user
               f.gx = gx
               f.save()
               messages.success(request, 'تم  اضافة قيمه واصله')
               return redirect('dgxr',id=id)
        else:
            messages.error(request, 'عمليه خاطْئه')
            return redirect('Gxqu',id=id) 
    

    else:
       context = {
       'form':Gxquform(),
         }
       return render (request, 'prodects/gxqu.html', context)


@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['groadmin'])
def gx(request):
    if request.method == 'POST' :
        
        if  request.POST.get('gx') == '': 
           messages.error(request, 'مربع التاجر فارغ')
           return redirect('gx') 
            
        if  request.POST.get('title') == '': 
           messages.error(request, 'مربع العنوان فارغ')
           return redirect('gx') 

        if  request.POST.get('number') == '': 
           messages.error(request, 'مربع رقم الهاتف فارغ')
           return redirect('gx') 
        if  len(request.POST.get('number')) != int(11): 
           messages.error(request, '  يجب رقم الهاتف ان يكون 11 رقم ')
           return redirect('gx') 
        if  request.POST.get('email') == '': 
           messages.error(request, 'مربع رقم الاميل فارغ')
           return redirect('gx') 
        email = request.POST.get('email') 
        if Gx.objects.filter(email=email).exists():
            messages.error(request, ' هذا الاميل موجود مسبقا ')
            return redirect('gx') 

        add_category= Gxform(request.POST)
        
        if add_category.is_valid():
               add_category.save()
               messages.success(request, 'تم اضافة تاجر')
               return redirect('gxd')
        else:
            messages.error(request, 'يوجد هذا التاجر مسبقا')
            return redirect('gxd')
    else:
       context = {
       'form':Gxform(),
         }
       return render (request, 'prodects/gx.html', context)
    
@allowedUsers(allowedGroups=['groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def deleteGx(request,id):     
     pro_delete = get_object_or_404(Gx, id=id)
     if request.method == 'POST':
          pro_delete.delete()
          messages.success(request, 'تم الحذف')
          return redirect('gxd')
     else:
         return render(request,'pages/delete.html',)

@allowedUsers(allowedGroups=['groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def updateGx(request,id,):
    gx = Gx.objects.get(id=id)
    
    if request.method == 'POST' :
       
            book_save = Gxform(request.POST, request.FILES ,instance=gx)
            if book_save.is_valid():
                book_save.save()
                messages.success(request, 'تم التعديل')
                return redirect('gxd')

    else:
            book_save =Gxform(instance=gx)

    context ={
            'form':book_save,
        }
    return render(request, 'pages/update.html',context)






@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['groadmin'])
def gxd(request):
    gr = request.POST.get('gr')
    mr = request.POST.get('mr')
    id = request.POST.get('id')
    email = request.POST.get('email')

    gx = Gx.objects.all()
    if request.method == 'POST':
        try:
            f = gx.filter(
                gx__icontains = gr,
                number__icontains = mr,
                id__icontains = id,
                email__icontains = email,

                )
                
            context ={
                          'gx':f,
                       } 
            messages.success(request, 'عملية بحث ناجحة')
            return render (request, 'prodects/gxd.html', context)
        except:
             context ={
                          'gx':gx,
                       } 
             messages.error(request, 'عملية بحث غير ناجحة')
             return render (request, 'prodects/gxd.html', context)
    
       
    context = {
       'gx':gx,
         }
    return render (request, 'prodects/gxd.html', context)

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['groadmin'])
def gxproduct(request,id):
    gx = Gx.objects.get(id=id)
    vf = 0
    bv = Gxqu.objects.filter(gx=gx.id)
    for i in bv:
        vf += int(i.qu)
    product = Product.objects.filter(gx=gx.id)
    sad = 0
    sa = 0 
    for iu in product:
         v = Fintion.objects.filter(fintion=iu.pk, order_idsid__statusu='completed')
         for i in v:
            sad += int(i.usus) * int(i.fintion.pricels)
         b = Fintion.objects.filter(fintion=iu.id, ).exclude(order_idsid__statusu ='completed')
         for isd in b:
            sa = int(isd.usus) * int(isd.fintion.pricels)
    grx = request.POST.get('gr')
    g = request.POST.get('id')
    # gx = Gx.objects.all()
    if request.method == 'POST':
        
        try:
            f = product.filter(
                name__icontains = grx,
                id__icontains = g,
                )
                
            context ={
                        'gx':f,
                        'gr':gx,
                        'hf':vf,
                        'sa':sa,
                        'sad':sad
                       } 
            messages.success(request, 'عملية بحث ناجحة')
            return render (request, 'prodects/gxproduct.html', context)

        except:
             context ={
                          'gx':product,
                          'gr':gx,
                         'hf':vf,
                         
                         'sa':sa,
                         'sad':sad
                       } 
             messages.error(request, 'عملية بحث غير ناجحة')
             return render (request, 'prodects/gxproduct.html', context)


    else:
        context = {
                'gx':product,
                'gr':gx,
                'sa':sa,
                'sad':sad,
                'hf':vf
                  }
        return render (request, 'prodects/gxproduct.html', context)

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['groadmin'])
def dgxr(request,id):
    gx = Gx.objects.get(id=id)
    # gr = 0
    # grc = Gxqu.objects.filter(gx=gx.id)
    # for i in grc:
    #     gr = i.qu
    
    # print(gr)
    # if gr == None:
    #    gr = 0
    v = Product.objects.filter(gx=gx.pk).aggregate(Sum("pricels"))['pricels__sum']
    vd = Product.objects.filter(gx=gx.pk)
    
    sd = 0
    for i in vd:
         iz = Fintion.objects.filter(fintion=i.pk, order_idsid__statusu='completed')
         for ig in iz:
            sd += int(ig.fintion.pricels) * int(ig.usus)
    
    gxh = Gx.objects.get(id=id)
    b = Gxqu.objects.filter(gx=gxh.id)
    bs = 0
    bsx = Gxqu.objects.filter(gx=gxh.id)
    for i in bsx:
         bs += int(i.qu)
    if bs == None:
        bs = 0
    s = int(sd) - int(bs)
    context = {
       'gx':b,
       'gr':gxh,
       'bs':bs,
       'sd':sd,
       's':s
         }
    return render (request, 'prodects/dgxr.html', context)

@allowedUsers(allowedGroups=['groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def deleteGxqu(request,id,ids):     
     pro_delete = get_object_or_404(Gxqu, id=id)
     if request.method == 'POST':
          pro_delete.delete()
          messages.success(request, 'تم الحذف')
          return redirect('dgxr',id=ids)
     else:
         return render(request,'pages/delete.html',)
     
@allowedUsers(allowedGroups=['groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def updateGxqu(request,id,ids):
    gx = Gx.objects.get(id=ids)
    gr = Gxqu.objects.filter(gx=gx.id).aggregate(Sum('qu'))['qu__sum']
    # print(gr)
    if gr == None:
       gr = 0
    v = Product.objects.filter(gx=gx.pk).aggregate(Sum("pricels"))['pricels__sum']
    vd = Product.objects.filter(gx=gx.pk)
    
    sd = 0
    for i in vd:
         iz = Fintion.objects.filter(fintion=i.pk, order_idsid__statusu='completed')
         for ig in iz:
            sd += int(ig.fintion.pricels) * int(ig.usus)
    
    gr = Gxqu.objects.filter(gx=gx.id).aggregate(Sum('qu'))['qu__sum']
    gs = Gxqu.objects.get(gx__id=ids,id=id)

    v = Product.objects.filter(gx=gx.id)
    s = 0
    for i in v:
        s +=i.qu * i.pricels
    if request.method == 'POST' :
        if  request.POST.get('qu') == '': 
           messages.error(request, 'مربع القيمه الواصله فارغ')
           return redirect('Gxqu',id=id) 
        tt = request.POST['qu']
        y = (int(tt) + gr) - int(gs.qu ) 
        if not sd >= y:
            messages.error(request, ' القيمه الواصله اكبر من مجموع القيمه المسحوبه')
            return redirect('updateGxqu',id=id,ids=ids) 
        
        else:
            book_save = Gxquform(request.POST, request.FILES ,instance=gs)
            if book_save.is_valid():
                book_save.save()
                messages.success(request, 'تم التعديل')
                return redirect('dgxr',id=ids)

    else:
            book_save =Gxquform(instance=gs)

    context ={
            'form':book_save,
        }
    return render(request, 'pages/update.html',context)



from django.utils import timezone
@login_required(login_url='signin')
@ratelimit(key='ip', rate='100/m')
@allowedUsers(allowedGroups=['factory','groadmin'])
def prodectsfactrory(request):
    
    v =  Gx.objects.filter(email=request.user.email).exists()
    ssd = None
    if v:
        gr =  Gx.objects.get(email=request.user.email)
        ssd = gr.pk
 
   
    events = Product.objects.filter(gx=ssd).annotate(
        pro_dahte = F('pro_date') + timezone.timedelta(minutes=10) ,
        
       
    )
   

   
    if request.method == "POST"  or 'p' in request.POST:
          
            try:
               namel =request.POST.get('namel')
               lg =request.POST.get('lg')
               ls =request.POST.get('ls')
               name =request.POST.get('name')
               number =request.POST.get('number')
               facat =request.POST.get('facat')
               gx =request.POST.get('gx')
               id =request.POST.get('id')

               if name:
                   events = events.filter(name__icontains = name)
               if id:
                   events = events.filter(uuid__icontains = id)
               if number:
                   events = events.filter(gx__number__icontains = number)
               if facat:
                   events = events.filter(facat__icontains = facat)
               if gx:
                   events = events.filter(gx__gx__icontains = gx)
           
               if ls and lg:
                   events = events.filter(publish_date__range = (ls, lg ))
               elif ls:
                   events = events.filter(publish_date__gte = ls)
               elif lg:
                   events = events.filter(publish_date__lte = lg)

             
    #            f = product.filter(
    #                  publish_date__range = [
    #                  lg,
    #                  ls
            
    #                  ],
                  
    #                 #  namel__icontains = namel,
    #                  name__icontains = name,
    #                  id__icontains = id,

    #                  gx__number__icontains = number,
    #                  facat__icontains = facat,
    #                  gx__gx__icontains = gx,

    #            ).annotate(
    #     pro_dahte = F('pro_date') + timezone.timedelta(minutes=10) ,
       
    # )
              
              
              
               context ={
                  'Product': events,
                  'g':timezone.now()
               } 
               messages.success(request, 'عملية بحث ناجحة')
               return render(request, 'pages/addprodectfactory.html' , context)
            except:
                context ={
                  'Product': events,
                  'g':timezone.now()
                } 
                
                messages.error(request, '  عملية بحث غير ناجحة  ')
                return render(request, 'pages/addprodectfactory.html' , context)

    else:
         
      
         context = {
           'Product': events,
             'from':Productfrm(),
           'all':Product.objects.all().count(),
           'formcat': Categoryform(),
           'category':Category.objects.all(),
           
           'category':Category.objects.all(),
           'g':timezone.now()
         
             }

         return render(request, 'pages/addprodectfactory.html' , context)


@allowedUsers(allowedGroups=['factory','groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def addprodectfactorygx(request):
    ty = UserProfile.objects.filter(user_id=request.user.id)
    if ty:
        for i in ty:
             if Gx.objects.filter(email = i.user.email).exists():
                 messages.error(request, '  تم اضافة تاجر مسبقا')
                 return redirect('prodectsfactrory')
             else:
                 gr = Gx()
                 gr.gx = i.user.username
                 gr.title = i.address
                 gr.email = i.user.email
                 gr.number = i.zip_number
                 gr.save()
                 messages.success(request, ' تم اضافة تاجر ')
                 return redirect('prodectsfactrory')
    messages.success(request, ' لا يوجد مستخدم')
    return redirect('prodectsfactrory')




@allowedUsers(allowedGroups=['factory','groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def addprodectfactory(request):
     
     if request.method == 'POST':
        facat = False
        boonimg = False
        photo = None
        photos = None
        gx = None
        
        if 'gx' in request.POST:
            
           gx = request.POST.get('gx')
        else:
            messages.error(request, ' لا يوجد تاجر  ')
            return redirect('addprodectfactory')
        g = Gx.objects.filter(id=gx).last()
       
        if not g.gx == request.user.username:
            messages.error(request, ' اختر التاجر الذى اضفته ')
            return redirect('addprodectfactory')

        
        if 'photo' in request.FILES:
            
           photo= request.FILES.get('photo')
        else:
            messages.error(request, '   اضف صوره للمنتج')
            return redirect('addprodectfactory')
        
        if 'photos' in request.FILES:
            photos = request.FILES.get('photos')
        else:
            messages.error(request, '   اضف صوره اضافيه للمنتج')
            return redirect('addprodectfactory')

        if 'facat' in request.POST:
             facat = request.POST['facat']
             facat = True
        else:
             facat = False
           
        if 'boonimg' in request.POST:
            boonimg = request.POST['boonimg']
            boonimg = True
        else:
            boonimg = False
            
        if boonimg == True and  facat == True:
            messages.error(request, 'عملية  غير ناجحة')
            return redirect('addprodectfactory')
        
        else:
  
            add_book = Productfactoryform(request.POST, request.FILES)
            
            if add_book.is_valid():
                t = add_book.save( commit=False)
                t.qu =  request.POST['qur']
                t.user_updete = request.user
                t.user_create = request.user
                # t.gx = request.user
                t.save()
                messages.success(request, f'  تم اضافة منتج لى {request.user} ')
                return redirect('prodectsfactrory')
            else:
                messages.error(request, '  عملية  غير ناجحة  ')
                return redirect('addprodectfactory')
  
        
     context = {
       'from':Productfactoryform(),
       'user':request.user,
       
    #    't':t,
       'category':Category.objects.all(),
  
         
    }

     return render(request, 'pages/addfactroy.html' , context)
@allowedUsers(allowedGroups=['factory','groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def deletefactory(request,id):
     pro_delete = get_object_or_404(Product, id=id)
     pro = Product.objects.get(id=id)
     h = Fintion.objects.filter(fintion=pro_delete).exists()
     o = request.user
     i = pro.user_updete
   
 
     if pro_delete.statusu == 'completed':
        messages.error(request, ' عمليه خاطئه ')
        return redirect('prodectsfactrory')
     if not pro_delete.pro_date + timezone.timedelta(minutes=10) > timezone.now() :
        messages.error(request, ' تم انتهاء المدة الحذف ')
        return redirect('prodectsfactrory')
     elif h:
        messages.error(request, ' تم السحب من المنتج ولا يمكن الحذف عليه ')
        return redirect('prodectsfactrory')

     elif pro.statusu == 'completed':
        messages.error(request, 'اطلب اكتمل ولا يمكن حذفه ')
        return redirect('prodectsfactrory')
     elif not pro.user_create == request.user  and not  request.user.groups.filter(name='factory')  :
        messages.error(request, ' انت لسة اليزر الذى اضف المنتج  ')
        return redirect('prodectsfactrory')

     
     elif request.method == 'POST':
          pro.delete()
          messages.success(request, 'تم الحذف')

          return redirect('prodectsfactrory')

     else:
         
         return render(request,'pages/delete.html',)

@allowedUsers(allowedGroups=['factory','groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def updatefactory(request, id):
    book_id = Product.objects.get(id=id)
    h = Fintion.objects.filter(fintion=book_id).exists()

    pro = Product.objects.get(id=id)
    if pro.photo == '' or None:
        messages.error(request, '  اضف صوره للمنتج ')
        return redirect('prodectsfactrory')
    if pro.photos == '' or None:
        messages.error(request, '  اضف صوره اصافيه للمنتج ')
        return redirect('prodectsfactrory')

    o = request.user
    i = pro.user_updete
    if book_id.statusu == 'completed':
        messages.error(request, ' عمليه خاطئه ')
        return redirect('prodectsfactrory')
    if not book_id.pro_date + timezone.timedelta(minutes=10) > timezone.now() :
        
        messages.error(request, ' تم انتهاء المدة التعديل ')
        return redirect('prodectsfactrory')
    elif h:
        messages.error(request, ' تم السحب من المنتج ولا يمكن التعديل عليه ')
        return redirect('prodectsfactrory')

    elif pro.statusu == 'completed':
        messages.error(request, 'اطلب اكتمل ولا يمكن التعديل عليه')
        return redirect('prodectsfactrory')

    elif not pro.user_create == request.user  and not  request.user.groups.filter(name='factory')  :
        messages.error(request, ' انت لسة اليزر الذى اضف المنتج  ')
        return redirect('prodectsfactrory')

    elif request.method == 'POST':
        facat = None
        boonimg = None

        if 'facat' in request.POST:
             facat = request.POST['facat']
         
           
        if 'boonimg' in request.POST:
            boonimg = request.POST['boonimg']
       
            
        if boonimg == 'on' and  facat == 'on':
          
          
            messages.error(request, 'عملية  غير ناجحة')
            return redirect('prodectsfactrory')
        # elif len(request.POST['number'] ) !=  int(11) :
        #         messages.error(request, 'لابد ان يكون رقم الهاتف  مكون من 11 رقم')
        #         return redirect('index')
        else:
            book_save = Productfactoryform(request.POST, request.FILES ,instance=book_id)
            # if book_save.cleaned_data.get('photo') == '':
            #     messages.error(request, '   اشف صوره للمنتج')
            #     return redirect('prodectsfactrory')

            if book_save.is_valid():
                t = book_save.save(commit=False)
                t.user_updete = request.user
                t.user_create = request.user
                t.qu =  request.POST['qur']
                t.save()
                messages.success(request, 'تم التعديل')

                return redirect('prodectsfactrory')

    else:
            book_save =Productfactoryform(instance=book_id)
  
    context ={
            'form':book_save,
             
       'category':Category.objects.all(),
        }
    return render(request, 'pages/update.html',context)



@allowedUsers(allowedGroups=['groadmin','adminCastomar',])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def update_is_active(request, id):
    book_id = Product.objects.get(id=id)
    h = Fintion.objects.filter(fintion=book_id).exists()
    pro = Product.objects.get(id=id)
    if   pro.pro_date  + timezone.timedelta(minutes=10) > timezone.now():
        messages.error(request, '  لا يتم التفعيل الى بعد 10 دقائق  ')
        return redirect('index')
    if request.user.groups.filter(name='adminCastomar'):
        if pro.is_active == True:
            if   pro.update_pro  + timezone.timedelta(minutes=10) < timezone.now():
                 messages.error(request, '  اتجه للاداره للتعدل فيه ')
                 return redirect('index')
    
    if pro.facat == True:
                 Colorsd =  Color.objects.filter(productcolor=pro)
                 for Colors in Colorsd:
                    if not Sise.objects.filter(productsise__pk=Colors.pk).exists():
                           messages.error(request, '  اضف مقاسات للالوان')
                           return redirect('index')
    
    if pro.statusu == 'completed':
        messages.error(request, 'اطلب اكتمل ولا يمكن التعديل عليه')
        return redirect('index')
    
    if  pro.price ==  None and pro.price_decint ==  None :
                messages.error(request, '   تحقق من اضافة سعر للمنتج واضافة سعر وهمى ')
                return redirect('index')
    if not pro.photo and pro.photos:
        messages.error(request, 'تاكد من اضافة الصور')
        return redirect('index')

    elif request.method == 'POST':
            if  pro.price ==  None and pro.price_decint ==  None :
                messages.error(request, '   تحقق من اضافة سعر للمنتج واضافة سعر وهمى ')
                return redirect('index')
            if not pro.photo and pro.photos:
                 messages.error(request, 'تاكد من اضافة الصور')
                 return redirect('index')
            if pro.boonimg == True:
                 co =  Img.objects.filter(i=pro).aggregate(s = Sum(F('quimg')))['s'] or 0
                 if co == 0:
                      messages.error(request, '  اضف الوان ')
                      return redirect('index')
            if pro.facat == True:
                 co =  Color.objects.filter(productcolor=pro).aggregate(s = Sum(F('qucolor')))['s'] or 0
                 if co == 0:
                      messages.error(request, '  اضف الوان ')
                      return redirect('index')
                 
                 so =  Sise.objects.filter(productsise__productcolor=pro).aggregate(s = Sum(F('qusise')))['s'] or 0
                 if so == 0:
                      messages.error(request, '  اضف مقاسات ')
                      return redirect('index')
            coy=  Color.objects.filter(productcolor=pro)
            for vc in coy:
               ds = Sise.objects.filter(productsise__id=vc.id,productsise__productcolor__id=pro.id)
               
            book_save = Productform_is_active(request.POST, request.FILES ,instance=book_id)
            if book_save.is_valid():
                ssh = book_save.save(commit=False)

                ssh.update_pro = timezone.now()
                ssh.save()
                messages.success(request, 'تم التفعيل')
                return redirect('index')
    else:
            book_save =Productform_is_active(instance=book_id)
  
    context ={
            'form':book_save,
             
            'category':Category.objects.all(),
        }
    return render(request, 'pages/update.html',context)


@ratelimit(key='user_or_ip', rate='25/m')
def prodects(request):
    pro = Product.objects.filter(is_active=True).exclude(qu=0)
    page = request.GET.get('page',1)
    paginator = Paginator(pro,1000000)
    try:
        pro = paginator.page(page)
    except PageNotAnInteger:
        pro = paginator.page(1)
    except EmptyPage:
        pro = paginator.page(paginator.num_pages)

    name = None
    desc = None
    pfrom =None
    pto = None
    cs = None
   
    pro = Product.objects.filter(is_active=True).exclude(qu=0)

    if 'cs' in request.GET:
        cs = request.GET['cs']
        if not cs:
            cs = 'off'

    if 'searchname' in request.GET:
      name=request.GET['searchname']
      if name:
        if cs == 'on':
          pro=pro.filter(name__icontains=name)
        else:
             pro=pro.filter(name__icontains=name)
    
    if 'searchdesc' in request.GET:
        desc = request.GET['searchdesc']
        if desc:
            if cs == 'on':
              pro = pro.filter(description__contains=desc)
            else:
                 pro = pro.filter(description__icontains=desc)

    if 'searchpricefrom' in request.GET and 'searchpriceto' in request.GET:
         pfrom = request.GET['searchpricefrom']
         pto = request.GET['searchpriceto']
         if pfrom and pto:
             if pfrom.isdigit() and pto.isdigit():
                 pro = pro.filter(price__gte=pfrom, price__lte=pto)
    if request.user.groups.filter(name='adminCastomar') or request.user.groups.filter(name='groadmin'):
        tr = True
        t = True
    else:
        tr = False
        t = False
    if request.user.groups.filter(name='hr') or request.user.groups.filter(name='staff'):
        hrr = True
    else:
        hrr = False
    context = {
       'Product':pro,
       'category':Category.objects.all(),
       'hrr':hrr,
       'tr':tr,
       't':t,
       'qus': request.user.groups.filter(name='castomar'),
       "my": Product.objects.filter(is_active=True,desconts=True).exclude(qu=0)
    }
    return render (request, 'prodects/prodects.html', context)

from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Product, Category




@allowedUsers(allowedGroups=['grosent',])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def delete_selected_products(request):
    if request.method == 'POST':
        ids = request.POST.getlist('products')
        print(ids)
        Product.objects.filter(id__in=ids).delete()
        return redirect('index')

    else:
         
         return render(request,'pages/delete.html',)# أو أي صفحة تود الرجوع إليها


@ratelimit(key='user_or_ip', rate='50/m')
# @login_required(login_url='signin')
def prodect(request, uuid):
    if not  request.user.is_authenticated and uuid:
        messages.error(request ,_('سجل اولا'))
        return redirect('signin')
    else:
        cache_key = f"pro__{uuid}"
        p = cache.get(cache_key)

        if p is None:
            p = get_object_or_404(Product, uuid=uuid)
            cache.set(cache_key, p, timeout=60*60)  # ساعة واحدة

        bb = Product.objects.filter(category=p.category, is_active=True).exclude(qu=0)

        context = {
            'pro': p,
            'qus': request.user.groups.filter(name='castomar'),
            'bb': bb,
            'category': Category.objects.all(),
            # 'uuuu': Sise.objects.filter(productsise__productcolor__id=pro_id, productsise__name=colar)  # معلقة لعدم توفر المتغير colar
        }

        return render(request, 'prodects/prodect.html', context)


# from django.core.cache import cache

# @ratelimit(key='user_or_ip', rate='50/m')
# @login_required(login_url='signin')
# def prodect(request,uuid):
#     if request.user.is_authenticated and not request.user.is_anonymous and uuid:
#      cache_kay = f"pro__{pro_id}"
#      p = cache.get(cache_kay)
#      if p is None:
#          p = get_object_or_404(Product,uuid=uuid)
#          cache.set(cache_kay,p,timeout=60*60)
#          bb = Product.objects.filter(category=p.category).filter(is_active=True).exclude(qu=0)
    


#          context = {
#            'pro':get_object_or_404(Product,pk=pro_id),
#            'qus': request.user.groups.filter(name='castomar'),
#            'bb':bb,
          
#            'category':Category.objects.all(),
    
#         #    'uuuu':  Sise.objects.filter(productsise__productcolor__id=pro_id,productsise__name=colar)
          
#           }
     
#          return render (request, 'prodects/prodect.html',context)

def search(request):
    return render (request, 'prodects/search.html')

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['groadmin'])
def profintion(request,id):
     
    if request.method == 'POST': 
        status = request.POST['statusu']
        pro = Product.objects.get(id=id)
        pro.statusu = status
        pro.save()
        return redirect('index')


    return render (request, 'orders/fanth.html')



@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['adminCastomar','groadmin'])
def index(request):
      
    
    if request.method == 'POST' and 's' in request.POST:
    
        add_category= Categoryform(request.POST)
        if add_category.is_valid():
               add_category.save()
               messages.success(request, 'تم اضافة فاقه')
               return redirect('index')

    product = Product.objects.all()
    if request.method == "POST"  or 'p' in request.POST:
          
            try:
               namel =request.POST.get('namel')
               lg =request.POST.get('lg')
               ls =request.POST.get('ls')
               name =request.POST.get('name')
               number =request.POST.get('number')
               facat =request.POST.get('facat')
               gx =request.POST.get('gx')
               id =request.POST.get('id')
               uuid =request.POST.get('uuid')


               events = Product.objects.all()
               
               if name:
                   events = events.filter( name__icontains = name)
               if number:
                   events = events.filter(gx__number__icontains = number)
               if namel:
                   events = events.filter(namel__icontains = namel)
               if gx:
                   events = events.filter(gx__gx__icontains = gx)
               if id:
                   events = events.filter(id__icontains = id)
               if id:
                   events = events.filter(uuid__icontains = uuid)
               if facat:
                   events = events.filter(facat__icontains = facat)
               if lg and ls:
                   events = events.filter(publish_date__range = (lg, ls ))
               elif lg:
                   events = events.filter(publish_date__gte = lg)
               elif ls:
                   events = events.filter(publish_date__lte = ls)
            #    product = f.filter(
            #          publish_date__range = [
            #          lg,
            #          ls
            
            #          ],
                  
            #         #  namel__icontains = namel,
            #          name__icontains = name,
            #          id__icontains = id,

            #          gx__number__icontains = number,
            #          facat__icontains = facat,
            #          gx__gx__icontains = gx,

            #    )
              
              
              
               context ={
                  'Product': events,
               } 
               messages.success(request, 'عملية بحث ناجحة')
               return render(request, 'pages/index.html' , context)
            except:
                
                messages.error(request, '  عملية بحث غير ناجحة  ')
                return redirect('index')
    else:
         
         if request.user.groups.filter(name='adminCastomar') or request.user.groups.filter(name='groadmin'):
             tr = True
             t = True
         else:
            tr = False
            t = False

         if request.user.groups.filter(name='hr') or request.user.groups.filter(name='staff'):
            hrr = True
   
         else:
            hrr = False
         context = {
           'Product': product,
             'from':Productfrm(),
           'all':Product.objects.all().count(),
           'formcat': Categoryform(),
           'category':Category.objects.all(),
            'hrr':hrr,
           'tr':tr,
           't':t,
           'category':Category.objects.all(),
         
             }

         return render(request, 'pages/index.html' , context)


@aminnUsers(adminGroups=['groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')

def category(request):
    userprofile = UserProfile.objects.get(user=request.user)
    if request.user.groups.filter(name='adminCastomar')  or request.user.groups.filter(name='groadmin'):
        tr = True
       
    else:
        tr = False
    if request.user.groups.filter(name='hr'):
        hrr = True
   
    else:
        hrr = False
     
    context = {
     
       'category':Category.objects.all(),
       'userprofile' : UserProfile.objects.get(user=request.user),
       'userimg':userprofile.userimg ,
        'hrr':hrr,
        'tr':tr,
        'category':Category.objects.all(),
 
         
    }

    return render(request, 'parts/asidepar.html' , context)


@allowedUsers(allowedGroups=['adminCastomar','groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def addindex(request):
     
     if request.method == 'POST':
       
        facat = False
        boonimg = False
        qu = None
        qur = None
        if 'qu' in request.POST:
            qu = request.POST.get('qu')
        else:
            messages.error(request, ' الكميه غير موجوده  ')
            return redirect('addindex')
        if 'qur' in request.POST:
            qur = request.POST.get('qur')
        else:
            messages.error(request, '  الكميه الاصليه غير موجوده ')
            return redirect('addindex')
        if not qur == qu:
            messages.error(request, ' يحب ان يكون الكميه مساويه للكميه الاصليه فى البدايه  ')
            return redirect('addindex')

        if 'photo' in request.FILES:
            
           photo= request.FILES.get('photo')
        else:
            messages.error(request, '   اضف صوره للمنتج')
            return redirect('addindex')
        
        if 'photos' in request.FILES:
            photos = request.FILES.get('photos')
        else:
            messages.error(request, '   اضف صوره اضافيه للمنتج')
            return redirect('addindex')

        if 'facat' in request.POST:
             facat = request.POST['facat']
             facat = True
        else:
             facat = False
           
        if 'boonimg' in request.POST:
            boonimg = request.POST['boonimg']
            boonimg = True
        else:
            boonimg = False
            
        if boonimg == True and  facat == True:
            messages.error(request, ' لا يجب اختيار المقسات مع الوان معا ')
            return redirect('addindex')
        else:
            add_book = Productfrm(request.POST, request.FILES)
            if add_book.is_valid():
                t = add_book.save( commit=False)
                t.user_updete = request.user
                t.user_create = request.user
                t.save()
                messages.success(request, f'  تم اضافة منتج لى {request.user} ')
                return redirect('index')
            else:
                messages.error(request, '  عملية  غير ناجحة  ')
                return redirect('addindex')
     if request.user.groups.filter(name='adminCastomar')  or request.user.groups.filter(name='groadmin'):
        tr = True
        t = True
     else:
        tr = False
        t = False

     if request.user.groups.filter(name='hr'):
        hrr = True
   
     else:
        hrr = False
     context = {
       'from':Productfrm(),
       'user':request.user,
        'hrr':hrr,
       'tr':tr,
       't':t,
       'category':Category.objects.all(),
         
    }
     return render(request, 'pages/addindex.html' , context)

@allowedUsers(allowedGroups=['adminCastomar','groadmin'])

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def delete(request,id):
     pro_delete = get_object_or_404(Product, id=id)
     pro = Product.objects.get(id=id)
     if request.user.groups.filter(name='adminCastomar'):
        if pro.is_active == True:
        
            if   pro.update_pro + timezone.timedelta(minutes=10) < timezone.now()  :
                messages.error(request, ' انتهاء مدة التعدبل عليه اتجه للاداره ')
                return redirect('index')
 

     o = request.user
     i = pro.user_updete
     if pro.statusu == 'completed':
        messages.error(request, 'اطلب اكتمل ولا يمكن حذفه ')
        return redirect('index')
     elif not pro.user_updete == request.user  and not  request.user.groups.filter(name='groadmin')  :
        messages.error(request, ' انت لسة اليزر الذى اضف المنتج  ')
        return redirect('index')

     
     elif request.method == 'POST':
          pro.delete()
          messages.success(request, 'تم الحذف')

          return redirect('index')

     else:
         
         return render(request,'pages/delete.html',)

@allowedUsers(allowedGroups=['adminCastomar','groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def update(request, id):
    book_id = Product.objects.get(id=id)
    pro = Product.objects.get(id=id)
    if request.user.groups.filter(name='adminCastomar'):
        if pro.is_active == True:
            if   pro.update_pro + timezone.timedelta(minutes=10) < timezone.now()  :
                messages.error(request, ' انتهاء مدة التعدبل عليه اتجه للاداره ')
                return redirect('index')
 
    o = request.user
    i = pro.user_updete
    if pro.statusu == 'completed':
        messages.error(request, 'اطلب اكتمل ولا يمكن التعديل عليه')
        return redirect('index')
    
    elif not pro.user_updete == request.user  and not  request.user.groups.filter(name='groadmin')  :
        messages.error(request, ' انت لسة اليزر الذى اضف المنتج  ')
        return redirect('index')
    
    

    elif request.method == 'POST':
        if pro.photo == '' or None :
             messages.error(request, '  اضف صوره للمنتج ')
             return redirect('index')
        
        if pro.photos == '' or None:
            messages.error(request, '  اضف صوره اصافيه للمنتج ')
            return redirect('index')
        

    
        facat = None
        boonimg = None

        if 'facat' in request.POST:
             facat = request.POST['facat']
        if 'boonimg' in request.POST:
            boonimg = request.POST['boonimg']
        if boonimg == 'on' and  facat == 'on':
          
            messages.error(request, 'عملية  غير ناجحة')
            return redirect('index')
        # elif len(request.POST['number'] ) !=  int(11) :
        #         messages.error(request, 'لابد ان يكون رقم الهاتف  مكون من 11 رقم')
        #         return redirect('index')
        else:
            book_save = Productfrm(request.POST, request.FILES ,instance=book_id)
            if book_save.is_valid():
                t = book_save.save(commit=False)
                t.user_updete = request.user
                t.save()
                messages.success(request, 'تم التعديل')

                return redirect('index')

    else:
            book_save =Productfrm(instance=book_id)
  
    context ={
            'form':book_save,
             
       'category':Category.objects.all(),
        }
    return render(request, 'pages/update.html',context)



@ratelimit(key='user_or_ip', rate='10/m')
@allowedUsers(allowedGroups=['adminCastomar'])
def passs(request):
    
    title = 'k'
    passs = 1
    if 'user' in request.POST:
       
        if title == request.POST['user'] or passs == request.POST['passs']  :
            return redirect('index')
    
        else:
           messages.error(request,'هذه الصفحه متاحه للادارة فقط')
           return redirect('passs')
    else: 
        return render(request,'pages/pass.html')

@ratelimit(key='user_or_ip', rate='50/m')
def search(request):
    form = Searchform()
    j='llllllllllllllll'
    query = None
    results = []
    if 'query' in request.GET:
        form = Searchform(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.annotate(search=SearchVector('name','price'),).filter(search=query)
            j='llllllllllllllll'
    return render(request, 'prodect/search.html',{'form':form,'query':query,'results':results,'j':j})


# def post_search(request):
#     form = Searchform()
#     j='llllllllllllllll'
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = Searchform(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             search_vector = SearchVector('name','price')
#             search_query = SearchQuery(query,config='english')
#             results = Product.objects.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).filter(search=search_query).order_by('-rank')
#             j='llllllllllllllll'
#     return render(request, 'prodect/search.html',{'form':form,'query':query,'results':results,'j':j})

@aminnUsers(adminGroups=['groadmin'])
def cattger(request):
     cattger = Category.objects.all()
     return render(request, 'prodect/cattger.html',{'cattger':cattger,})


# @allowedUsers(allowedGroups=['adminCastomar'])

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
@aminnUsers(adminGroups=['groadmin'])
def deletecattger(request,id):
     pro_delete =get_object_or_404(Category, id=id)
     
     if request.method == 'POST':
          try:
             pro_delete =get_object_or_404(Category, id=id)
             pro_delete.delete()
             messages.success(request,"تم الحذف بانجاح")
             return redirect('cattger')
          except:
               messages.error(request,"مربوطه  بمنتجات اخرى")
               return redirect('cattger')

     else:
         return render(request,'pages/delete.html')

@aminnUsers(adminGroups=['groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def updatecattger(request, id):
    book_id = Category.objects.get(id=id)


    if request.method == 'POST':
        book_save = Categoryform(request.POST, request.FILES ,instance=book_id)
        if book_save.is_valid():
            book_save.save()
            return redirect('cattger')

    else:
            book_save =Categoryform(instance=book_id)
    context ={
            'form':book_save,
        }
    return render(request, 'pages/update.html',context)


@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])
def addimgs(request,id):

      
    pro = Product.objects.get(id=id)

    o = request.user
    i = pro.user_updete
    if  o != i :
       
         messages.error(request, 'عملية  غير ناجحة')
         return redirect('index')
    elif request.method == 'POST' and 's' in request.POST:
        quimg = request.POST['quimg']
        name = request.POST['name']
        asname = request.POST['name']

        i = Img.objects.filter(i_id=id)
        ol = Product.objects.get(id=id)
        io = 0
        for iy in i:
            io +=iy.quimg

        if int(ol.qu) >= int(quimg) + int(io):
        

            photos=None
            if  'photos' in request.FILES:
                    photos = request.FILES['photos']
            else:
     
                   photos = request.FILES['photos']
            Img.objects.create(photos = photos,i = Product.objects.get(id=id),quimg=quimg,name=name ,asname=asname)
            messages.success(request,"تم الاضافه")
         
            return redirect('dimgs',id=id)
        else:
            messages.error(request,"لقد نفذت الكميه")

            return redirect('dimgs',id=id)


    else:
        context={
            'form':Photosform()
        }
        return render(request, 'pages/addimg.html',context)
    

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])
def dimgs(request,id):
   pro = Product.objects.get(id=id)
   if not pro.pro_date + timezone.timedelta(minutes=10) > timezone.now() and  request.user.groups.filter(name='factory') :
        messages.warning(request, ' تم انتهاء المدة  ')
        return render(request, '404.html')


   o = request.user
   i = pro.user_updete
   if  o != i :
       
         messages.error(request, 'عملية  غير ناجحة')
         return redirect('index')
   else:
        i = Img.objects.filter(i__id=id)
        print(i)
        
        
        context={
                 'i':i,
                 's':Product.objects.get(id=id),
     
         }
        return render(request, 'pages/dimg.html',context)


@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def deleteimg(request,id,idimg):
     pro_delete =get_object_or_404(Img,i__id=id, id=idimg)
     
     if request.method == 'POST':
          try:
             pro_delete.delete()
             messages.success(request,"تم الحف بانجح")

             return redirect('dimgs',id=id)
          
          except:
               messages.error(request,"فشلت عملية الحذف")
               return redirect('dimgs',id=id)
              

     else:
         return render(request,'pages/delete.html')
     


@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def updateimg(request,id,idimg):
     pro_update =get_object_or_404(Img,i__id=id, id=idimg)
     
     if request.method == 'POST':
        book_save = Photosform(request.POST, request.FILES ,instance=pro_update)
        if book_save.is_valid():
            book_save.save()
            return redirect('dimgs',id=id)

     else:
        book_save =Photosform(instance=pro_update)
        context ={
            'form':book_save,
        }
        return render(request, 'pages/update.html',context)
         