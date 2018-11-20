from rest_framework import serializers
from articles.models import User
from articles.models import Article, Category, Comment, Follow, Favorite, Highlight


class ArticleListSerializer(serializers.ModelSerializer):
    articleid = serializers.ReadOnlyField(source='uuid')
    #owner = serializers.ReadOnlyField(source='owner.username')
    first_name = serializers.ReadOnlyField(source='owner.first_name')
    last_name = serializers.ReadOnlyField(source='owner.last_name')
    owner = serializers.SlugRelatedField(read_only=True, slug_field='username')
    category = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field='name')

    class Meta:
        model = Article
        fields = ['articleid', 'title',
                  'introduction', 'owner', 'first_name', 'last_name', 'category',
                  'publish_date', 'slug', 'full_text', 'image', 'media']


class MyArticleListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field='name')

    class Meta:
        model = Article
        fields = ['uuid', 'title',
                  'introduction', 'owner', 'category', 'status', 'full_text',
                  'publish_date', 'slug',  'image', 'media', 'created_on']
        extra_kwargs = {

            'users': {'lookup_field': 'username'}
        }


class MyFavoriteListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    slug = serializers.StringRelatedField(source='article.slug')
    uuid = serializers.StringRelatedField(source='article.uuid')
    title = serializers.StringRelatedField(source='article.title')
    introduction = serializers.StringRelatedField(
        source='article.introduction')
    category = serializers.StringRelatedField(
        source='article.category', many=True)
    status = serializers.StringRelatedField(source='article.status')
    full_text = serializers.StringRelatedField(source='article.full_text')
    publish_date = serializers.StringRelatedField(
        source='article.publish_date')
    image = serializers.StringRelatedField(source='article.image')
    media = serializers.StringRelatedField(source='article.media')
    created_on = serializers.StringRelatedField(source='article.created_on')

    class Meta:
        model = Favorite
        fields = ['id', 'owner', 'slug', 'uuid', 'title',
                  'introduction', 'category', 'status', 'full_text',
                  'publish_date',  'image', 'media', 'created_on']


class ArticleDetailSerializer(serializers.ModelSerializer):
    articleid = serializers.ReadOnlyField(source='uuid')
    owner = serializers.ReadOnlyField(source='owner.username')
    first_name = serializers.ReadOnlyField(source='owner.first_name')
    last_name = serializers.ReadOnlyField(source='owner.last_name')
    category = category = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field='name')

    class Meta:
        model = Article
        fields = ['articleid', 'owner', 'first_name', 'last_name', 'title',
                  'introduction', 'full_text',  'category', 'image',
                  'media', 'publish_date', 'slug', 'publish_date']
        extra_kwargs = {
            'url': {'view_name': 'article-detail', 'lookup_field': 'slug'},
            'users': {'lookup_field': 'username'}
        }


class MyArticleDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    articleid = serializers.ReadOnlyField(source='uuid')
    first_name = serializers.ReadOnlyField(source='owner.first_name')
    last_name = serializers.ReadOnlyField(source='owner.last_name')
    category = category = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field='name')

    class Meta:
        model = Article
        fields = ['articleid', 'owner', 'first_name', 'last_name', 'title',
                  'introduction', 'full_text',  'category', 'image',
                  'media', 'publish_date', 'slug', 'publish_date']
        extra_kwargs = {
            'url': {'view_name': 'my-article-detail', 'lookup_field': 'slug'},
            'users': {'lookup_field': 'username'}
        }


class NewUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        password = validated_data['password']
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Article.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'articles')


class UserListSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Article.objects.all())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'articles')


class NewArticleSerializer(serializers.ModelSerializer):

    class Meta:

        model = Article
        fields = ['title', 'introduction', 'full_text', 'category', 'status', 'image',
                  'media', 'publish_date', 'answer_article']


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'article_in_category']


class CategoryDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Category
        fields = ['name',  'article_in_category', 'created_by', ]


class NewCategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category
        fields = ['name']


class NewCommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:

        model = Comment
        fields = ['text', 'article', 'id', 'owner']


class CommentListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:

        model = Comment
        fields = ['id', 'text', 'article', 'owner']


class CommentDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:

        model = Comment
        fields = ['id', 'text', 'article', 'owner']


class NewFollowSerializer(serializers.ModelSerializer):

    class Meta:

        model = Follow
        fields = ['user_followed']


class FollowListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    user_followed = serializers.ReadOnlyField(source='user_followed.username')

    class Meta:

        model = Follow
        fields = ['id', 'owner', 'user_followed']


class NewFavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:

        model = Favorite
        fields = ['article', 'owner', 'id']


class FavoriteListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    favorite_article = serializers.StringRelatedField(source='article.slug')

    class Meta:

        model = Favorite
        fields = ['id', 'owner', 'favorite_article']


class NewHighlightSerializer(serializers.ModelSerializer):

    class Meta:

        model = Highlight
        fields = ['article', 'highlight_content']


class HighlightListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:

        model = Highlight
        fields = ['id', 'owner', 'article', 'highlight_content']


class SearchListSerializer(serializers.ModelSerializer):
    key = serializers.ReadOnlyField(source='uuid')
    first_name = serializers.ReadOnlyField(source='owner.first_name')
    last_name = serializers.ReadOnlyField(source='owner.last_name')
    owner = serializers.SlugRelatedField(read_only=True, slug_field='username')
    category = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field='name')

    class Meta:
        model = Article
        fields = ['key', 'title',
                  'owner', 'first_name', 'last_name', 'category',
                  'publish_date', 'slug', 'introduction', 'status']
