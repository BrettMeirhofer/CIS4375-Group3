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


def index(request):
    out = """Hello, world. You're at the jeans index. """
    team = ["Brett Meirhofer", "Perminder Singh", "Laura Moreno, Daniel Thomas"]
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
                       "URLField": "nvarchar"}


def dict3(request):
    title_row = ["Load Order", "Table Name", "Row Name", "Default", "Max Length", "Type", "PK", "FK",
                 "Required", "Allow NULL", "C Delete", "C Update", "Domain", "Row Desc", "Table Desc"]
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
    ddh.generate_alter_sql("jeans")
    return HttpResponse("Success")


def generate_sql_all(request):
    ddh.generate_ordered_sql("jeans", True, "DROP TABLE", "Drop.sql")
    ddh.generate_create_sql("jeans", FieldTypeMap.field_type_dict)
    ddh.generate_ordered_sql("jeans", True, "DELETE FROM", "Delete.sql")
    ddh.generate_alter_sql("jeans")
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
        'headers': current_table.list_headers,
        'title': current_table._meta.db_table,
        'fields': current_table.list_fields
    }
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


def add_row(request, table):
    if request.method == 'POST':
        current_form = None
        for form in forms.form_listing:
            if form._meta.model._meta.db_table.lower() == table.lower():
                current_form = form

        form = current_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/listall/' + table + "/")

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

    form = current_form()
    template = loader.get_template('jeans/editview.html')
    context = {
        'form': form,
        'action': "/add_row/{}/".format(table)
    }
    return HttpResponse(template.render(context, request))


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

    if request.method == 'POST':
        form = current_form(request.POST, instance=current_row)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/listall/' + table + "/")

    form = current_form(None, instance=current_row)
    template = loader.get_template('jeans/editview.html')
    context = {
        'form': form,
        'action': "/edit_row/{}/{}/".format(table, id)
    }
    return HttpResponse(template.render(context, request))

# TODO Insert script for inserting test data
# TODO master script that combines Create -> Insert -> Alter scripts
