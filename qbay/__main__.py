"""
main file to import all models
"""
from qbay import *
from qbay.cli import login_page, register_page, create_product_page, \
    update_product_page, update_user_page, place_order_page


def main():
    while True:
        print('\n' * 3)
        selection = input('''Welcome. Please make a selection. 
        1 : login
        2 : register
        3 : user profile update
        4 : user home page
        5 : place order''')
        selection = selection.strip()
        if selection == '1':
            user = login_page()
            if user:
                print(f'welcome {user.username}')
                break
            else:
                print('login failed')
        elif selection == '2':
            register_page()
        elif selection == '3':
            update_user_page()
        elif selection == '4':
            print("Please choose an option:")
            print("  1. Create a product")
            print("  2. Update a product")
            select2 = input()
            if select2 == '1':
                create_product_page()
            elif select2 == '2':
                update_product_page()
        elif selection == '5':
            place_order_page()


if __name__ == '__main__':
    main()
