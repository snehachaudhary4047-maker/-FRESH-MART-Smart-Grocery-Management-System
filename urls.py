from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(),  name='logout'),
    path('', views.HomeView.as_view(), name='home'),

    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/add/', views.CategoryAddView.as_view(), name='category_add'),
    path('category/<int:pk>/update', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('product/add/', views.ProductAddView.as_view(), name='product_add'),
    path('product/<int:pk>/update', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product_delete'),

    path('variant/add/', views.VariantAddView.as_view(), name='variant_add'),
    path('variant/<int:pk>/update', views.VariantUpdateView.as_view(), name='variant_update'),
    path('variant/<int:pk>/delete', views.VariantDeleteView.as_view(), name='variant_delete'),


    path('sales/',  views.SalesListView.as_view(), name='sales_list'),
    path('sales/add/',views.SalesAddView.as_view(), name='sales_add'),
    path('sales/<int:pk>/update', views.SalesUpdateView.as_view(), name='sales_update'),
    path('sales/<int:pk>/delete', views.SalesDeleteView.as_view(), name='sales_delete'),

    path('customer/',  views.CustomerListView.as_view(), name='customer_list'),
    path('customer/add',  views.CustomerAddView.as_view(), name='customer_add'),
    path('customer/<int:pk>/update',  views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customer/<int:pk>/delete',  views.CustomerDeleteView.as_view(), name='customer_delete'),

    path('bill/', views.BillCreateView.as_view(),  name='bill_create'),
    path('bill/<int:bill_no>/',views.BillPrintView.as_view(),  name='bill_print'),

    path('profit/', views.ProfitView.as_view(),      name='profit'),
    path('profit/<int:pk>/delete',views.ProfitDelete.as_view(), name='profit_delete'),
    path('profit/delete', views.ProfitTotalDelete.as_view(), name='profit_total_delete'),

    path('chatbot/', views.ChatBotView.as_view(), name='chatbot'),

    path('expiredcorner/',views.ExpiredCornerView.as_view(), name='expiredcorner'),

    path('contributor/',views.ProjectContributorView.as_view(), name='contributor'),

    path('matplotlib/', views.MatplotlibChartView.as_view(), name='matplotlib_charts'),

    path('daa/', views.DAAView.as_view(), name='daa'),


]