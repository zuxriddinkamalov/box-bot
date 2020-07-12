import os
import traceback

from aiogram.types import InputFile

from db import proj_path, core_models, telegram_models


class Client():

    @classmethod
    def test_connection(self):

        try:
            core_models.Language.objects.get(pk=1)
            
            print(f"CLIENT: connection stable")
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
    def get_message(self, number: int, lan: str):

        return core_models.Message.objects.filter(
            language__title=str(lan)
            ).get(number=number).text

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

        buttons = models.Button.objects.filter(
            language__title=str(language),
            checkpoint=int(checkpoint),
            active=True
            ).order_by("number")

        return buttons

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
    def update_photo(self, photo_id: int, file_id: str):

        photo = core_models.Photo.objects.get(pk=photo_id)
        photo.file_id = file_id
        photo.save()

        return photo

    @classmethod
    def tick_view(self, obj):

        obj.views = obj.views + 1
        obj.save()


if __name__ == "__main__":

    client = Client()
    client.test_connection()
