from django.contrib import admin
from .models import Category, CategoryImage

# Register your models here.




class CategoryImageInline(admin.TabularInline):
    extra = 1
    model = CategoryImage
    prepopulated_fields = {"slug": ('title',)}



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    inlines = [CategoryImageInline,]

    class Meta:
        model = Category



admin.site.register(Category, CategoryAdmin)