import django.db.models
from . import data_dict_helper as ddh
from django.http import HttpResponse
import os
from django.db import connection
from django.template import loader
from . import data_dict_helper
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from . import models
from . import forms
from django.shortcuts import render
from .models import Customer, CustomerPromo, Promo
from django.db.models import Count
import glob
from django.apps import apps
from django.core.exceptions import FieldDoesNotExist
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.db import connection, ProgrammingError, DataError
import json
from datetime import date


def index(request):
    template = loader.get_template('jeans/index.html')
    return HttpResponse(template.render({}, request))


class FieldTypeMap:
    field_type_dict = {"CharField": "nvarchar", "DateField": "date", "BooleanField": "bit", "BigAutoField": "bigint",
                       "EmailField": "nvarchar", "TextField": "nvarchar", "ForeignKey": "int", "IntegerField": "int",
                       "DecimalField": "numeric", "AutoField": "int", "PhoneNumberField": "nvarchar",
                       "URLField": "nvarchar", "MoneyField": "numeric", "CurrencyField": "nvarchar",
                       "PhoneField": "nvarchar"}


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
    order_by = request.GET.get('order_by')
    if order_by is None:
        order_by = "id"

    direction = request.GET.get('direction')
    if direction is None:
        direction = "asc"

    app = apps.get_app_config("jeans")
    app_models = app.models.values()
    current_table = None
    for model in app_models:
        if model._meta.db_table.lower() == table.lower():
            current_table = model

    if not current_table:
        return HttpResponse("Failed")

    list_fields = current_table.list_fields
    headers = []
    for field in list_fields:
        try:
            headers.append({"title": current_table._meta.get_field(field).verbose_name, "name":current_table._meta.get_field(field).name})
        except FieldDoesNotExist:
            headers.append({"title": current_table.list_func_names[field], "name": None})

    ordering = order_by.lower()
    if direction == 'desc':
        ordering = '-{}'.format(ordering)
    paginator = Paginator(current_table.objects.all().order_by(ordering), 25)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = loader.get_template('jeans/listview.html')
    context = {'page_obj': page_obj, 'title': current_table._meta.verbose_name_plural, "fields": list_fields,
               "headers": headers, "table": table,  'order_by': order_by, 'direction': direction,}
    return HttpResponse(template.render(context, request))


def delete_single(request, table, id):
    app = apps.get_app_config("jeans")
    app_models = app.models.values()
    current_table = None
    for model in app_models:
        if model._meta.db_table.lower() == table.lower():
            current_table = model

    template = loader.get_template('jeans/deletefailed.html')
    try:
        current_table.objects.filter(id=id).delete()
        return HttpResponseRedirect('/listall/' + table + "/")
    except django.db.IntegrityError as e:
        context = {'error': "Cannot delete rows due to ForeignKey constraint."}
        return HttpResponse(template.render(context, request))



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
        'title': current_table._meta.verbose_name
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
        'edit': True,
        'table': table,
        'id': id,
        'instance': current_row,
        'title': current_table._meta.verbose_name
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


def graph_view(file):
    module_dir = os.path.dirname(__file__)
    path = os.path.join(os.path.dirname(module_dir), "jeans", "SQL", "Graphs",
                        file)
    sql = open(path).read()
    with connection.cursor() as cursor:
        cursor.execute(sql)
        sql_output = cursor.fetchall()

    response_data = {"labels": [], "data": []}
    for row in sql_output:
        response_data["labels"].append(row[0])
        response_data["data"].append(str(row[1]))
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def graph_view_month(file):
    module_dir = os.path.dirname(__file__)
    path = os.path.join(os.path.dirname(module_dir), "jeans", "SQL", "Graphs",
                        file)
    sql = open(path).read()
    with connection.cursor() as cursor:
        cursor.execute(sql)
        sql_output = cursor.fetchall()

    response_data = {"labels": ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], "data": []}
    for i in response_data["labels"]:
        response_data["data"].append('0')
    for row in sql_output:
        response_data["data"].insert(row[0]-1, str(row[1]))
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def top5_cust(request):
    return graph_view("Top5_Cust_Promo.sql")


def top5_promos(request):
    return graph_view("Top5_Promo_Redeem.sql")


def uniq_cust_month(request):
    return graph_view_month("UniqueCustMonth.sql")


def delete_rows(request):
    app = apps.get_app_config("jeans")
    app_models = app.models.values()
    current_table = None
    data = request.POST.dict()
    print(request.POST)
    for model in app_models:
        if model._meta.db_table.lower() == data["table"].lower():
            current_table = model

    if not current_table:
        return HttpResponse("Failed")

    print(current_table)
    rows = request.POST.getlist('rows[]')
    rows = [int(i) for i in rows]
    try:
        current_table.objects.filter(pk__in=rows).delete()
    except django.db.IntegrityError as e:
        return HttpResponse("Cannot delete rows due to ForeignKey constraint.")

    return HttpResponse(200)

def promo_email_page(request):
    solid_tables = data_dict_helper.get_solid_models("jeans")
    tables = []
    for table in solid_tables:
        tables.append(table._meta.verbose_name_plural)

    template = loader.get_template('jeans/send_promos.html')
    promos = models.Promo.objects.filter(promo_status=1)
    context = {
        "promos": promos
    }
    return HttpResponse(template.render(context, request))


def preview_promo(request):
    promo = models.Promo.objects.get(id=int(request.POST["id"]))
    return render_promo(request, promo)


def render_promo(request, promo):
    solid_tables = data_dict_helper.get_solid_models("jeans")
    tables = []
    for table in solid_tables:
        tables.append(table._meta.verbose_name_plural)

    template = loader.get_template('jeans/promo.html')
    products = promo.promo_products.all()
    images = models.ProductImage.objects.filter(product__in=products)
    context = {
        "promo": promo,
        "products": products,
        "images": images
    }
    return HttpResponse(template.render(context, request))


def print_promo(request, id):
    promo = models.Promo.objects.get(id=id)
    return render_promo(request,promo)


def top_promos(request):
    # Get top promos being used
    promo_customer_counts = CustomerPromo.objects.values('promo_id').annotate(customer_count=Count('customer_id', distinct=True)).order_by('-customer_count')[:10]
    promo_ids = [row['promo_id'] for row in promo_customer_counts]
    promos = Promo.objects.filter(id__in=promo_ids).values('id', 'promo_name', 'promo_code', 'promo_desc')
    top_promos_data = [{'promo': {'id': promo['id'], 'name': promo['promo_name'], 'code': promo['promo_code'], 'desc': promo['promo_desc']}, 'customer_count': row['customer_count']} for row, promo in zip(promo_customer_counts, promos)]


def report(request):
    paths, names = get_report_paths()
    context = {"reports": names}
    return render(request, 'jeans/report.html', context)


def top_customers(request):
    # Define the base directory for the SQL files
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SQL', 'Reports')
    
    # Build the path to the TopCustomers.sql file
    sql_file_path = os.path.join(base_dir, 'ReportTopCustomer.sql')
    
    with open(sql_file_path, 'r') as file:
        sql_query = file.read()

    # Execute the SQL query
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        result = cursor.fetchall()

    # Pass the result to the template
    context = {'top_customers': result}
    return render(request, 'jeans/print_report.html', context)


class ReportData:
    owner = ""
    name = ""
    rule = ""
    desc = ""
    data = []
    titles = []
    sql = []

    def __init__(self, owner, name, rule, data, titles, sql, desc):
        self.owner = owner
        self.name = name
        self.rule = rule
        self.data = data
        self.titles = titles
        self.sql = sql
        self.desc = desc


def build_report_obj(path):
    print(path)
    with open(path, "r") as report_object:
        report_text = report_object.readlines()

    owner = report_text.pop(0).replace("--", "")
    name = report_text.pop(0).replace("--", "")
    rule = report_text.pop(0).replace("--", "")
    desc = report_text.pop(0).replace("--", "")
    titles = report_text.pop(0).replace("--", "").split(",")
    align = report_text.pop(0).replace("--", "").replace("\n", "").split(",")

    with open(path, "r") as report_object:
        sql = report_object.read()

    with connection.cursor() as cursor:
        cursor.execute(sql)
        output = cursor.fetchall()

        new_output = []
        for row in output:
            new_row = []
            for index, column in enumerate(row):
                col_class = align[index]
                new_row.append([column, col_class])
            new_output.append(new_row)

    report_data = ReportData(owner, name, rule, new_output, titles, report_text, desc)
    return report_data


def get_reports(path):
    return glob.glob(os.path.join(path, "SQL/Reports/Report*"))


def get_report_paths():
    module_dir = os.path.dirname(__file__)
    paths = get_reports(module_dir)
    out = []
    print(paths)

    for path in paths:
        print(path)
        name = open(path).readlines()[1]
        name = name.replace("--", "")
        out.append([name, path])
    out.sort(key=lambda x: x[0].replace(" ", ""))
    paths = []
    names = []
    for element in out:
        paths.append(element[1])
        names.append(element[0])
    return paths, names


def html_report(request, index):
    paths, names = get_report_paths()
    file_path = paths[index]
    context = {"report": build_report_obj(file_path), "date": date.today()}
    return render(request, 'jeans/print_report.html', context)



