from qbay.models import login, Product, register, create_product, \
    update_product, User, user_update


def login_page():
    '''
    This function provides the CLI for the login function. It takes a user's
    email and password and input and returns their account as output.
    '''
    email = input('Please input email:')
    password = input('Please input password:')
    return login(email, password)


def register_page():
    '''
    This function provides the CLI for the register function. It takes a user's
    email and password as input, and requires that the user confirm their
    password. Returns None.
    '''
    email = input('Please input email: ')
    password = input('Please input password: ')
    password_twice = input('Please input the password again: ')
    if password != password_twice:
        print('Failed - password entered not the same')
    elif register('Unnamed user', email, password):
        print('Registration succceeded')
    else:
        print('Failed - input does not meet one of the requirements.')


def update_user_page():
    '''
    update_user_page takes 0 parameters.
    This provides functionality for the CLI
    to provide the ability to update a user's
    information.
    '''
    # Test case:
    # register('u0 r3 1', 'testr3-1@test.com', '123aBc!')

    current_name = input(
        """Please enter the username of the user you want to update: """)

    # set current_user to the user with username = current_name
    current_user = User.query.filter_by(username=current_name).first()

    # set not_existing to a boolean whether User exists or not
    not_existing = User.query.filter_by(username=current_name).first() is None

    # loop until valid username is inputted
    while (not_existing):
        print("User does not exist.")
        current_name = input(
            """Please enter the username of the user you want to update: """)
        current_user = User.query.filter_by(username=current_name).first()
        not_existing = User.query.filter_by(username=current_name)\
            .first() is None

    # to avoid any errors with our user_update function,
    # set placeholders if they're empty.
    if not(current_user.shipping_addr):
        current_user.shipping_addr = "104 Park St"

    if not(current_user.postal_code):
        current_user.postal_code = "K7K 1M9"

    current_shipp_addr = current_user.shipping_addr
    current_postal_code = current_user.postal_code

    print("""
    1. Update username
    2. Update shipping address
    3. Update postal code
    4. Update username & shipping address
    5. Update username & postal code
    6. Update shipping address & postal code
    7. Update username & shipping address & postal code
    8. Exit
    """)

    flag = int(input("What option would you like to choose: "))

    if flag == 1:
        # Update username option
        updated_username = input("Please enter your new username: ")

        # Print user_update function incase of any failures.
        print(user_update(current_name, new_username=updated_username,
                          new_shipping_address=current_shipp_addr,
                          new_postal_code=current_postal_code))

    elif flag == 2:
        # Update shipping address
        updated_shipping_addr = input("""
        Please enter your new shipping address:
        """)

        print(user_update(current_name, new_username=current_name,
                          new_shipping_address=updated_shipping_addr,
                          new_postal_code=current_postal_code))

    elif flag == 3:
        # Update postal code
        updated_postal_code = input("Please enter your new postal code: ")

        print(user_update(current_name, new_username=current_name,
                          new_shipping_address=current_shipp_addr,
                          new_postal_code=updated_postal_code))

    elif flag == 4:
        # Update username & shipping address
        updated_username = input("Please enter your new username: ")
        updated_shipping_addr = input("""
        Please enter your new shipping address:
        """)

        print(user_update(current_name, new_username=updated_username,
                          new_shipping_address=updated_shipping_addr,
                          new_postal_code=current_postal_code))

    elif flag == 5:
        # Update username & postal code
        updated_username = input("Please enter your new username: ")
        updated_postal_code = input("Please enter your new postal code: ")

        print(user_update(current_name, new_username=updated_username,
                          new_shipping_address=current_shipp_addr,
                          new_postal_code=updated_postal_code))

    elif flag == 6:
        # Update shipping & postal
        updated_shipping_addr = input("""
        Please enter your new shipping address:
        """)
        updated_postal_code = input("Please enter your new postal code: ")

        print(user_update(current_name, new_username=current_name,
                          new_shipping_address=updated_shipping_addr,
                          new_postal_code=updated_postal_code))

    elif flag == 7:
        # Update username & shipping address & postal code
        updated_username = input("Please enter your new username: ")
        updated_shipping_addr = input("""
        Please enter your new shipping address:
        """)
        updated_postal_code = input("Please enter your new postal code: ")

        print(user_update(current_name, new_username=updated_username,
                          new_shipping_address=updated_shipping_addr,
                          new_postal_code=updated_postal_code))

    elif flag == 8:
        exit()


def create_product_page():
    '''
    This function provides the CLI interface
    to create a product in the database.
    The user has the ability to insert a title,
    description, and price
    '''
    title = input('Please input title: ')
    desc = input('Please input description: ')
    price = int(input('Please enter price: '))
    date = input('Please input date: ')
    email = input('Please input email: ')

    if create_product(title, desc, price, date, email):
        print('Product succesfully created')
    else:
        print('Product Creation Failed')


def update_product_page():
    '''
    This function provides the CLI interface
    to update a product in the database.
    The user has the option to update the price, title or description.

    '''
    # ask user for id of the product to update
    id = int(input('Please input the id of the product you want to update: '))

    # store the current product in variable
    currentProduct = Product.query.filter_by(id=id).first()

    # current product information
    currentPrice = currentProduct.price
    currentTitle = currentProduct.title
    currentDesc = currentProduct.desc

    flag = True
    while flag:
        if (not currentProduct):  # checks if product with id exists
            print('Product does not exist')
            break  # exit loop

        print("""
        1. Update price
        2. Update title
        3. Update description
        4. Update price and title
        5. Update price and description
        6. Update title and description
        7. Update price, title, description
        8. Exit
         """)

        flag = input("What would you like to do: ")  # prompt user
        if flag == "1":
            newPrice = int(input('Please enter the new price: '))
            update_product(id, newPrice=newPrice, newTitle=currentTitle,
                           newDesc=currentDesc)  # only update price
            print('Updated price ')
        elif flag == "2":
            newTitle = input('Please enter the new title: ')
            update_product(id, newPrice=currentPrice, newTitle=newTitle,
                           newDesc=currentDesc)  # only update title
            print('Updated title')
        elif flag == "3":
            # only update description
            newDesc = input('Please enter the new description: ')
            update_product(id, newPrice=currentPrice,
                           newTitle=currentTitle, newDesc=newDesc)
            print('Updated description')
        elif flag == "4":
            # only update price and title
            newPrice = int(input('Please enter the new price: '))
            newTitle = input('Please enter the new title: ')
            update_product(id, newPrice=newPrice,
                           newTitle=newTitle, newDesc=currentDesc)
            print('Updated price and title')
        elif flag == "5":
            # only update price and description
            newPrice = int(input('Please enter the new price: '))
            newDesc = input('Please enter the new description: ')
            update_product(id, newPrice=newPrice,
                           newTitle=currentTitle, newDesc=newDesc)
            print('Updated price and description')
        elif flag == "6":
            # only update title and description
            newTitle = input('Please enter the new title: ')
            newDesc = input('Please enter the new description: ')
            update_product(id, newPrice=currentPrice,
                           newTitle=newTitle, newDesc=newDesc)
            print('Updated title and description')
        elif flag == "7":
            #  update price, title, and description
            newPrice = int(input('Please enter the new price: '))
            newTitle = input('Please enter the new title: ')
            newDesc = input('Please enter the new description: ')
            update_product(id, newPrice=newPrice,
                           newTitle=newTitle, newDesc=newDesc)
            print('Updated price, title and description')
        elif flag == "8":
            exit()


def place_order_page():
    '''
    This function provides the CLI interface
    to order a product.
    The user has the option to order any order given the id.
    '''

    current_name = input(
        """Enter your username to purchase a product: """)

    # set current_user to the user with username = current_name
    current_user = User.query.filter_by(username=current_name).first()
    user_email = current_user.email

    # set not_existing to a boolean whether User exists or not
    not_existing = User.query.filter_by(username=current_name).first() is None

    # loop until valid username is inputted
    while (not_existing):
        print("User does not exist.")
        current_name = input(
            """Enter your username to purchase a product or exit to leave: """)
        current_user = User.query.filter_by(username=current_name).first()
        not_existing = User.query.filter_by(username=current_name)\
            .first() is None
        if current_name == "exit":
            exit()

    title = input(
        'Please input the title of the product you want to purchase: ')
    currentProduct = Product.query.filter_by(title=title).first()
    not_existing = Product.query.filter_by(title=title).first() is None

    if (not_existing):  # checks if product with title=title exists
        print('Product does not exist')
        exit()  # exit loop

    # current product to be purchased information
    currentPrice = currentProduct.price
    currentTitle = currentProduct.title
    currentDesc = currentProduct.desc
    user_email = current_user.email

    flag = True
    while flag:

        print("""
        1. Purchase Product
        2. See Product Information
        3. Exit
         """)

        flag = input("What would you like to do: ")

        if flag == 1:
            # purchaseProduct(user_email, currentTitle)
            print("Product purchased.")

        elif flag == 2:
            print('The title of the product is: ', currentTitle)
            print('The price of the product is: ', currentPrice)
            print('The description of the product is: ', currentDesc)

        elif flag == 3:
            exit()
