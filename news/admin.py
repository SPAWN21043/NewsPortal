from django.contrib import admin
from .models import Post, PostCategory, Author, Category, Comment


# ������ ����� ����� ��� ������������� ������� � �������
class PostAdmin(admin.ModelAdmin):
    # list_display � ��� ������ ��� ������ �� ����� ������, ������� �� ������ ������ � ������� � ��������
    list_display = ('post_user', 'is_news', 'date_create', 'heading', 'text', 'rating_post', 'categories') # ���������� ������ ��� ���� ����� ��� ����� ��������� �����������
    list_filter = ('post_user', 'is_news', 'date_create', 'heading', 'rating_post')
    search_fields = ('is_news',)

    def categories(self, obj):
        return ",".join([p.name_category for p in obj.categ.all()])


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

