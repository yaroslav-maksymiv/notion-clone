from rest_framework import serializers
from .models import (
    Page, Text, Heading_2, Heading_1, Page_element,
    PageLink, To_do, Code
)


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'


class Heading_2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Heading_2
        fields = '__all__'


class Heading_1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Heading_1
        fields = '__all__'


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__'


class PageLinkSerializer(serializers.ModelSerializer):
    page_id = serializers.IntegerField(source='page.id')
    page_name = serializers.CharField(source='page.name')
    page_photo = serializers.CharField(source='page.photo')

    class Meta:
        model = PageLink
        fields = ['id', 'page_id', 'page_name', 'page_photo', 'page_element']


class To_doSerializer(serializers.ModelSerializer):
    class Meta:
        model = To_do
        fields = '__all__'        


class Page_elementSerializer(serializers.ModelSerializer):
    heading_1 = Heading_1Serializer(many=True, read_only=True)
    heading_2 = Heading_2Serializer(many=True, read_only=True)
    text = TextSerializer(many=True, read_only=True)
    page_link = PageLinkSerializer(many=True, read_only=True)
    to_do = To_doSerializer(many=True, read_only=True)
    code = CodeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Page_element
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class PageChildrenSerializer(serializers.ModelSerializer):
    child_pages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Page
        fields = ['id', 'child_pages']

    def get_child_pages(self, instance):
        child_pages = instance.children.all()
        return PageSerializer(child_pages, many=True, read_only=True).data


class PageFullSerializer(serializers.ModelSerializer):
    page_elements = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Page
        fields = '__all__'

    def get_page_elements(self, instance):
        elements = instance.page_elements.all().order_by('order_on_page')
        return Page_elementSerializer(elements, many=True, read_only=True).data

    def get_parent(self, obj):
        parent = obj.parent
        parent_list = []
        while parent is not None:
            parent_list.append(parent)
            parent = parent.parent
        return [{'id': parent.id, 'name': parent.name, 'photo': parent.photo} for parent in reversed(parent_list)]
