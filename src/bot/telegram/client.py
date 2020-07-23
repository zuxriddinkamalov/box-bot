import os
import traceback

from aiogram.types import InputFile

from db import proj_path, core_models, telegram_models, Paginator

from geopy.geocoders import Nominatim
from geopy.distance import geodesic


class Client():

    @classmethod
    def test_connection(self):

        try:
            core_models.Language.objects.get(pk=1)

            print(f"CLIENT: connection is stable")
        except Exception as e:
            print(f"ERROR: connection lost")

    @classmethod
    def get_telegram_token(self):

        active_settings = telegram_models.Settings.objects.filter(
            active=True
            ).first()

        return {
            'title': active_settings.title,
            'token': active_settings.token
            }

    @classmethod
    def get_chatbase_token(self):

        active_settings = telegram_models.Settings.objects.filter(
            active=True
            ).first()

        return {
            'title': active_settings.title,
            'token': active_settings.chatbase_token
            }

    @classmethod
    def get_paysystem_token(self, id: int):

        paysystem = telegram_models.PaySystem.objects.filter(
            active=True
            ).get(pk=id)

        return paysystem

    @classmethod
    def is_verified(self, user: int):
        user = self.get_user(user)

        return True if user.phone else False

    @classmethod
    def has_real_name(self, user: int):
        user = self.get_user(user)

        return True if user.real_name else False

    @classmethod
    def get_message(self, number: int, lan: str):

        return core_models.Message.objects.filter(
            language__title=str(lan)
            ).get(number=number).text.replace('\\n', '\n')

    @classmethod
    def get_user_language(self, user: int):

        return str(telegram_models.User.objects.get(
            chat_id=user
            ).language.title)

    @classmethod
    def user_exists(self, user: int):

        try:
            telegram_models.User.objects.get(chat_id=user)
            return True

        except Exception:

            return False

    @classmethod
    def user_create(self, user):

        new = telegram_models.User()

        new.chat_id = user.id
        new.language = core_models.Language.objects.get(pk=1)
        new.first_name = user.first_name
        new.last_name = user.last_name
        new.username = user.username

        new.save()

        return new

    @classmethod
    def get_user(self, user: int):

        try:

            user = telegram_models.User.objects.get(chat_id=user)
            return user

        except Exception as identifier:

            return False

    @classmethod
    def get_buttons(self, language: str, checkpoint: int):

        buttons = core_models.Button.objects.filter(
            language__title=str(language),
            checkpoint=int(checkpoint),
            active=True
            ).order_by("order")

        return buttons

    @classmethod
    def get_categories(self, language: str, page: int):

        categories = core_models.Category.objects.filter(
            language__title=str(language),
            active=True
            ).order_by("order")

        pagination = Paginator(categories, 5)
        current_page = pagination.page(page)

        return {
            'categories': current_page.object_list,
            'next': current_page.next_page_number() if current_page.has_next() else 1,
            'prev': current_page.previous_page_number() if current_page.has_previous() else pagination.num_pages,
            'total': pagination.num_pages
        }

    @classmethod
    def get_products(self, language: str, category: int, page: int):

        products = core_models.Product.objects.filter(
            language__title=str(language),
            active=True,
            category__id=category
            ).order_by("order")

        pagination = Paginator(products, 5)
        current_page = pagination.page(page)

        return {
            'products': current_page.object_list,
            'next': current_page.next_page_number() if current_page.has_next() else 1,
            'prev': current_page.previous_page_number() if current_page.has_previous() else pagination.num_pages,
            'total': pagination.num_pages
        }

    @classmethod
    def add_to_cart(self, user, product: int, quantity: int):

        user = self.get_user(user)

        try:

            cart = telegram_models.Cart.objects.filter(user=user, canceled=False).get(active=True)

            if cart.positions.all().filter(product__id=product).count() != 0:
                position = cart.positions.all().get(product__id=product)
                position.count = position.count + quantity
                position.save()

                return cart

        except Exception as e:

            cart = telegram_models.Cart()
            cart.user = user
            cart.save()

        position = core_models.Position()
        position.product = core_models.Product.objects.get(pk=product)
        position.count = quantity
        position.save()

        cart.positions.add(position)

        return cart

    @classmethod
    def get_cart_count(self, user):

        user = self.get_user(user)

        try:

            cart = telegram_models.Cart.objects.filter(user=user, canceled=False).get(active=True)

            return cart.get_count()

        except Exception as e:

            return 0

    @classmethod
    def get_cart(self, user: int):

        user = self.get_user(user)

        try:

            cart = telegram_models.Cart.objects.filter(user=user, canceled=False).get(active=True)

            return cart

        except Exception as e:

            return None

    @classmethod
    def clear_cart(self, user: int):

        user = self.get_user(user)

        cart = telegram_models.Cart.objects.filter(user=user, canceled=True).get(active=True)
        rs = cart.positions.all().delete()
        cart.delete()

        return rs

    @classmethod
    def cancel_cart(self, user: int):

        cart = self.get_cart(user)
        cart.canceled = True
        cart.save()

        return cart

    @classmethod
    def revoke_cart(self, user: int):

        user = self.get_user(user)

        cart = telegram_models.Cart.objects.filter(user=user, canceled=True).get(active=True)
        cart.canceled = False
        cart.save()

        return cart

    @classmethod
    def get_category(self, number: int):

        return core_models.Category.objects.get(pk=number)

    @classmethod
    def get_product(self, number: int):

        return core_models.Product.objects.get(pk=number)

    @classmethod
    def get_managers(self):

        return telegram_models.Settings.objects.filter(
            active=True
            ).first().managers.all()

    @classmethod
    def get_managers_ids(self):

        ids: int = []

        for manager in self.get_managers():
            ids.append(manager.chat_id)

        return ids

    @classmethod
    def set_language(self, user: int, language: str):

        current_user = telegram_models.User.objects.get(chat_id=user)
        language = core_models.Language.objects.get(title=language)

        current_user.language = language
        current_user.language_set = True
        current_user.save()

    @classmethod
    def set_phone(self, user: int, phone: int):

        current_user = telegram_models.User.objects.get(chat_id=user)
        current_user.phone = phone
        current_user.save()

    @classmethod
    def set_real_name(self, user: int, name: str):

        current_user = telegram_models.User.objects.get(chat_id=user)
        current_user.real_name = name
        current_user.save()

    @classmethod
    def get_all_news(self, user: int):

        language = self.get_user_language(user)

        news = core_models.Announcement.objects.filter(
            language__title=language,
            active=True,
            visible=True
            ).order_by("-created_at")

        return news

    @classmethod
    def get_all_event(self, user: int):

        language = self.get_user_language(user)
        events = core_models.Event.objects.filter(
            language__title=language,
            active=True,
            visible=True
            ).order_by("-created_at")

        return events

    @classmethod
    def get_photo(self, current):

        photo = current.photo
        if photo.file_id is None:

            photoPath = str(photo.photo).split("/")
            end_path = os.path.join(
                proj_path,
                photoPath[0],
                photoPath[1],
                photoPath[2]
                )

            return [InputFile(end_path), False, photo.id]
        else:
            return [photo.file_id, True, photo.id]

    @classmethod
    def get_paysystems(self):

        return telegram_models.PaySystem.objects.filter(
            active=True
            ).order_by('order')
        
    @classmethod
    def get_branches(self):

        return telegram_models.Branch.objects.filter(
            active=True
            ).order_by('order')

    @classmethod
    def update_photo(self, photo_id: int, file_id: str):

        photo = core_models.Photo.objects.get(pk=photo_id)
        photo.file_id = file_id
        photo.save()

        return photo

    @classmethod
    def tick_view(self, obj):

        obj.views = obj.views + 1
        obj.save()
        
    @classmethod
    def get_order(self, order: int):
        
        return telegram_models.Order.objects.get(pk=order)

    @classmethod
    def create_order(self, user: int, data):

        cart = self.get_cart(user)
        user = self.get_user(user)
        status = core_models.OrderStatus.objects.get(order=1)

        delivery = data['delivery']
        time = data['time']
        card = data['card']
        try:
            branch = int(data['branch'])
        except Exception as e:
            pass

        order = telegram_models.Order()
        order.user = user
        order.phone = user.phone
        order.name = user.real_name
        
        closest = True

        order.cart = cart

        order.status = status

        if card:
            paysystem = telegram_models.PaySystem.objects.get(pk=int(data['paysystem']))
            order.card = card
        else:
            paysystem = None
            order.card = card

        order.paysystem = paysystem

        if time:

            order.time = time

        if delivery:

            order.delivery = delivery
            order.latitude = data['location_x']
            order.longitude = data['location_y']

            try:
                geolocator = Nominatim(user_agent="onezeth")
                
                location = geolocator.reverse(f"{data['location_x']}, {data['location_y']}", language='ru-RU')
                order.address = location.address

            except Exception as e:
                print(e)
                order.address = ''

            if closest:

                min = 1000000.0
                branch_number = None
                for branch in telegram_models.Branch.objects.filter(active=True):

                    point1 = (float(data['location_x']), float(data['location_y']))
                    point2 = (branch.latitude, branch.longitude)
                    distance = geodesic(point1, point2).km
                    if float(distance) < min:
                        
                        branch_number = branch
                        min = distance

                order.selected_branch = branch_number

        else:

            order.selected_branch = telegram_models.Branch.objects.get(pk=branch)

        order.save()
        
        print(order.selected_branch)

        cart.active = False
        cart.save()
        return order


if __name__ == "__main__":

    client = Client()
    client.test_connection()
