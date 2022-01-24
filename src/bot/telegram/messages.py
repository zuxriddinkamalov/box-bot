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
        'order_edit': Client.get_message(35, language),
        'info_updated': Client.get_message(36, language),
        'checkout_title': Client.get_message(37, language),
        'checkout_description': Client.get_message(38, language),
        'set_branch': Client.get_message(39, language),
        'in_porgress_cooking': Client.get_message(40, language),
        'in_porgress_to_delivery': Client.get_message(41, language),
        'in_porgress_to_self': Client.get_message(42, language),
        'noNews': Client.get_message(43, language),
        'choose_events': Client.get_message(44, language),
        'noEvents': Client.get_message(45, language),
    }

    return MESSAGES


def GenerateCart(user: int):

    cart = Client.get_cart(user)
    language = Client.get_user_language(user)

    if cart is None:

        return [Messages(user)['cart_is_empty'], False]
    
    positions = cart.positions.all()
    for position in positions:
        if position.product.language.title != language:
            position.product = core_models.Product.objects.filter(
                language__title=language
                ).get(
                    code=position.product.code
                    )
            position.save()

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

            end_text += f'\n{category.title.upper()}\n'

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


def GenerateOrder(user, data, channel=False):

    

    cart = Client.get_cart(user)
    if not channel:
        language = Client.get_user_language(user)
        ru_lan_user = user
    else:
        ru_lan_user = telegram_models.User.objects.filter(language__title='ru').first()
        language = ru_lan_user.language
        ru_lan_user = ru_lan_user.chat_id

    if channel:
        user_order = telegram_models.Order.objects.get(pk=int(data['order_id']))
        cart = user_order.cart

        
    positions = cart.positions.all()
    for position in positions:
        if position.product.language.title != language:
            position.product = core_models.Product.objects.filter(
                language__title=language
                ).get(
                    code=position.product.code
                    )
            position.save()

    position_text = Messages(ru_lan_user)['position_text']
    order_header = Messages(ru_lan_user)['order_header']
    cart_footer = Messages(ru_lan_user)['cart_footer']
    
    order_user = Client.get_user(user)
    
    delivery = data['delivery']
    time = data['time']
    
    if not time:
        time = Messages(ru_lan_user)['order_close_time']

    try:
        paysystem = data['paysystem']
        paysystem = telegram_models.PaySystem.objects.get(pk=int(paysystem)).title
    except Exception as e:
        paysystem = Messages(ru_lan_user)['order_cash']

    order_header = order_header.replace(
        '{time}', time
        ).replace(
            '{payment}',
            paysystem).replace(
                '{delivery}',
                Messages(ru_lan_user)['order_yes'] if delivery else Messages(ru_lan_user)['order_no']
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

            end_text += f'\n{category.title.upper()}\n'

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
    
    if channel:
        if user_order.delivery:
            end_text += f"\n\nПредположительный адрес: {user_order.address}" 

    return end_text
