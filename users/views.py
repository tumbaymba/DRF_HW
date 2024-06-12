from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from studing.models import Course
from users.models import User, Payment
from users.permissions import IsOwner, IsModerator, IsSuperuser
from users.serializers import UserSerializer, PaymentSerializer, PaymentCreateSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSuperuser]


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSuperuser]


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'pay_method')
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated, IsSuperuser]


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)
        course = serializer.validated_data.get('course')

        if course in Course.objects.filter(owner=self.request.user):
            payment = serializer.save()
            stripe_price_product = create_stripe_product(payment.course.title)
            stripe_price_id = create_stripe_price(payment.course.price, stripe_price_product)
            payment.payment_link, payment.payment_id = create_stripe_session(stripe_price_id)
            payment.save()
        else:
            raise serializers.ValidationError('Укажите правильный курс для оплаты из посещаемых')
