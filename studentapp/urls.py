from django.urls import path, include
from studentapp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home_fn),
    #path('student',views.add_student),
    path('student',views.studata_fn),
    path('home', views.dashboard),
    path('delstu/<rid>',views.delstudent),
    path('updatestu/<rid>',views.updateStudent),

    #after integration 
    path('index',views.index_pg),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('filterbybranch/<brname>',views.filterByBranch),


    path('updateqty/<incr>/<cid>',views.updateQuantity),
    path('range',views.rangeSearch),
    path('details/<sid>',views.showDetails),
    path('addtocart/<sid>',views.addtocart),
    path('viewcart',views.viewcart),
    path("delete/<cid>",views.deletefromcart),
    # path('updateqty/<incr>/<cid>',views.updatequantity),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendemail',views.sendemail),
#     path('user-orders/', views.user_orders, name='user_orders'),
#     path('orders',views.userorders),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)