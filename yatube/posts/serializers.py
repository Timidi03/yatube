from .models import Post, Tag, PostTag, Group
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='slug', required=False, queryset=Group.objects.all())
    character_quantity = serializers.SerializerMethodField()
    publication_date = serializers.CharField(source='pub_date')
    
    class Meta:
        model = Post
        fields = ('text', 'publication_date', 'author', 'group', 'image', 'character_quantity')
        
    def create(self, validated_data):
        if 'tag' not in self.initial_data:
            return Post.objects.create(**validated_data)
        
        tags = validated_data.pop('tag')
        post = Post.objects.create(**validated_data)
        for tag in tags:
            current_tag, _ = Tag.objects.get_or_create(**tag)
        PostTag.objects.create(post=post, tag=current_tag)
        return post
        
    def get_character_quantity(self, obj):
        return len(obj.text)
    
