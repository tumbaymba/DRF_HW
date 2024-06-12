from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from studing.models import Course, Lesson, Subscription
from users.models import User


class LessonAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@sky.pro")
        self.user.set_password('123qwe')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='course_test',
            description='course_test',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title="test_lesson",
            description="test_lesson",
            course=self.course,
            owner=self.user,
            video_url=r"https://www.youtube.com/watch?v=HYOd_KlieeE&list=RDMMHYOd_KlieeE&start_radio=1"

        )

    def test_list_lesson(self):

        response = self.client.get(
            reverse('studing:lesson_list')
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {'course': self.lesson.course.title,
                     'description': self.lesson.description,
                     'id': self.lesson.id,
                     'owner': self.lesson.owner.id,
                     'preview': self.lesson.preview,
                     'title': self.lesson.title

                     }
                ]
            }
        )

    def test_get_lesson(self):
        """Тестирование вывода урока (detail)"""

        response = self.client.get(
            reverse('studing:lesson_get', kwargs={'pk': self.lesson.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_lesson(self):
        """Тестирование создания урока"""

        data = {
            'title': "test_lesson_2",
            'description': "test_lesson_2",
            'course': self.lesson.course.id,
            'owner': self.lesson.owner.id,
        }

        response = self.client.post(
            reverse('studing:lesson_create'),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_create_lesson_validation_error(self):
        """Тестирование создания урока с валидацией"""

        data = {
            'title': "test_lesson_3",
            'description': "test_lesson_3",
            'course': self.lesson.course.id,
            'owner': self.lesson.owner.id,
            'video_url': r"https://dzen.ru/video/watch/65113ea5b1765406f111c976?utm_referrer=www.google.com"

        }

        response = self.client.post(
            reverse('studing:lesson_create'),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Ссылки на сторонние видео запрещены']}
        )

    def test_update_lesson(self):
        """Тестирование редактирования урока"""

        response = self.client.patch(
            reverse('studing:lesson_update', kwargs={'pk': self.lesson.id}),
            {'description': 'change'})

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_lesson(self):
        """Тестирование удаления урока (не владельца)"""

        user_del = User.objects.create(email="test_del@sky.pro")
        user_del.set_password('123qwe456rty')
        self.client.force_authenticate(user=user_del)

        lesson_del = Lesson.objects.create(
            title="test_lesson_delete",
            description="test_lesson_delete",
            course=self.course,
            owner=self.user,
        )

        response = self.client.delete(
            reverse('studing:lesson_delete', kwargs={'pk': lesson_del.id}))

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )


class SubscriptionAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test3@sky.pro")
        self.user.set_password('123qwe')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='course_test',
            description='course_test',
            owner=self.user
        )

    def test_subscribe_to_course(self):
        """Тестирование на создание подписки на курс"""

        data = {
            "user": self.user.id,
            "course": self.course.id,
        }

        response = self.client.post(
            reverse('studing:subscription'),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'message': 'Вы подписались на обновления курса'}
        )

    def test_subscribe_to_course_cancel(self):
        """Тестирование на отмену подписки на курс"""

        subscription = Subscription.objects.create(
            course=self.course,
            user=self.user,
        )

        subscription.refresh_from_db()

        data = {
            "course": self.course.id,
        }

        self.client.force_authenticate(user=self.user)

        response_subscribe = self.client.post(
            reverse('studing:subscription'),
            data=data
        )

        self.assertEquals(
            response_subscribe.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response_subscribe.json(),
            {'message': 'Вы отписались от обновления курса'}
        )