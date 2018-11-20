from rest_framework import pagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


from articles.models import User, Article, Category, Comment, Follow, Favorite, Highlight


from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from articles.permissions import ArticlePermissions, UserPermission, UserListCreatePermission, NoPermission, CategoryPermission, HighlightPermission
from articles.serializers import ArticleListSerializer, ArticleDetailSerializer, \
    NewArticleSerializer, MyArticleListSerializer, MyArticleDetailSerializer, UserSerializer, \
    UserListSerializer, NewUserSerializer, NewCategorySerializer,  CategoryListSerializer, CategoryDetailSerializer, \
    NewCommentSerializer, CommentListSerializer, CommentDetailSerializer, NewFollowSerializer, FollowListSerializer, \
    FavoriteListSerializer, SearchListSerializer, NewFavoriteSerializer, HighlightListSerializer, NewHighlightSerializer, MyFavoriteListSerializer


class CategoryViewSet(ModelViewSet):

    permission_classes = [CategoryPermission]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name']
    filter_fields = ['name']
    lookup_field = 'name'

    def get_queryset(self):
        return Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return NewCategorySerializer
        elif self.action == 'list':
            return CategoryListSerializer
        else:
            return CategoryDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ArticlesPagination(pagination.PageNumberPagination):

    page_size = 6

    def get_paginated_response(self, data):
        return Response({

            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data
        })


class ArticleViewSet(ModelViewSet):

    permission_classes = [ArticlePermissions]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['title', 'slug', 'category__name',
                     'owner__username', 'publish_date', 'created_on', 'introduction']
    filter_fields = ('title', 'slug', 'category__name',
                     'owner__username', 'publish_date', 'created_on', 'introduction')
    ordering_fields = ['publish_date', 'created_on']
    pagination_class = ArticlesPagination

    def get_queryset(self):
        return Article.objects.filter(status='PUB').filter(publish_date__lte=datetime.now()).order_by('-publish_date')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return NewArticleSerializer
        elif self.action == 'list':
            return ArticleListSerializer
        else:
            return ArticleDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyArticleViewSet(ModelViewSet):
    permission_classes = [ArticlePermissions]
    pagination_class = ArticlesPagination

    def get_queryset(self):
        if self.request.user.id is None:
            return
        else:
            return Article.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return NewArticleSerializer
        elif self.action == 'list':
            return MyArticleListSerializer
        else:
            return MyArticleDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyFavoritesViewSet(ModelViewSet):
    permission_classes = [ArticlePermissions]
    pagination_class = ArticlesPagination

    def get_queryset(self):
        if self.request.user.id is None:
            return
        else:
            return Favorite.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return NewFavoriteSerializer
        elif self.action == 'list':
            return MyFavoriteListSerializer
        else:
            return MyFavoriteListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    lookup_field = 'username'
    search_fields = ['username', 'email']
    filter_fields = ('username', 'email', 'first_name',
                     'last_name', 'articles')

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [UserListCreatePermission]
        elif self.action == 'create' and self.request.user.is_anonymous:
            self.permission_classes = [UserListCreatePermission]
        elif self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [UserPermission]
        elif self.action == 'destroy' or self.action == 'retrieve':
            self.permission_classes = [UserPermission]
        else:
            self.permission_classes = [NoPermission]
        return super(UserViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return NewUserSerializer
        elif self.action == 'list':
            return UserListSerializer
        else:
            return UserSerializer


class CommentViewSet(ModelViewSet):

    permission_classes = [ArticlePermissions]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['article', 'text', 'owner']
    filter_fields = ('article', 'text', 'owner')
    ordering_fields = ['created_on']

    def get_queryset(self):
        return Comment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return NewCommentSerializer

        elif self.action == 'list':
            return CommentListSerializer
        else:
            return CommentDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowViewSet(ModelViewSet):

    permission_classes = [ArticlePermissions]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['owner', 'user_followed']
    filter_fields = ('owner', 'user_followed')
    ordering_fields = ['owner', 'user_followed']

    def get_queryset(self):
        return Follow.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return NewFollowSerializer
        elif self.action == 'list':
            return FollowListSerializer
        else:
            return FollowListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FavoriteViewSet(ModelViewSet):

    permission_classes = [ArticlePermissions]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['owner', 'article']
    filter_fields = ('owner', 'article')
    ordering_fields = ['owner', 'article']

    def get_queryset(self):
        return Favorite.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return NewFavoriteSerializer
        elif self.action == 'list':
            return FavoriteListSerializer
        else:
            return FavoriteListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HighlightViewSet(ModelViewSet):

    permission_classes = [HighlightPermission]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['owner__username', 'article__slug', 'highlight_content']
    filter_fields = ['owner__username', 'article__slug', 'highlight_content']

    def get_queryset(self):
        return Highlight.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return NewHighlightSerializer
        elif self.action == 'list':
            return HighlightListSerializer
        else:
            return NewHighlightSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SearchViewSet(ModelViewSet):

    permission_classes = [ArticlePermissions]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['title', 'slug', 'category__name', 'full_text',
                     'owner__username', 'publish_date', 'created_on', 'introduction']

    def get_queryset(self):
        return Article.objects.filter(status='PUB')

    def get_serializer_class(self):
        return SearchListSerializer
