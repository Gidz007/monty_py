from django.conf import settings
from django.conf.urls.static import static

"""
URL configuration for kgl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# This url imports the categorypage from the views. 
from kglapp.views import categorypage, inventory_view, product_detail, addproduct,inventory, customerpage, creditpage, manual_register_user, login_user, logout_user, dashboard, branchdetail, pos_sale, editinventory, deletepage, product_edit, display_products, branchpage, deletepage

urlpatterns = [
    path('admin/', admin.site.urls),


    ###################################################
    ### These a the login urls that a to handle the login ins singn ins and the create accounts.
    # This is the index url
    path('category', categorypage, name='category'),
    path('branch', branchpage),


    #####################################################
    ### This is a url for adding stock. 
    path('addproduct/', addproduct),


    ###################################################
    ### This is the product display url.
    # This is the inventory url that displays what we have in our database.
    path('products/', inventory_view, name='products'),


    ####################################################
    ## These a dynamic urls. these a meant to handel the product sales.
    # A dynamic url that will vist the product being viewed.  
    path('view/<str:id>', product_detail ),
    # This rout is for editing the available inventory.
    path('edit/<int:id>', editinventory, name='products'), 
    # The route for deleting a inventory.
    path('delete/<int:id>', deletepage),


    ######################################################
    # A rounte to display products. 
    path('displayproduce/', display_products, name='displayproduce'),
    # A rounte for editing my products. 
    path('editproduct/<int:id>', product_edit),
    

    ####################################################
    ## This url is for inventory management.
    # This will manage the inventory of every branch.
    path('invent/', inventory),


    #####################################################
    ## This is a url for the customer's details form entry.
    path('customers', customerpage),


    #####################################################
    ## The route for the creditsales. 
    # This is to handle the navigations.
    path('credit', creditpage),     
    
    
    #####################################################
    ## The rounts to handle the login. 
    # The display based to the login.
    # Regester user manually.
    path('register/', manual_register_user),

    
    # Login and logout
    path('', login_user),  # Login page
    path('logout/', logout_user),


    # Home/dashboard after login
    path('home/', inventory_view),

    # path('', include('kglapp.urls')),

    #######################################################
    ## A route to handle the dashboard of the adminstrator.
    path('dash/', dashboard), 


    #######################################################
    ## This is a dynamic url that will veiw the details of a particular branch.  
    path('branch/<str:id>',branchdetail ),


    ######################################################
    path('pos-sale/', pos_sale, name='sales_page'),
    # Dynamic url to make a sale based on the product id.
    path('sale/<int:id>/', pos_sale, name='sales_detail'),

    # Url to delete aproduct.
    path('delete/<int:id>/', deletepage, name='delete_product'),

]




