# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _

from ferramentas.models.navegacao import Navegacao, NavegacaoItem
from ferramentas.models.favoritos import Favoritos, FavoritosItem
from ferramentas.models.ajuda import Ajuda, AjudaItem
from ferramentas.models.aviso import Aviso


def ativar(modeladmin, request, queryset):
    queryset.update(ativo=True)
ativar.short_description = "Setar como ativo os itens selecionados"

def inativar(modeladmin, request, queryset):
    queryset.update(ativo=False)
inativar.short_description = "Setar como inativo os itens selecionados"

class NavegacaoItemInline(admin.StackedInline):
    
    model = NavegacaoItem
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('', {
            'fields': ('titulo', 'link', 'categoria',)
        }),
        ('', {
            'fields': ('usuarios',),
        }),
        ('', {
            'fields': ('ordem',),
        }),
    )
    filter_horizontal = ('usuarios',)
    

class NavegacaoAdmin(admin.ModelAdmin):
    
    # List Options
    list_display = ('ordem', 'titulo',)
    list_display_links = ('titulo',)
    
    # Fieldsets
    fieldsets = (
        ('', {
            'fields': ('titulo', 'ordem',)
        }),
    )
    
    # Misc
    save_as = True
    
    # Inlines
    inlines = [NavegacaoItemInline]
    

class FavoritosItemInline(admin.TabularInline):
    
    model = FavoritosItem
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('', {
            'fields': ('titulo', 'link', 'ordem',)
        }),
    )
    

class FavoritosAdmin(admin.ModelAdmin):
    
    # List Options
    list_display = ('usuario',)
    list_display_links = ('usuario',)
    
    # Fieldsets
    fieldsets = (
        ('', {
            'fields': ('usuario',)
        }),
    )
    
    # Misc
    save_as = True
    
    # Inlines
    inlines = [FavoritosItemInline]
    
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(FavoritosAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if not change:
                obj.user = request.user
        obj.save()
    
    def queryset(self, request):
        if request.user.is_superuser:
            return Favoritos.objects.all()
        return Favoritos.objects.filter(usuario=request.user)
    




class AvisoAdmin(admin.ModelAdmin):
    
    # List Options
    list_display = ('ordem', 'titulo','status')
    list_display_links = ('titulo',)
    actions = [ativar, inativar]
    # Fieldsets
    fieldsets = (
        ('', {
            'fields': ('titulo', 'texto','usuarios','ativo')
        }),
    )
    
    # Misc
    save_as = True
    filter_horizontal = ('usuarios',)
      
    
    

admin.site.register(Navegacao, NavegacaoAdmin)
admin.site.register(Favoritos, FavoritosAdmin)
admin.site.register(Aviso, AvisoAdmin)

