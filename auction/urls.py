from django.urls import path

from . import views

app_name = 'auction'
urlpatterns = [
    path('top/', views.TopView.as_view(), name='top'),
    path('create/', views.CreateAuctionView.as_view(), name='create_auction'),
    path('create_comp/', views.CreateAuctionCompView.as_view(), name='create_auction_comp'),
    path('<int:pk>/', views.AuctionDetailView.as_view(), name='auction_detail'),
    path('my_auction/', views.MyAuctionManagerView.as_view(), name='auction_manager'),
    path('my_auction/edit/<int:pk>', views.MyAuctionEditView.as_view(), name='auction_edit'),
    path('my_auction/delete/<int:pk>', views.MyAuctionDeleteView.as_view(), name='auction_delete'),
    path('bid_list/', views.BidListView.as_view(), name='bid_list'),
    path('success_bid_auction_list/', views.SuccessBidAuctionListView.as_view(), name='success_bid_auction_list'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('notification/', views.NotificationView.as_view(), name='notification'),

]
