from qbay.models import register, login, create_product, update_product
from qbay.models import user_update, purchase_product


def test_r1_1_non_empty():
    '''
    Testing R1-1: Both the email and password cannot be empty.
    '''
    assert register('', 'test1@testr1.com', '123456') is False
    assert register('u1 1', '', '123456') is False
    assert register('', '', '123456') is False


def test_r1_2_unique_email():
    '''
    Testing R1-2: A user is uniquely identified by his/her email address.
    '''
    assert register('u1 2 0', 'testr1_2@test.com', '123aBc!') is True
    assert register('u1 2 1', 'testr1_2@test.com', '123aBc!') is False


def test_r1_3_rfc_5322():
    '''
    Testing R1-3: The email has to follow addr-spec defined in RFC 5322.
    '''
    assert register('u1 3 0', 'testr1_3@test.com', '123aBc!') is True
    assert register('u1 3 1', 'test3.com', '123aBc!') is False
    assert register('u1 3 2', 'test3@com', '123aBc!') is False
    assert register('u1 3 3', '@test3.com', '123aBc!') is False


def test_r1_4_password_complexity():
    '''
    Testing R1-4: Password has to meet the required complexity.
    minimum length 6
    at least one upper case
    at least one lower case
    at least one special character
    '''
    assert register('u1 4 0', 'testr1-4-0@test.com', '123aBc!') is True
    assert register('u1 4 1', 'testr1-4-1@test.com', '123abc!') is False
    assert register('u1 4 2', 'testr1-4-2@test.com', '123ABC!') is False
    assert register('u1 4 3', 'testr1-4-3@test.com', 'aBcDeF') is False
    assert register('u1 4 4', 'testr1-4-4@test.com', '123456!') is False


def test_r1_5_user_name_rules():
    '''
    Testing R1-5: User name has to be non-empty, alphanumeric-only and
    space allowed only if it is not as the prefix or suffix.
    '''
    assert register('u1 5 0', 'testr1-5-0@test.com', '123aBc!') is True
    assert register('', 'testr1-5-1@test.com', '123aBc!') is False
    assert register('u1-5-2', 'testr1-5-2@test.com', '123aBc!') is False
    assert register('u1 5 3 ', 'testr1-5-3@test.com', '123aBc!') is False
    assert register(' u1 5 4', 'testr1-5-4@test.com', '123aBc!') is False
    assert register(' u1 5 5 ', 'testr1-5-5@test.com', '123aBc!') is False


def test_r1_6_pasword_len():
    '''
    Testing R1-6: User name has to be longer than 2 characters 
    and less than 20 characters.
    '''
    assert register('u1 6 0', 'testr1-6-0@test.com', '123aBc!') is True
    assert register('u1', 'testr1-6-1@test.com', '123aBc!') is False
    assert register('u1' + 'a' * 20, 'testr1-6-2@test.com', '123aBc!') is False


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''

    assert register('u1 7 0', 'testr1-7-0@test.com', '123aBc!') is True
    assert register('u1 7 1', 'testr1-7-1@test.com', '123aBc!') is True
    assert register('u1 7 2', 'testr1-7-0@test.com', '123aBc!') is False


def test_r1_8_shipping_empty():
    '''
    Testing R1-8: Shipping address is empty at the time of registration.
    '''
    register('u1 8', 'testr1-8@test.com', '123aBc!')
    newu = login('testr1-8@test.com', '123aBc!')
    assert newu.shipping_addr == ""


def test_r1_9_postal_empty():
    '''
    Testing R1-9: Postal code is empty at the time of registration.
    '''
    register('u1 9', 'testr1-9@test.com', '123aBc!')
    newu = login('testr1-9@test.com', '123aBc!')
    assert newu.postal_code == ""


def test_r1_10_balance_100():
    '''
    Testing R1-10: Balance should be initialized as 100 at the time of 
    registration. (free $100 dollar signup bonus).
    '''
    register('u1 10', 'testr1-10@test.com', '123aBc!')
    newu = login('testr1-10@test.com', '123aBc!')
    assert newu.balance == 100


def test_r2_1_login_possible():
    '''
    Testing R2-1: A user can log in using her/his email address
      and the password.
    '''
    register('u0 r2 1', 'testr2-1@test.com', '123aBc!')

    user = login('testr2-1@test.com', "123aBc!")
    assert user is not None
    user2 = login('testr2-1@test.com', '1234567')
    assert user2 is False


def test_r2_2_login_correct():
    '''
    Testing R2-2: A user can log in using her/his email address
      and the password.
    '''
    register('u0 r2 2', 'testr2-2@test.com', '123aBc!')

    assert login('', '') is False
    assert login('john@gmail.com', '') is False
    assert login('', 'abcde123!') is False
    assert login('john@gmail.com', 'abcd') is False
    assert login('john.com', 'abcdD12!') is False
    assert login('john@gmail.com', 'abcDE!') is False
    assert login('john@gmail.com', 'ABCD123!') is False
    assert login('john@gmail.com', 'Abcdefg!') is False
    assert login('john@gmail.com', 'abcde123!') is False
    assert login('john@gmail.com', 'Abcdefg1') is False


def test_r3_1_user_update():
    '''
    Testing R3-1: A user should only be able to update their
      username, shipping_address, and postal_code.
    '''
    register('u0 r3 1', 'testr3-1@test.com', '123aBc!')

    new_user = login('testr3-1@test.com', "123aBc!")

    user_update('u0 r3 1', new_username='abc',
                new_shipping_address='140 Park St',
                new_postal_code='K7K 1J5')

    assert new_user.username == "abc"

    # Shouldn't be able to update more than 3 arguments.
    # Should only update user, shipping, and postal
    assert user_update('abc', new_username='u012',
                       new_shipping_address='120 Gilmore St',
                       new_postal_code='K7K 1J5',
                       new_password='newpassword') is False

    assert user_update('u012', new_username='u012',
                       new_shipping_address='120 Gilmore St',
                       new_postal_code='K7K 1J5',
                       new_email='newemail@gmail.com') is False


def test_r3_2_address_rules():
    '''
    Testing R3-2: Shipping_address should be non-empty,
    alphanumeric-only, and no special characters such as !
    '''

    # alphanumerics only.

    register('u0 r3 2', 'testr3-2@test.com', '123aBc!')

    new_user = login('testr3-2@test.com', "123aBc!")

    user_update('u0 r3 2', new_username='u0 r3 2',
                new_shipping_address='51 Colborne St',
                new_postal_code='K7K 1J5') is True

    assert new_user.shipping_addr == "51 Colborne St"

    # has special character
    assert user_update('u0 r3 2', new_username='u0 r3 2',
                       new_shipping_address='#120 Gilmore',
                       new_postal_code='K7K 1J5') is False

    assert user_update('u0 r3 2', new_username='u0 r3 2',
                       new_shipping_address='120-Gilmore-St!',
                       new_postal_code='K7K 1J5') is False

    # empty, therefore false.
    assert user_update('u0 r3 2', new_username='u0 r3 2',
                       new_shipping_address='',
                       new_postal_code='K7K 1J5') is False


def test_r3_3_postal_code():
    '''
    Testing R3-3: Postal code has to be a valid Canadian
    postal code.
    Make use of regular expressions to ensure the validity.
    '''
    register('u0 r3 3', 'testr3-3@test.com', '123aBc!')
    assert user_update('u0 r3 3', new_username='u0 r3 3',
                       new_shipping_address='51 Colborne St',
                       new_postal_code='K7K 1J5') is True

    # Not following the Alphabet-Numeral-Alphabet pattern.
    assert user_update('u0 r3 3', new_username='u0 r3 3',
                       new_shipping_address='51 Colborne St',
                       new_postal_code='K77 1J5') is False
    # Missing space between 3rd/fourth character.
    assert user_update('u0 r3 3', new_username='u0 r3 3',
                       new_shipping_address='51 Colborne St',
                       new_postal_code='K7K1J5') is False
    # Non alpha-numeric character.
    assert user_update('u0 r3 3', new_username='u0 r3 3',
                       new_shipping_address='51 Colborne St',
                       new_postal_code='K7@ 1J5') is False


def test_r3_4_username_requirement():
    '''
    Testing R3-4: Username follows the requirements from the
    registration.
    '''
    register('u0 r3 4', 'testr3-4@test.com', '123aBc!')
    assert user_update('u0 r3 4', new_username='u1 r3 4',
                       new_shipping_address='51 Colborne St',
                       new_postal_code='K7K 1J5') is True

    # Can't have a space as a prefix.
    assert user_update('u0 r3 4', new_username=' u123',
                       new_shipping_address='51 Colborne St',
                       new_postal_code='K7K 1J5') is False
    # Has to be longer than 2 characters.
    assert user_update('u0 r3 4', new_username='u1',
                       new_shipping_address='51 Colborne St',
                       new_postal_code='K7K 1J5') is False
    # Alphanumeric only.
    assert user_update('u0 r3 4', new_username='u1!@#',
                       new_shipping_address='51 Colborne St',
                       new_postal_code='K7K 1J5') is False


def test_r4_1_alphanumeric_only():
    '''
    R4-1: The title of product is alphanumeric-only, 
    and space allowed only if
    not as prefix and suffix.
    '''
    register('u0 r4 1', 'testr4-1@test.com', '123aBc!')
    assert create_product('Iphone 4 1', 't' * 21, 20,
                          None, "testr4-1@test.com") is True
    assert create_product('Test-1-0', 't' * 21, 20, None,
                          "testr4-1@test.com") is False
    assert create_product('Test 1 0 ', 't' * 21, 20, None,
                          "testr4-1@test.com") is False
    assert create_product(' Test 1 0', 't' * 21, 20, None,
                          "testr4-1@test.com") is False
    assert create_product(' Test 1 0 ', 't' * 21, 20,
                          None, "testr4-1@test.com") is False
    assert create_product('', 't' * 21, 20, None, "testr4-1@test.com") is False


def test_r4_2_title_char():
    '''
    R4-2: The title of the product is no longer than 80 characters.
    '''
    register('u0 r4 2', 'testr4-2@test.com', '123aBc!')
    assert create_product('Iphone 4 2', 't' * 21, 20,
                          None, "testr4-2@test.com") is True
    assert create_product('Iphone 4 2' * 15, 't' * 21, 20,
                          None, "testr4-2@test.com") is False


def test_r4_3_descrip_length():
    '''
    R4-3: The description of the product can be arbitrary characters,
    with a minimum length of 20 characters and a maximum of 2000 characters.
    '''
    register('u0 r4 3', 'testr4-3@test.com', '123aBc!')
    assert create_product('Iphone 4 3', 't' * 21, 15,
                          None, 'testr4-3@test.com') is True
    assert create_product('Iphone431', 't' * 10, 15,
                          None, 'testr4-3@test.com') is False
    assert create_product('Iphone 4 3 2', 't' * 2100, 15,
                          None, 'testr4-3@test.com') is False


def test_r4_4_compare_descrip_title():
    '''
    R4-4: Description has to be longer than the product's title.
    '''
    register('u0 r4 4', 'testr4-4@test.com', '123aBc!')
    assert create_product('Iphone 4 4', 't' * 21, 15,
                          None, 'testr4-4@test.com') is True
    assert create_product('Iphone 4 4' * 8, 't' * 21, 15,
                          None, 'testr4-4@test.com') is False


def test_r4_5_price_range():
    '''
    R4-5: Price has to be of range [10, 10000].
    '''
    register('u0 r4 5', 'testr4-5@test.com', '123aBc!')
    assert create_product('Iphone 4 5', 't' * 21, 20,
                          None, 'testr4-5@test.com') is True
    assert create_product('Iphone 4 5 1', 't' * 21, 9,
                          None, 'testr4-5@test.com') is False
    assert create_product('Iphone 4 5 2', 't' * 21, 10001,
                          None, 'testr4-5@test.com') is False


def test_r4_7_owner_not_empty():
    '''
    Testing R4-7: The owner_email cannot be empty. The owner
    of the corresponding product must exist in the database.
    '''
    register('u0 r4 7', 'testr4-7@test.com', '123aBc!')
    assert create_product(
        'title47',
        'description goes here',
        20,
        '2021-11-10',
        'testr4-7@test.com') is True
    assert create_product('title482', 'description', 20,
                          '2021-11-10', '') is False


def test_r4_8_unique_titles():
    '''
    Testing R4-8: A user can't create products that have the same title.
    '''
    register('u0 r4 8', 'testr4-8@test.com', '123aBc!')
    assert create_product(
        'title48',
        'description goes here',
        40,
        '2021-12-11',
        'testr4-8@test.com') is True

    assert create_product(
        'title48',
        'description2',
        37,
        '2021-12-10',
        'testr4-8@test.com') is False


def test_r5_1_cannot_change_email_or_date():
    '''
    Testing R5-1: A user can update all properties of product except for
    owner email and last_modified_date
    '''
    register('r5 1', 'testr5-1@test.com', '123aBc!')
    create_product(
        'title51',
        'description goes here',
        40,
        '2021-12-11',
        'testr5-1@test.com')
    assert update_product(1, newPrice=25, newTitle="Title511",
                          newDesc="description goes here") is True
    assert update_product(1, last_modified_date="2021-12-1") is False
    assert update_product(1, owner_email="test@yahoo.com") is False


def test_r5_2_price_must_increase():
    '''
    Testing R5-2: A user can only increase the price but not decrease
    '''
    register('r5 2', 'testr5-2@test.com', '123aBc!')
    create_product(
        'title52',
        'description goes here',
        40,
        '2021-12-11',
        'testr5-2@test.com')
    assert update_product(
        1,
        newPrice=150,
        newTitle='newer title',
        newDesc='newer newer description') is True
    assert update_product(
        1,
        newPrice=50,
        newTitle='newer title',
        newDesc='newer newer description') is False


def test_r5_3_update_date():
    '''
    Testing R5-3: last_modified_date should be updated when operation is
    succesful.
    '''
    register('r5 3', 'testr5-3@test.com', '123aBc!')
    create_product(
        'title53',
        'description goes here',
        40,
        '2021-12-11',
        'testr5-3@test.com')
    assert update_product(1,
                          newPrice=150,
                          newTitle='newer title',
                          newDesc='newer newer description') is True


def test_r5_4_validate_attributes():
    '''
    Testing R5-4: When updating a product model, all the attributes must
    be validated before updating.
    '''
    register('r5 4', 'testr5-4@test.com', '123aBc!')
    create_product(
        'title54',
        'description goes here',
        40,
        '2021-12-11',
        'testr5-4@test.com')
    assert update_product(1, newPrice=1500, newTitle='n',
                          newDesc='nn') is False
    assert update_product(1, newPrice=500, newTitle='nn', newDesc='n') is False


def test_sql_title_createProduct():
    ''' injecting the title parameter with the payload '''
    register('r5 4', 'testr5-4@test.com', '123aBc!')
    errors = []
    for payload in open('qbay_test/payload.txt', "r").readlines():
        try:
            assert create_product(
                payload,
                'description of stuff',
                40,
                '2021-12-11',
                'testr5-4@test.com') is False
        except Exception as e:
            errors.append(e)


def test_sql_desc_createProduct():
    ''' injecting the description parameter with the payload '''
    register('r5 4', 'testr5-4@test.com', '123aBc!')
    errors = []
    for payload in open('qbay_test/payload.txt', "r").readlines():
        try:
            assert create_product(
                'title',
                payload,
                40,
                '2021-12-11',
                'testr5-4@test.com') is False
        except Exception as e:
            errors.append(e)


def test_sql_price_createProduct():
    ''' injecting the price parameter with the payload '''
    register('r5 4', 'testr5-4@test.com', '123aBc!')
    errors = []
    for payload in open('qbay_test/payload.txt', "r").readlines():
        try:
            assert create_product(
                'title',
                'description of stuff',
                payload,
                '2021-12-11',
                'testr5-4@test.com') is False
        except Exception as e:
            errors.append(e)


def test_sql_date_createProduct():
    ''' injecting the date parameter with the payload '''
    errors = []
    register('r5 4', 'testr5-4@test.com', '123aBc!')
    for payload in open('qbay_test/payload.txt', "r").readlines():
        try:
            assert create_product(
                'title',
                'description of stuff',
                40,
                payload,
                'testr5-4@test.com') is False
        except Exception as e:
            errors.append(e)


def test_sql_email_createProduct():
    ''' injecting the email parameter with the payload '''
    errors = []
    register('r5 4', 'testr5-4@test.com', '123aBc!')
    for payload in open('qbay_test/payload.txt', "r").readlines():
        try:
            assert create_product(
                'title',
                'description of stuff',
                40,
                '2021-12-11',
                payload) is False
        except Exception as e:
            errors.append(e)


def test_sql_register_username():
    '''Fuzzy Test: injecting into the username parameter
    with general injection payload.'''
    i = 0
    errors = []
    for payload in open('qbay_test/payload.txt', "r").readlines():
        try:
            assert register(
                payload,
                'test-sql' + i + '@gmail.com',
                '123aBc!') is False
            i += 2
        except Exception as e:
            errors.append(e)


def test_sql_register_email():
    '''Fuzzy Test: injecting into the email parameter
    with general injection payload..'''

    errors = []
    for payload in open('qbay_test/payload.txt', "r").readlines():
        try:
            assert register(
                "r5 4",
                payload,
                '123aBc!') is False
        except Exception as e:
            errors.append(e)


def test_sql_register_password():
    '''Fuzzy Test: injecting into the password parameter
    with general injection payload.'''

    i = 1
    errors = []
    for payload in open('qbay_test/payload.txt', "r").readlines():
        try:
            assert register(
                "r5 4",
                'test-sql' + i + '@gmail.com',
                payload) is False
            i += 2
        except Exception as e:
            errors.append(e)


def test_sql_purchase_title():
    '''Fuzzy Test: injecting into the productTitle parameter
    with general injection payload.'''

    register('sql 1 0', 'testsql10@test.com', '123aBc!')
    register('sql 1 1', 'testsql11@test.com', '123aBc!')
    create_product('sqlpurchasetestpt', 
                   'a test product meant for use with the sql testing',
                   50, None, 'testsql10@test.com')

    errors = []
    for payload in open('qbay_test/payload.txt', "r").readlines():
        try:
            assert purchase_product(
                payload,
                'testsql11@test.com') is False
        except Exception as e:
            errors.append(e)


def test_sql_purchase_email():
    '''Fuzzy Test: injecting into the email parameter
    with general injection payload.'''

    register('sql 2 0', 'testsql20@test.com', '123aBc!')
    create_product('sqlpurchasetestem', 
                   'a test product meant for use with the sql testing',
                   50, None, 'testsql20@test.com')

    errors = []
    for payload in open('qbay_test/payload.txt', "r").readlines():
        try:
            assert purchase_product(
                'sqlpurchasetestem',
                payload) is False
        except Exception as e:
            errors.append(e)


def test_purchase_product():
    '''
    Testing placing order: user cannot place an order for their own product,
    and user cannot place an order that costs more than their balance.
    '''
    assert purchase_product('title53', 'testr5-3@test.com') is not True
    assert purchase_product('title53', 'testr4-3@test.com') is True
    assert purchase_product('newer title', 'testr5-3@test.com') is not True
    assert purchase_product('title53', 'testr4-3@test.com') is True
