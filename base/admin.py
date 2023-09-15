from django.contrib import admin

from .models import (
    Page, Page_element, Text, Heading_1, Heading_2, PageLink, To_do, Code
)


class TextAdmin(admin.ModelAdmin):
    list_display = ('id', 'page_element', 'text')
    ordering = ["-id"] 


class HeadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'page_element', 'heading_text')
    ordering = ["-id"] 


class PageLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'page_element') 
    ordering = ["-id"]   


class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')  
    ordering = ["-id"]  


class To_doAdmin(admin.ModelAdmin):
    list_display = ('id', 'completed', 'description')   
    ordering = ["-id"]   


class CodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'language')  
    ordering = ["-id"]       


admin.site.register(Page, PageAdmin)
admin.site.register(Page_element)
admin.site.register(Text, TextAdmin)
admin.site.register(Heading_1, HeadingAdmin)
admin.site.register(Heading_2, HeadingAdmin)
admin.site.register(PageLink)
admin.site.register(To_do, To_doAdmin)
admin.site.register(Code, CodeAdmin)