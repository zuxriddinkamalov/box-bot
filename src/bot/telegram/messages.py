from client import core_models
from client import telegram_models
from client import Client as client

Client = client()


def Messages(user: int):

    language = Client.get_user_language(int(user))

    MESSAGES = {
        'start_message': Client.get_message(1, language),
        'ask_for_language': Client.get_message(2, language),
        'main_menu': Client.get_message(3, language),
        'category': Client.get_message(4, language),
        'product': Client.get_message(5, language),
        'quantity': Client.get_message(6, language),
        'cart_added': Client.get_message(7, language),
        'position_text': Client.get_message(8, language),
        'cart_header': Client.get_message(9, language),
        'cart_is_empty': Client.get_message(10, language),
        'cart_footer': Client.get_message(11, language),
        'edit_menu': Client.get_message(12, language),
        'cart_cleared': Client.get_message(13, language),
        'cart_restored': Client.get_message(14, language),
        'add_phone': Client.get_message(15, language),
        'phone_set': Client.get_message(16, language),
        'phone_length': Client.get_message(17, language),
        'phone_only_digits': Client.get_message(18, language),
        'delivery': Client.get_message(19, language),
        'real_name_get': Client.get_message(20, language),
        'location': Client.get_message(21, language),
        'time_set_delivery': Client.get_message(22, language),
        'time_set_self': Client.get_message(23, language),
        'set_time': Client.get_message(24, language),
        'time_set_success': Client.get_message(25, language),
        'payment_type': Client.get_message(26, language),
        'order_accepted': Client.get_message(27, language),
        'product_removed': Client.get_message(28, language),
        'paysystem_choose': Client.get_message(29, language),
        'order_header': Client.get_message(30, language),
        'order_cash': Client.get_message(31, language),
        'order_close_time': Client.get_message(32, language),
        'order_yes': Client.get_message(33, language),
        'order_no': Client.get_message(34, language),
    }

    return MESSAGES


def GenerateCart(user: int):

    cart = Client.get_cart(user)
    language = Client.get_user_language(user)

    if cart is None:

        return [Messages(user)['cart_is_empty'], False]

    position_text = Messages(user)['position_text']
    cart_header = Messages(user)['cart_header']
    cart_footer = Messages(user)['cart_footer']

    end_text = f'{cart_header}'

    categories = core_models.Category.objects.filter(
            language__title=str(language),
            active=True
            ).order_by("order")

    for category in categories:

        positions = cart.positions.all().filter(product__category=category)
        if positions.count() != 0:

            end_text += f'{category.title.upper()}\n'

            for position in positions:

                end_text = end_text + position_text.replace(
                    '{product}',
                    position.product.title
                    ).replace(
                        '{product_count}',
                        str(position.count)
                    ).replace(
                        '{price}',
                        '{:,}'.format(position.product.price * position.count).replace(',', ' ')
                    )

    price = "{:,}".format(cart.get_price()).replace(",", " ")
    end_text += f'\n{cart_footer.replace("{cost}", price)}'

    return [end_text, True]


def GenerateOrder(user, data):

    cart = Client.get_cart(user)
    language = Client.get_user_language(user)

    position_text = Messages(user)['position_text']
    order_header = Messages(user)['order_header']
    cart_footer = Messages(user)['cart_footer']
    
    order_user = Client.get_user(user)
    
    delivery = data['delivery']
    time = data['time']
    
    if not time:
        time = Messages(user)['order_close_time']

    try:
        paysystem = data['paysystem']
        paysystem = telegram_models.PaySystem.objects.get(pk=int(paysystem)).title
    except Exception as e:
        paysystem = Messages(user)['order_cash']

    order_header = order_header.replace(
        '{time}', time
        ).replace(
            '{payment}',
            paysystem).replace(
                '{delivery}',
                Messages(user)['order_yes'] if delivery else Messages(user)['order_no']
            ).replace(
                '{name}',
                order_user.real_name
                ).replace(
                '{phone}',
                f'+{str(order_user.phone)}'
                )
    end_text = f'{order_header}'

    categories = core_models.Category.objects.filter(
            language__title=str(language),
            active=True
            ).order_by("order")

    for category in categories:

        positions = cart.positions.all().filter(product__category=category)
        if positions.count() != 0:

            end_text += f'{category.title.upper()}\n'

            for position in positions:

                end_text = end_text + position_text.replace(
                    '{product}',
                    position.product.title
                    ).replace(
                        '{product_count}',
                        str(position.count)
                    ).replace(
                        '{price}',
                        '{:,}'.format(position.product.price * position.count).replace(',', ' ')
                    )

    price = "{:,}".format(cart.get_price()).replace(",", " ")
    end_text += f'\n{cart_footer.replace("{cost}", price)}'

    return end_text
