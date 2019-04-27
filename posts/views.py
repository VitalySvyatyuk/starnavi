from django.contrib.auth.hashers import make_password
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import CustomUser, Post, Preference
from .permissions import IsOwnerOrReadOnly
from .serializers import CustomUserSerializer, PostSerializer
from .utils import check_email, enrich_data


class CustomUserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.validated_data['email_deliverability'] = check_email(serializer.validated_data['email'])
        serializer.validated_data['enrichment'] = enrich_data(serializer.validated_data['email'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data['username'], status=status.HTTP_201_CREATED, headers=headers)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly, ])
    def set_like(self, request, *args, **kwargs):
        '''
        User may have only one vote for post, it may be like (1) or unlike (-1)
        Also, user may change his vote as many times as he wants
        '''
        like = request.data.get('like')
        if like and int(like) in (1, -1):
            post = self.get_object()
            preference = Preference.objects.filter(post=post, user=request.user).first()
            if preference:
                post.likes -= preference.like
                preference.delete()

            if not preference or preference.like != int(like):
                post.likes += int(like)
                Preference.objects.create(user=request.user, post=post, like=int(like))
            post.save()
            return Response("Your prefernce is taken", status.HTTP_200_OK)
        else:
            return Response("like parameter should be 1 or -1", status.HTTP_400_BAD_REQUEST)
