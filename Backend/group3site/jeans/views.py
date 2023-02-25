from . import data_dict_helper as ddh
from django.http import HttpResponse
import os
from django.template import loader
from . import data_dict_helper


def index(request):
    out = """Hello, world. You're at the jeans index. """
    team = ["Brett Meirhofer", "Perminder Singh", "Laura Moreno"]
    solid_tables = data_dict_helper.get_solid_models("jeans")
    tables = []
    for table in solid_tables:
        tables.append(table._meta.verbose_name_plural)

    template = loader.get_template('jeans/index.html')
    context = {
        'tables': tables,
        'team': team,
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


# TODO Insert script for inserting test data
# TODO master script that combines Create -> Insert -> Alter scripts