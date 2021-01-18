from django.urls import path
from . import views


app_name = 'proj'
urlpatterns = [

    #Main
    path('login/', views.Login.as_view(), name='login'),
    path('', views.Main.as_view(), name='main'),
    path('join/', views.Join.as_view(), name='join'),
    path('edit/', views.Edit.as_view(), name='edit'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('admin/', views.Admin.as_view(), name='admin'),
    path('<str:name>/maps/', views.Maps.as_view(), name='maps'),
    path('payment/', views.Payment, name='payment'),
    path('refund/', views.Refund, name='refund'),   
    path('pclist/', views.Pclist, name='pclist'), 
    path('setting/', views.Setting.as_view(), name='setting'),
    path('food/', views.Food.as_view(), name='food'),    


     
    #Board
    path('board/', views.Boarding.as_view(), name='board'),
    path('board/manage/', views.BoardManage.as_view(), name='boardmanage'),
    path('board/<int:boardnum>/', views.ContentList.as_view(), name='contentlist'),
    path('board/<int:boardnum>/search/', views.SearchContent.as_view(), name='searchcontent'),
    path('board/<int:boardnum>/<int:textnum>/', views.Content.as_view(), name='content'),
    path('board/write/', views.Write.as_view(), name='write'),
    path('board/<int:boardnum>/<int:textnum>/delete/', views.Delete.as_view(), name='delete'),


    #maps
    path('fox/', views.Fox, name='fox'),
    path('ghostcastle/', views.Ghostcastle, name='ghostcastle'),
    path('lime/', views.Lime, name='lime'),
    path('pop/', views.Pop, name='pop'),
    path('skybridge/', views.Skybridge, name='skybridge'),
    path('ocelot/', views.Ocelot, name='ocelot'),
   
]