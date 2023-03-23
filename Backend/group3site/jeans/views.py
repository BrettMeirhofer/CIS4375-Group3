from . import data_dict_helper as ddh
from django.http import HttpResponse
import os
from django.template import loader
from . import data_dict_helper
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from . import models
from . import forms
from django.apps import apps
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)


def index(request):
    out = """Hello, world. You're at the jeans index. """
    team = ["Brett Meirhofer", "Perminder Singh", "Laura Moreno" , "Daniel Thomas", "Alex Bermudez", "Daniel Hernandez"]
    solid_tables = data_dict_helper.get_solid_models("jeans")
    tables = []
    for table in solid_tables:
        tables.append(table._meta.verbose_name_plural)

    form = forms.ProductForm()
    template = loader.get_template('jeans/index.html')
    context = {
        'tables': tables,
        'team': team,
        'form': form,
        'form2': forms.PromoForm(),
    }
    return HttpResponse(template.render(context, request))


class FieldTypeMap:
    field_type_dict = {"CharField": "nvarchar", "DateField": "date", "BooleanField": "bit", "BigAutoField": "bigint",
                       "EmailField": "nvarchar", "TextField": "nvarchar", "ForeignKey": "int", "IntegerField": "int",
                       "DecimalField": "numeric", "AutoField": "int", "PhoneNumberField": "nvarchar",
                       "URLField": "nvarchar", "MoneyField": "numeric"}


def dict3(request):
    title_row = ["Load Order", "Table Name", "Attribute Name", "Default", "Max Length", "Type", "PK", "FK",
                 "Required", "Allow NULL", "C Delete", "C Update", "Domain", "Attribute Desc", "Table Desc"]
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, "GeneratedFiles", "DataDict.xlsx")
    ddh.generate_data_dict_excel(file_path, title_row, FieldTypeMap.field_type_dict)
    final_sheet = open(file_path, "rb")
    response = HttpResponse(final_sheet,
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return response


def generate_drop(request):
    ddh.generate_ordered_sql("jeans", True, "DROP TABLE", "Drop.sql")
    return HttpResponse("Success")


# Generates a correctly ordered delete script
def generate_delete(request):
    ddh.generate_ordered_sql("jeans", True, "DELETE FROM", "Delete.sql")
    return HttpResponse("Success")


def generate_create(request):
    ddh.generate_create_sql("jeans", FieldTypeMap.field_type_dict)
    return HttpResponse("Success")


def generate_alter(request):
    return HttpResponse("Success")


def generate_sql_all(request):
    ddh.generate_ordered_sql("jeans", True, "DROP TABLE", "Drop.sql")
    ddh.generate_create_sql("jeans", FieldTypeMap.field_type_dict)
    ddh.generate_ordered_sql("jeans", True, "DELETE FROM", "Delete.sql")
    ddh.generate_insert_sql("jeans")
    return HttpResponse("Success")


def view_products(request):
    solid_tables = data_dict_helper.get_solid_models("jeans")
    output = ', \n'.join([q._meta.verbose_name_plural for q in solid_tables])
    return HttpResponse(output)


def view_products_list(request, table):
    app = apps.get_app_config("jeans")
    app_models = app.models.values()
    current_table = None
    for model in app_models:
        if model._meta.db_table.lower() == table.lower():
            current_table = model

    if not current_table:
        return HttpResponse("Failed")

    paginator = Paginator(current_table.objects.all(), 10)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = loader.get_template('jeans/listview.html')
    context = {
        'page_obj': page_obj,
        'title': current_table._meta.db_table,
    }
    if hasattr(current_table, "list_headers") and hasattr(current_table, "list_fields"):
        context["fields"] = current_table.list_fields
        context["headers"]: current_table.list_headers
    return HttpResponse(template.render(context, request))


def delete_single(request, table, id):
    app = apps.get_app_config("jeans")
    app_models = app.models.values()
    current_table = None
    for model in app_models:
        if model._meta.db_table.lower() == table.lower():
            current_table = model

    current_table.objects.filter(id=id).delete()
    return HttpResponseRedirect('/listall/' + table + "/")


def create_single(request, table):
    app = apps.get_app_config("jeans")
    app_models = app.models.values()
    current_table = None
    for model in app_models:
        if model._meta.db_table.lower() == table.lower():
            current_table = model

    current_form = None
    for target_form in forms.form_listing:
        if target_form._meta.model == current_table:
            current_form = target_form

    form = current_form(request.POST or None)

    formsets = []
    if hasattr(form, "formsets"):
        for formset in form.formsets:
            formsets.append(formset(request.POST or None, request.FILES or None, prefix='variants'))

    if request.method == 'POST':
        result = save_form(form, formsets, table)
        if result is not None:
            return result

    template = loader.get_template('jeans/product_create_or_update.html')
    context = {
        'form': form,
        'action': "/create_row/{}/".format(table),
        'formsets': formsets,
    }
    return HttpResponse(template.render(context, request))


def save_form(form, formsets, table):
    if not all((x.is_valid() for x in formsets)):
        return None

    if not form.is_valid():
        return None

    saved_instance = form.save()
    for formset in formsets:
        variants = formset.save(commit=False)  # self.save_formset(formset, contact)
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in variants:
            formset.form.setfk(formset.form, instance=variant, parentinstance=saved_instance)
            variant.save()

    return HttpResponseRedirect('/listall/' + table + "/")


def edit_single(request, table, id):
    app = apps.get_app_config("jeans")
    app_models = app.models.values()
    current_table = None
    for model in app_models:
        if model._meta.db_table.lower() == table.lower():
            current_table = model

    current_form = None
    for target_form in forms.form_listing:
        if target_form._meta.model == current_table:
            current_form = target_form

    current_row = current_table.objects.get(id=id)
    form = current_form(request.POST or None, instance=current_row)

    formsets = []
    if hasattr(form, "formsets"):
        for formset in form.formsets:
            formsets.append(formset(request.POST or None, request.FILES or None, prefix='variants', instance=current_row))

    if request.method == 'POST':
        result = save_form(form, formsets, table)
        if result is not None:
            return result

    template = loader.get_template('jeans/product_create_or_update.html')
    context = {
        'form': form,
        'action': "/edit_row/{}/{}/".format(table, id),
        'formsets': formsets,
    }
    return HttpResponse(template.render(context, request))


def generate_insert(request):
    ddh.generate_insert_sql("jeans", FieldTypeMap.field_type_dict)
    return HttpResponse("Success")


class ProductPromoInline():
    form_class = forms.PromoForm
    model = models.Promo
    template_name = "jeans/product_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            variants = formset.save(commit=False)  # self.save_formset(formset, contact)
            for obj in formset.deleted_objects:
                obj.delete()
            for variant in variants:
                print(self.object)
                variant.promo = self.object
                variant.save()

        return HttpResponseRedirect("/listall/promo/")


class ProductCreate(ProductPromoInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'variants': forms.ProductPromoFormSet(prefix='variants'),
            }
        else:
            return {
                'variants': forms.ProductPromoFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants'),
            }


class ProductUpdate(ProductPromoInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'variants': forms.ProductPromoFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='variants'),
        }