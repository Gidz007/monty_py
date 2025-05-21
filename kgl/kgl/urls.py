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
from kglapp.views import (
    categorypage, 
    inventory_view, 
    product_detail, 
    addproduct,
    inventory, 
    customerpage, 
    creditpage, 
    manual_register_user, 
    login_user, 
    logout_user, 
    dashboard, 
    branchdetail, 
    pos_sale, 
    editinventory, 
    deletepage, 
    product_edit, 
    display_products, 
    branchpage, 
    deletepage, 
    managerview,
    salesagentland,
)
urlpatterns = [
    path('admin/', admin.site.urls),


    ###################################################
    ## Route that is to deal with the display of all users and redirect them to there landing pages.
    # Login 
    path('', login_user),  # Login page
    # logout
    path('logout/', logout_user), 
    


    #####################################################
    ## These a routes for handling entry forms. 
    # Products entry form. 
    path('addproduct/', addproduct),
    # Category entry form.
    path('category', categorypage, name='category'),
    # Branch details entry.  
    path('branch', branchpage),
    # Inventory entry form.
    path('invent/', inventory),
    # Credit customers entry form. 
    path('customers', customerpage),
    # Creditsales entry form per (branch).
    path('credit', creditpage),
    # Entering a user with there roles.
    path('register/', manual_register_user),
    # Route to handle the sale of a product. and make changes on runtime.
    path('pos-sale/', pos_sale, name='sales_page'),


    ###################################################
    ### Routs for handling templates that display data.
    # Viewing inventory recorded per branch.
    path('products/', inventory_view, name='products'),
    # Displaying a produce recorded. 
    path('displayproduce/', display_products, name='displayproduce'),


    ####################################################
    ## Dynamic rounts to take action on data.
    # viewing a product on selection per id.  
    path('view/<str:id>', product_detail ),
    # Editing a product and redirecting to the display.
    path('edit/<int:id>', editinventory, name='products'), 
    # Deleting an inventory.
    path('delete/<int:id>', deletepage, name='products'),
    # Editing a produce 
    path('editproduct/<int:id>', product_edit),
    # Deleting a product. 
    path('delete/<int:id>/', deletepage, name='delete_product'),
    # Dynamic url to querry data in form of reports.   
    path('branch/<str:id>',branchdetail ),
    # Making a sale based on the selection
    path('sale/<int:id>/', pos_sale, name='sales_detail'),



    #######################################################
    ## Routes to handle the landing pages of all the users. 
    # The dashboard for the admin.
    path('dash/', dashboard),
    # The manager's landing page
    path('manager/', managerview),
    # Route to handle the landing page of the sales agent.
    path('salesagent/', salesagentland),
]




