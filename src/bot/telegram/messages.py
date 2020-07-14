from client import core_models
from client import Client as client

Client = client()


def Messages(user: int):

    lan = Client.get_user_language(int(user))

    MESSAGES = {
        'start_message': Client.get_message(1, lan),
        'ask_for_language': Client.get_message(2, lan),
        'main_menu': Client.get_message(3, lan),
        'category': Client.get_message(4, lan),
        'product': Client.get_message(5, lan),
        'quantity': Client.get_message(6, lan),
        'cart_added': Client.get_message(7, lan),
        'position_text': Client.get_message(8, lan),
        'cart_header': Client.get_message(9, lan),
        'cart_is_empty': Client.get_message(10, lan),
        'cart_footer': Client.get_message(11, lan),
        'edit_menu': Client.get_message(12, lan),
        'cart_cleared': Client.get_message(13, lan),
        # 'information': Client.getMessage(4, lan),
        # 'before_real_name': Client.getMessage(5, lan),
        # 'getRealName': Client.getMessage(6, lan),
        # 'getPhone': Client.getMessage(7, lan),
        # 'accept_data': Client.getMessage(8, lan),
        # 'account_menu': Client.getMessage(9, lan),
        # 'noNews': Client.getMessage(10, lan),
        # 'noEvents': Client.getMessage(11, lan),
        # 'user_info': Client.getMessage(12, lan),
        # 'settings': Client.getMessage(13, lan),
        # 'edit_account': Client.getMessage(14, lan),
        # 'edit_account_updated': Client.getMessage(15, lan),
        # 'inn_accept': Client.getMessage(16, lan),
        # 'inn_only_digits': Client.getMessage(17, lan),
        # 'inn_updated': Client.getMessage(18, lan),
        # 'inn_updated_twice': Client.getMessage(19, lan),
        # 'userCurrentInfo': Client.getMessage(20, lan),
        # 'phone_only_digits': Client.getMessage(21, lan),
        # 'phone_length': Client.getMessage(22, lan),
        # 'language_changed': Client.getMessage(24, lan),
        # 'auth': Client.getMessage(25, lan),
        # 'NotAuth': Client.getMessage(26, lan),
        # 'pricelist_about': Client.getMessage(27, lan),
        # 'choose_region': Client.getMessage(28, lan),
        # 'choose_branch': Client.getMessage(29, lan),
        # 'choose_territory': Client.getMessage(30, lan),
        # 'manager_choose_action': Client.getMessage(31, lan),
        # 'manager_info': Client.getMessage(32, lan),
        # 'add_review': Client.getMessage(33, lan),
        # 'add_comment': Client.getMessage(34, lan),
        # 'thanks_for_review': Client.getMessage(35, lan),
        # 'choose_events': Client.getMessage(36, lan),
        # 'no_quizes_yet': Client.getMessage(37, lan),
        # 'choose_quiz': Client.getMessage(38, lan),
        # 'quiz_results': Client.getMessage(39, lan),
        # 'start_command': Client.getMessage(40, lan),
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
