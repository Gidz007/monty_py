## Karibu Groceries Ltd
- An inventory system is required to solve a problem of record keeping in the business.
- The manager optted for an inventory system to be put in place to help out.

## Project requirements.
- Kgl deals in cereal produce.
- Beans, Grain Maize, Cow peas, G-nuts, Soybeans
- Individual dealers with produce not less than a tone (1000kg).
- Gets produce from its two farms from Maganjo and Matugga.
- Has two branches
- Has a manager and 2 attendants in both the branches.

## Project execution.
- creation of models
- creation of views to connect python logic to html.
- Html that will be viewed by the customer.

## Models.                  Related to
- Category                    --------
- Product                     Category
- Branch                      Product (foreighnkey)
- inventory                   Product + Branch
- Stock                       Product + Branch
- Customer                    Creditsale
- Creditsale                  Customer + Product + Branch

## The fllow of code. 
- You make sure you have your models right
- Then here we go to the views, this actis like the brain of our whole project.
- then we can use crud.
- Create
- Reading 
- Updaate
- Delete.

## The reason for the project you ask your self 
- why a you requesting for the data and what a you going to use the data for.


# you can also use the the python shell for testing your project.

## In the view.py file the logic there is when a link is trigered by a customer


## When working with python manage.py shell.
- We have the crud features.
- for the models to get a model you import it in the shell. by running.

# form kglapp.model import Product
- This will give you the Porduct model
# from datetime import date
- This will give you the current date.
# Here is how you can try CRUD.
# newproduct = Product(item_name = 'Maize', ...........)
- This will create a new product in our model,

## In python shell, we have an anotation.
- There a several, and they include.
- startwith done by __startwith
- contains,
- exact
- endswith
- in
- oposite of not startswith, endswith, 

# Give me alist were the price is less than 50,000.
- we have look ups, like
- gt meaning greater than
- lt ---- lessthan
- gte ------ Greater than or equal to
- lte ------- less than or equal to
- We also have filter, get, all, startswith, contains, anotation. 

## The search logic for the nav bar.
- def search(request):
    if request.method == 'POST'
        data = request.POST
        search_term = data.get('the name for the search form')
        results = Product.object.filter(name__contains=search_term).

## The logic of displaying all products, all sales, and reports on the dashboard.
- def dashboard(request):
    all_out = Product.objects.filter(quantity__lt=2kgs)
    all_products = Products.objects.all()
    productsnumber = Product.objects.all()
    productcount = len(productsnumber)

    context = {
        "all_out" : all_out
        "all_products" : all_products
        "productcount" : productcount
    }

## Making reports using filters.
# Reading data,
# Updating data,
# Deleting data,
