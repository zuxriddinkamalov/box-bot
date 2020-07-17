from client import core_models
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
        # 'information': Client.getMessage(4, language),
        # 'before_real_name': Client.getMessage(5, language),
        # 'getRealName': Client.getMessage(6, language),
        # 'getPhone': Client.getMessage(7, language),
        # 'accept_data': Client.getMessage(8, language),
        # 'account_menu': Client.getMessage(9, language),
        # 'noNews': Client.getMessage(10, language),
        # 'noEvents': Client.getMessage(11, language),
        # 'user_info': Client.getMessage(12, language),
        # 'settings': Client.getMessage(13, language),
        # 'edit_account': Client.getMessage(14, language),
        # 'edit_account_updated': Client.getMessage(15, language),
        # 'inn_accept': Client.getMessage(16, language),
        # 'inn_only_digits': Client.getMessage(17, language),
        # 'inn_updated': Client.getMessage(18, language),
        # 'inn_updated_twice': Client.getMessage(19, language),
        # 'userCurrentInfo': Client.getMessage(20, language),
        # 'phone_only_digits': Client.getMessage(21, language),
        # 'phone_length': Client.getMessage(22, language),
        # 'language_changed': Client.getMessage(24, language),
        # 'auth': Client.getMessage(25, language),
        # 'NotAuth': Client.getMessage(26, language),
        # 'pricelist_about': Client.getMessage(27, language),
        # 'choose_region': Client.getMessage(28, language),
        # 'choose_branch': Client.getMessage(29, language),
        # 'choose_territory': Client.getMessage(30, language),
        # 'manager_choose_action': Client.getMessage(31, language),
        # 'manager_info': Client.getMessage(32, language),
        # 'add_review': Client.getMessage(33, language),
        # 'add_comment': Client.getMessage(34, language),
        # 'thanks_for_review': Client.getMessage(35, language),
        # 'choose_events': Client.getMessage(36, language),
        # 'no_quizes_yet': Client.getMessage(37, language),
        # 'choose_quiz': Client.getMessage(38, language),
        # 'quiz_results': Client.getMessage(39, language),
        # 'start_command': Client.getMessage(40, language),
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

    # for counter in range(0, cart.positions.all().count()):

    #     end_text = end_text + position_text.replace(
    #         '{count}',
    #         str(counter + 1)
    #         ).replace(
    #             '{product}',
    #             cart.positions.all()[counter].product.title
    #         ).replace(
    #             '{product_count}',
    #             str(cart.positions.all()[counter].count)
    #         )

    price = "{:,}".format(cart.get_price()).replace(",", " ")
    end_text += f'\n{cart_footer.replace("{cost}", price)}'

    return [end_text, True]


def GenerateOrder(user):
    # TODO cool logic for Order Generate
    pass
