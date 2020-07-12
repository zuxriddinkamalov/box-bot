from client import Client as client
Client = client()


def Messages(user):
    lan = Client.get_user_language(int(user))

    MESSAGES = {
        'start_message': Client.get_message(1, lan),
        'ask_for_language': Client.get_message(2, lan),
        'main_menu': Client.get_message(3, lan),
        'category': Client.get_message(4, lan),
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