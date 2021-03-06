## "My Simple eCart Project"

This is a simple REST API that I created to imitate an online shopping service. Users can create accounts as Customers or Vendors, each with specific functionalities. Vendors are able to update their personal information or perform CRUD operations on products that they are selling. On the flip side, customers can also update their personal information while being able to access a list of all products sold by all vendors, and can perform CRUD operations on products in their cart.  
The purpose of this project was to explore Django and Django REST Framework and to use them to practice building a web application in Python. I also wanted to practice creating a database that contains many tables and establishing different types of relationships between the tables using Django's default ORM layer. For example, customers can hold many products in their carts, many customers can have the same product in their carts, etc.. In short, I create the backend of a web application. As I am not all that interested in frontend, I decided to leave out any frontend userface for users to make calls to the API requests. If I am feeling bored at some point in the future, I may come back to this project and finally implement the frontend (possibly with Angular/Typescript)


To get started running this appliation on your local machine, you have to install the required Python libraries, which are listed in the 'requirements.txt' file. To avoid installing them individually, you can run the following command below in your command prompt (I also recommend creating a virtual environment to run the project in):

```
  pip install -r requirements.txt
```

After installing the necessary packages, you have to set up the database by using the 'makemigrations' and 'migrate' commands that Django includes in the manage.py file. To do this, run the following commands:

```
  python manage.py makemigrations
  python manage.py migrate
```

After setting up the tables in the database, we need to fill the tables with some sample data to test the functionality of the app (the process for doing so is in the section below). Finally, you can run the project and open the localhost url into your preferred browser. To run the project, we can call the 'runserver' command:

```
  python manage.py runserver
```

and the base localhost address is going to be http://localhost:8000/

### Setting Up Database
Now that the database has been migrated, let's set up the tables by inserting some data into them. We'll be working exclusively with JSON type data, and the entries we will be entering can be found in the 'successful-tests.txt' file. While entering the data, order matters to an extent, as the relationships in some tables will not allow for an object of one type to be created while an object of another type does not exist. For this project, we should enter the Customer/Vendor data first, followed by VendorProduct data, and then finishing off with CartProduct data. 
