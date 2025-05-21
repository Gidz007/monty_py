from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.db.models import Sum

# Importing models.
from django.db import models

# This imports the datatime for python. 
from datetime import date

# This imports the F model from djanago.
from django.db.models import F


### This imports the products model. 
from kglapp.models import Product, Category, Inventory, Branch, Customer, Creditsale, Userprofile, Receipt
# Create your views here.

##################################################
## Custome decorators to chck for roles before authorisation.
# Ths manager custome decorator.
def manager_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'userprofile') and request.user.userprofile.is_manager:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this page.")
    return _wrapped_view


## The owner custome decorator.
def owner_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'userprofile') and request.user.userprofile.is_owner:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this page.")
    return _wrapped_view


######################################################
## This is a custom decorator that checks for conditions before authorisation.
## This is for the sales agent and the manager.
def role_required(allowed_roles):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user has a UserProfile and matches one of the allowed roles
            if hasattr(request.user, 'userprofile'):
                userprofile = request.user.userprofile
                if (userprofile.is_manager and 'manager' in allowed_roles) or \
                   (userprofile.is_sales_agent and 'sales_agent' in allowed_roles):
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You are not authorized to access this page.")
        return _wrapped_view
    return decorator

# @login_required
# @user_passes_test(is_owner)
def manual_register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_salesagent = bool(request.POST.get('is_salesagent'))
        is_manager = bool(request.POST.get('is_manager'))
        is_owner = bool(request.POST.get('is_owner'))

        # Save the user
        new_user = Userprofile(
            username=username,
            email=email,
            password=make_password(password),
            is_salesagent=is_salesagent,
            is_manager=is_manager,
            is_owner=is_owner
        )
        new_user.save()
        return redirect('/')  # Or any other page you prefer

    return render(request, 'index.html')







###################################################
## This is the login view. 
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # change 'home' to whatever your home page name is
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'login.html', context)

    return render(request, 'login.html')






##################################################
## This is the category view,
# This view is meant handle the logic of the category model.
# This model to to be inheritated by the product model. and it will be in the form. of products.
# This is for distinguishing the different categories of products from the legumes and the cereals.
# @login_required
# @manager_required
def categorypage(request):
    if request.method == 'POST':
        data = request.POST
        new_category = Category(
            category_name = data.get('category_name')
        )
        new_category.save()

        return redirect('products')  # Redirect to the products page or any other page you prefer

    return render(request, 'category.html')








##############################################
## This is a view for listing products.
# This will be for displaying the several products that a in stock.
# This will use a context to display products using templating 
# There will be a loop for that will interlece through the model to display the products.
# @login_required
# @user_passes_test(lambda u: u.is_salesagent or u.is_manager)
# @role_required(['sales_agent', 'manager'])
def inventory_view(request):
    all = Inventory.objects.all()

    context = {
        'all_products' : all
    }
    return render(request, 'productsale.html', context)






##############################################
### A view to handle a checked out or sold product.
# This will lead to a page that displays all the details of a particular product.
# This is the view for the dynamic url the goes to the page of the product details.
# @role_required(['sales_agent', 'manager'])
def product_detail(request, id):
    sent_id = id
    all = Inventory.objects.get(id=sent_id )
    
    context = {
        'product' : all,
    }
    return render(request, 'product_details.html', context)






###############################################
## A view to diplay all products tageting a way i can edit them before they a entred in the inventory system of a particular branch.
# @role_required(['sales_agent', 'manager'])
def display_products(request):
    all_objs = Product.objects.all()

    context = {
        'all_products' : all_objs
    }  

    return render(request, 'productsdisplay.html', context)







###############################################
## A view for editing products in that a purchased.
# @manager_required
def product_edit(request, id):
    # Fetch the product to edit
    product = get_object_or_404(Product, id=id)

    # Fetch all categories for the dropdown
    all_categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST

        # Fetch the selected category
        category_id = data.get('cat_name')
        category_obj = get_object_or_404(Category, id=category_id)

        # Update the product fields
        product.supplier_name = data.get('supplier_name')
        product.product_name = data.get('product_name')
        product.sku = data.get('sku')
        product.buying_price = data.get('buying_price')
        product.quantity = int(data.get('quantity') or 0)
        product.date = data.get('date')
        product.unit_price = float(data.get('unit_price') or 0)
        product.type_of_stock = data.get('type_of_stock')
        product.description = data.get('description')
        product.expiry_date = data.get('expiry_date')
        product.cat_name = category_obj  # Assign the selected category

        # Save the updated product
        product.save()

        # Redirect to a relevant page (e.g., product list or product detail page)
        return redirect('displayproduce')

    # Pass the product to the template for rendering.
    context = {
        'product' : product,
        'all_categories': all_categories,
    }
    return render(request, 'producteditor.html', context)    




###############################################
## This is the edite inventory view.
# @manager_required
def editinventory(request, id):
    sent_id = id
    invent = Inventory.objects.get(id=sent_id)
    product = Product.objects.all()
    branch = Branch.objects.all()
    
    if request.method == 'POST':
        data = request.POST

        # Debugging: Print submitted data
        print("Form submitted:", data)  

        try:
            # Get the product and branch
            product_id = data.get('product')
            branch_id = data.get('branch')
            product_obj = Product.objects.get(pk=product_id)
            branch_obj = Branch.objects.get(pk=branch_id)

        # Update the inventory item
            invent.buying_price = data.get('buying_price')
            invent.unit_price = data.get('unit_price')
            invent.unite_of_measure = data.get('unite_of_measure')
            invent.description = data.get('description')
            invent.expiry_date = data.get('expiry_date')
            invent.stock_quantity = data.get('stock_quantity')
            invent.reorder_level = data.get('reorder_level')
            invent.product = product_obj
            invent.branch = branch_obj
            invent.save()
            print("Inventory updated successfully!")

            return redirect('products')  # Redirect to the products page
        except Exception as e:
            print(f"Error updating inventory: {e}")


    context = { 
        'edit_details' : invent,
        'products': product,
        'branches': branch,
    }
    return render(request, 'edit.html', context)









################################################
## This view is to handle the a product being deleted.
def deletepage(request, id):

    # Fetch the inventory record. 
    to_delete = Inventory.objects.get(id=id)  

    if request.method == 'POST':
        # Delete the inventory record.
        data = request.POST
        to_delete.delete()
        return redirect('products')

    context = {
        'details' : to_delete,
    }
    return render(request, 'delete.html', context) 









###############################################
## This view is meant to populate our database in a way of adding products in our database.
# This going to be mainly for displaying details of the product that is selected to be sold.
# @login_required
# @user_passes_test(is_owner)
# @manager_required
def addproduct(request):

    # Message to be passed through a context to be rendered in html. 
    reply = 'Product added successfully'


    if request.method == 'POST':
        data = request.POST 

        cat_name = data.get('cat_name')
        cat_obj = Category.objects.get(pk=cat_name)
        new_product = Product(
            supplier_name = data.get('supplier_name'),
            product_name =data.get('product_name'),
            sku = data.get('sku'),
            buying_price = data.get('buying_price'),
            quantity = int(data.get ('quantity')),
            date = data.get ('date'),
            unit_price = float(data.get('unit_price')),
            type_of_stock = data.get('type_of_stock'),
            description =data.get('description'),
            expiry_date = data.get('expiry_date'),
            cat_name = cat_obj
        )
        new_product.save()

        print("Redirecting to products...")

        return redirect('displayproduce')
        


    categories = Category.objects.all()
    context = {
        'all_categories' : categories,
        'message': reply,
    }


    return render(request, 'productentry.html', context)










##########################################################
### This is the view for collecting the Branch information.
# This will collect data from the user and store it in the database.
# @login_required
# @user_passes_test(is_owner)
# @manager_required
def branchpage(request):
    if request.method == 'POST':
        data = request.POST 

        product = data.get('product')
        product_obj = Product.objects.get(pk=product)
        new_product = Branch(
            branch_name = data.get('branch_name'),
            contact = data.get('contact'),
            location = data.get('location'),
            product = product_obj, 
        )
        new_product.save()


    categories = Product.objects.all()
    context = {
        'all' : categories
    }


    return render(request, 'category.html', context)
    







################################################
### This is the inventory logic for entry of an inventory.
# This is meant to track the transactions in every branch.
# It will have a foreighn key from the product and branch to know from were it was sold.
# @manager_required
def inventory(request):
    if request.method == 'POST':
        data = request.POST

        product = data.get('product')
        branch = data.get('branch')
        branch_obj = Branch.objects.get(pk=branch)
        product_obj = Product.objects.get(pk=product)

        # You can create or update the inventory record from here. 
        inventory_record, created = Inventory.objects.get_or_create(
            product=product_obj,
            branch=branch_obj,
            defaults={
                'buying_price': data.get('buying_price'),
                'unit_price': data.get('unit_price'),
                'unite_of_measure': data.get('unite_of_measure'),
                'description': data.get('description'),
                'expiry_date': data.get('expiry_date'),
                'stock_quantity': int(data.get('stock_quantity') or 0),
                'reorder_level': data.get('reorder_level'),
            }
        )

        if not created:
            # If the inventory record already exists, update the stock quantity
            inventory_record.stock_quantity += int(data.get('stock_quantity') or 0)
            inventory_record.buying_price = data.get('buying_price')
            inventory_record.unit_price = data.get('unit_price')
            inventory_record.unite_of_measure = data.get('unite_of_measure')
            inventory_record.description = data.get('description')
            inventory_record.expiry_date = data.get('expiry_date')
            inventory_record.reorder_level = data.get('reorder_level')
            inventory_record.save()

        return redirect('products')  # Redirect to the products page

    products = Product.objects.all()
    branches = Branch.objects.all()
    context = {
        'all_products': products,
        'all_branches': branches,
    }
    return render(request, 'inventory.html', context)






##################################################
## This view is for redirecting users that want to log out.
# They a redirected to the home page which is the index page of the system.
def logout_user(request):
    logout(request)


    return redirect('/') 






##################################################
## The customer page.
# This form recording the customers relationship with business for one to qualify for credisales.
# @role_required(['sales_agent', 'manager'])
def customerpage(request):
    if request.method == 'POST':
        data = request.POST

        new_customer = Customer(
            full_names = data.get('full_names'),
            email = data.get('email'),
            contact = data.get('contact'),
            address = data.get('address'),
            gender = data.get('gender'),
        )
        new_customer.save()
    return render(request, 'customer.html')








########################################################
## This is a view for the creditsale.
# This is for tracking which branch has transacted a product.
# And which branch has done so.
# @role_required(['sales_agent', 'manager'])   
def creditpage(request):
    if request.method == 'POST':
        data = request.POST
        customer = data.get('customer')
        product = data.get('product')
        branch = data.get('branch')
        customer_obj = Customer.objects.get(pk=customer)
        product_obj = Product.objects.get(pk=product)
        branchobj = Branch.objects.get(pk=branch)

        # Get numeric inputs safely
        # if the input is none the result is returned to none and prevents crushing because of converting a none to an int.
        # This bring out this structure of int(data.get('quantity') or 0 )  
        quantity = int(data.get('quantity') or 0)
        unit_price = int(data.get('unit_price') or 0)
        amount_paid = int(data.get('amount_paid') or 0)

        # Auto-calculate totals
        total_price = quantity * unit_price
        balance_due = total_price - amount_paid

        # Parse due date
        try:
            # This line captures the due date that is posted in the form and django transforms it to what my model expects.  
            due_date = datetime.strptime(data.get('due_date'), "%Y-%m-%d").date()
        except:
            due_date = None
        
        # Creting a new object. 
        new_credit = Creditsale(
            quantity = quantity, 
            unit_price = unit_price,
            total_price = total_price,
            balance_due = balance_due,
            sales_agent = data.get('sales_agent'),
            date_of_sale = data.get('data_of_sales'),
            due_date = due_date,
            payment_status = data.get('payment_status'),
            amount_paid = amount_paid,
            customer = customer_obj,
            product = product_obj,
            branch = branchobj,
        ) 
        # Saving the new created object.
        new_credit.save()


    # Using a context to loop through the models. 
    produk = Product.objects.all()
    brank = Branch.objects.all()
    customers = Customer.objects.all()
    context = {
        'all_products' : produk,
        'all_branches' : brank,
        'all_customers' : customers,
    }

    return render(request, 'creditsale.html', context)






#######################################################
## A view to querry data to the dashboard of mr orban.
# @owner_required
def dashboard(request):

    
    # Query all branches
    branch = Branch.objects.all()

    # Context for the dashboard


    context = {
        'branchdetails' : branch,             
    }

    return render(redirect, 'dashboard.html', context)







#######################################################
## These a dashboard reports. 
## This is the view that handles the branch details.
# it will contain a dynamic url that will querry data, for each branch.
# @owner_required
def branchdetail(request, id):
    # Get the branch object
    branch = get_object_or_404(Branch, pk=id)

    # Query reorder levels for the branch
    reorder_levels = Inventory.objects.filter(branch_id=id, stock_quantity__lte=models.F('reorder_level'))

    # Query expired products for the branch
    expired_products = Inventory.objects.filter(branch_id=id, expiry_date__lt=date.today())

    # Query customers who have taken products on credit
    credit_customers = Creditsale.objects.filter(branch_id=id, balance_due__gt=0).select_related('customer')

    # Calculate total creditsales for a branch
    total_sales = Creditsale.objects.filter(branch=branch).aggregate(total=Sum('total_price'))['total'] or 0

    # Query expired products for the branch (via Inventory)
    expired_products_count = Inventory.objects.filter(branch=branch, product__expiry_date__lt=date.today()).count()

    # Count total products for the branch (via Inventory)
    total_products = Inventory.objects.filter(branch=branch).count()

    # Count total credit sales for the branch
    total_creditsales = Creditsale.objects.filter(branch=branch).count()

    # Get inventory for the branch
    inventory = Inventory.objects.filter(branch=branch)

    

    # Filter sales based on the branch
    # Passing total sales bassed on the branch 
    sales = Receipt.objects.filter(branch=branch).count()

    
    # Pass the data to the template
    context = {
        'name': branch,
        'total_sales': total_sales,
        'expired_products_count': expired_products_count,
        'total_products': total_products,
        'total_creditsales': total_creditsales,
        'inventory': inventory,
        'reorder_levels': reorder_levels,
        'expired_products': expired_products,
        'credit_customers': credit_customers,
        'sales': sales,
    }

    return render(request, 'branchdetail.html', context)







########################################################
## This code finds the inventory record of a product and branch.
# This code checks stock availability and ensures there is enough to make a sale.
# The code also updataes the new quantity in the database.    
# @login_required
# @role_required(['sales_agent', 'manager'])
def pos_sale(request, id):

    try:
        # Fetch the specific inventory record based on the ID from the URL
        selected_inventory = Inventory.objects.get(pk=id)
    except Inventory.DoesNotExist:
        return render(request, '404.html', {'error': 'Inventory not found'})  # Handle missing inventory gracefully

    inventory = Inventory.objects.get(pk=id)
    if request.method == 'POST':
        data = request.POST

        # Get the product and the branch
        product_id = data.get('product')
        branch_id = data.get('branch')
        quantity = int(data.get('quantity') or 0)
        amount_paid = float(data.get('amount_paid') or 0)

        # Fetch the inventory record
        inventory = Inventory.objects.filter(product_id=product_id, branch_id=branch_id).first()

        if not inventory:
            context = {
                'error': 'Inventory record not found for the selected product and branch.',
                'products': Product.objects.all(),
                'branches': Branch.objects.all(),
                'selected_product': selected_inventory.product,  # Pass the selected product
            }
            return render(request, 'sales.html', context)

        # Check if there is enough stock in the inventory
        if inventory.stock_quantity < quantity:
            context = {
                'error': 'Insufficient stock for this product in the selected branch.',
                'products': Product.objects.all(),
                'branches': Branch.objects.all(),
                'selected_product': selected_inventory.product,  # Pass the selected product
            }
            return render(request, 'sales.html', context)

        # Calculate total price and balance
        total_price = inventory.unit_price * quantity
        balance = total_price - amount_paid

        # --- CHECKING FOR DUPLICATES ---
        from datetime import date
        duplicate = Receipt.objects.filter(
            product_id=product_id,
            branch_id=branch_id,
            quantity=quantity,
            total_price=total_price,
            amount_paid=amount_paid,
            date_of_sale=date.today()
        ).exists()
        if duplicate:
            context = {
                'error': 'This sale has already been registered today!',
                'products': Product.objects.all(),
                'branches': Branch.objects.all(),
                'selected_product': selected_inventory.product,
            }
            return render(request, 'sales.html', context)
        # --- CHECK END ---

        # Deduct the sold quantity from the inventory
        inventory.stock_quantity -= quantity
        inventory.save()

        # Deduct the sold quantity from the product's total quantity
        product = inventory.product
        product.quantity -= quantity
        product.save()

        # Save the sale in the Receipt model
        receipt = Receipt(
            product=product,
            branch=inventory.branch,
            quantity=quantity,
            unit_price=inventory.unit_price,
            total_price=total_price,
            amount_paid=amount_paid,
            balance=balance,
            date_of_sale=date.today(),
        )
        receipt.save()

        # Pass the receipt to the template to show it
        inventories = Inventory.objects.all()
        context = {
            'products': Product.objects.all(),
            'branches': Branch.objects.all(),
            'selected_product': selected_inventory.product,
            'selected_branch': selected_inventory.branch,
            'inventory': inventories,
            'receipt': receipt,  # This will be used to show the receipt
        }
        return render(request, 'sales.html', context)

    # GET request — show form for POS sale
    inventories = Inventory.objects.all()
    context = {
        'products': Product.objects.all(),
        'branches': Branch.objects.all(),

        # Pass the selected product.
        'selected_product': selected_inventory.product,
        'selected_branch': selected_inventory.branch,

        # Pass all the inventories to the template. 
        'inventory' : inventories, # 
    }
    return render(request, 'sales.html', context)



##################################################
## The manager's landing page.
# On loging in the manager lands on this page after loging in.
def managerview(request):
    return render(request, 'managerland.html')



#################################################
## The salesagent landing page.
def salesagentland(request):
    return render(request, 'salesagent.html')













