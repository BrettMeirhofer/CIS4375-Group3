from django.db import models
import xlsxwriter
from django.apps import apps
import os

#employee_id int FOREIGN KEY REFERENCES Employee(id),
# Extracts the field props for a single field
# Could potentially pass a prop name/prop dictionary to define the order
def extract_field_props(current_field, model, field_type_dict):
    field_name = current_field.name
    field_type = type(current_field).__name__
    max_length = "NA" if current_field.max_length is None else current_field.max_length
    domain = "NA"
    if current_field.primary_key:
        help_text = model.pk_desc
    else:
        help_text = current_field.help_text

    if isinstance(current_field, models.fields.DecimalField):
        max_length = current_field.max_digits
        domain = "{} Decimals".format(current_field.decimal_places)

    if current_field.unique:
        if domain == "NA":
            domain = "UNIQUE"
        else:
            domain += "UNIQUE"

    c_delete = False
    c_update = False
    fk = False
    null = current_field.null
    if field_type == "ForeignKey":
        fk = True
        field_name += "_id"
        if null:
            c_update = True

    try:
        if field_type == "TextField":
            max_length = "max"
        field_type = field_type_dict[field_type]
    except KeyError:
        pass

    default = "NA" if current_field.default == models.fields.NOT_PROVIDED else current_field.default

    try:
        if current_field.auto_now_add:
            default = "CDate"

    except AttributeError:
        #Not a datefield
        pass

    pk = current_field.primary_key

    blank = True if current_field.primary_key else not current_field.blank
    return [field_name, help_text, default, max_length, field_type, pk, fk, blank, null, c_delete,
            c_update, domain]


# Given a model extracts a row of field properties for each field
# Title row could be passed as a parameter
# Field_type_dict could be a parameter
def extract_all_field_props(model, field_type_dict):
    model_object = model()
    model_fields = model_object._meta.get_fields(include_parents=False)
    visible_fields = []
    output_list = []
    visible_fields = [field for field in model_fields if
                      not isinstance(field, models.fields.reverse_related.ManyToOneRel)
                      and not isinstance(field, models.fields.reverse_related.ManyToManyRel)
                      and not isinstance(field, models.fields.related.ManyToManyField)]
    for current_field in visible_fields:
        output_row = extract_field_props(current_field, model, field_type_dict)
        output_list.append(output_row)
    return output_list


def generate_data_dict_excel(file_path, title_row, field_type_dict):
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    model_list = apps.get_app_config('jeans').get_models()
    max_lengths = []

    for col_index, title in enumerate(title_row):
        worksheet.write(0, col_index, title, bold)
        col_length = len(str(title))
        max_lengths.append(col_length)

    row_count = 1

    for row, model in enumerate(model_list):
        model_object = model()
        model_name = model._meta.db_table
        model_desc = model_object.description
        field_props = extract_all_field_props(model, field_type_dict)
        for count, props in enumerate(field_props):
            props.append(props.pop(1))
            if count == 0:
                props.insert(0, model_name)
                props.insert(0, model.load_order)
                props.append(model_desc)
            else:
                props.insert(0, " ")
                props.insert(0, " ")
                props.append(" ")

        for field_index, field in enumerate(field_props):
            for col_index, col in enumerate(field):
                worksheet.write(row_count, col_index, col)
                col_length = len(str(col))
                if col_length > max_lengths[col_index]:
                    max_lengths[col_index] = col_length

            row_count += 1
        row_count += 1

    for index, length in enumerate(max_lengths):
        worksheet.set_column(index, index, length * 1.25)

    header_dicts = []
    for row in title_row:
        header_dicts.append({"header": row})
    worksheet.add_table(0, 0, row_count, len(title_row) - 1, {"columns": header_dicts})
    workbook.close()


def get_solid_models(app_name):
    app = apps.get_app_config(app_name)
    solid_models = app.models.values()
    solid_models = [item() for item in solid_models]
    return [item for item in solid_models if not item._meta.abstract]


def generate_ordered_sql(app_name, order, statement, file_name):
    solid_tables = get_solid_models(app_name)
    solid_tables.sort(key=lambda x: x.load_order, reverse=order)
    module_dir = os.path.dirname(__file__)
    path = os.path.join(module_dir, "SQL", file_name)
    drop_file = open(path, "w")
    for table in solid_tables:
        drop_file.write(statement + " " + "\"" + table._meta.db_table + "\"" + "\n" + "\n")
    drop_file.close()


def generate_create_sql(app_name, field_type_dict):
    solid_tables = get_solid_models(app_name)
    solid_tables.sort(key=lambda x: x.load_order, reverse=False)
    module_dir = os.path.dirname(__file__)
    path = os.path.join(module_dir, "SQL", "Create.sql")
    drop_file = open(path, "w")
    for table in solid_tables:
        drop_file.write("CREATE TABLE " + table._meta.db_table + "(\n")
        drop_file.write("\tid int NOT NULL PRIMARY KEY IDENTITY(1,1),\n")

        model_fields = table._meta.get_fields(include_parents=False)
        visible_fields = [field for field in model_fields if
                          not isinstance(field, models.fields.reverse_related.ManyToOneRel)
                          and not isinstance(field, models.fields.reverse_related.ManyToManyRel)
                          and not isinstance(field, models.fields.related.ManyToManyField)
                          and not isinstance(field, models.ForeignKey)
                          and not isinstance(field, models.fields.AutoField)]

        for current_field in visible_fields:
            field_name = current_field.name
            field_type = field_type_dict[type(current_field).__name__]
            field_type_text = " " + field_type
            if field_type == "nvarchar":
                field_type_text = " nvarchar({})".format(current_field.max_length)
            null = ""
            default = ""
            if current_field.default != models.fields.NOT_PROVIDED:
                if field_type == "bit":
                    default = " DEFAULT {}".format(int(current_field.default))
                else:
                    default = " DEFAULT {}".format(current_field.default)
            if not current_field.null:
                null = " NOT NULL"
            unique = ""
            if current_field.unique:
                unique = " UNIQUE"
            drop_file.write("\t{}{}{}{}{},\n".format(field_name, field_type_text, null, default, unique))

        drop_file.write(");\n")
        drop_file.write("\n")
    drop_file.close()


def generate_alter_sql(app_name):
    solid_tables = get_solid_models(app_name)
    solid_tables.sort(key=lambda x: x.load_order, reverse=False)
    module_dir = os.path.dirname(__file__)
    path = os.path.join(module_dir, "SQL", "Alter.sql")
    drop_file = open(path, "w")
    for table in solid_tables:
        fk_fields = []
        for current_field in table._meta.get_fields(include_parents=False):
            if not isinstance(current_field, models.ForeignKey):
                continue
            fk_fields.append(current_field)

        if len(fk_fields) == 0:
            continue

        drop_file.write("ALTER TABLE " + table._meta.db_table + " ADD\n")

        for index, current_field in enumerate(fk_fields):
            end = ","
            if index == len(fk_fields) - 1:
                end = ";"
            drop_file.write("\t{}_id int FOREIGN KEY REFERENCES {}(id){}\n".format(current_field.name, current_field.related_model._meta.db_table, end))

        drop_file.write("\n")
    drop_file.close()
