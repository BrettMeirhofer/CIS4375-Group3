from django.db import models
from django import forms
#from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import os
from django.db import connection


def past_validator(value):
    if value > timezone.now().date():
        raise forms.ValidationError("The date must be in the past!")
    return value


def not_zero_validator(value):
    if value == 0:
        raise forms.ValidationError("The value cannot be zero")


class MoneyField(models.DecimalField):
    def __init__(self):
        super().__init__(max_digits=19, decimal_places=4, default=0)

    def __str__(self):
        return "$" + super.__str__(self)

    widget = forms.Textarea


class DescriptiveModel(models.Model):
    id = models.AutoField(primary_key=True)
    description = "Blank Description"
    pk_desc = "Standard Auto-Increment PK"
    load_order = -1

    class Meta:
        abstract = True
        managed = False


# Used as an abstract parent for status codes
class StatusCode(DescriptiveModel):
    description = "Used to soft delete rows with a reason name and desc"
    status_name = models.CharField(max_length=40)
    status_desc = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    category = "Other"

    def __str__(self):
        return self.status_name

    class Meta:
        abstract = True
        managed = False


# Used as an abstract parent for labels
class LabelCode(DescriptiveModel):
    description = "Allows for multiple named categories"
    type_name = models.CharField(max_length=40)
    type_desc = models.CharField(max_length=200, blank=True, null=True)
    category = "Other"
    load_order = 1

    def __str__(self):
        return self.type_name

    class Meta:
        abstract = True
        managed = False


class ProductStatus(StatusCode):
    description = 'Refers to the current state of the product'
    load_order = 1

    class Meta:
        db_table = "ProductStatus"
        verbose_name_plural = "Product Status"
        managed = False


class ProductTag(StatusCode):
    description = 'Used to categorize Products'
    load_order = 1

    class Meta:
        db_table = "ProductTag"
        verbose_name_plural = "Product Tag"
        managed = False


class Brand(DescriptiveModel):
    description = 'The Brand that supplies certain Products'
    brand_name = models.CharField(max_length=80)
    brand_desc = models.CharField(max_length=200, blank=True, null=True)
    brand_site = models.URLField()
    load_order = 1

    class Meta:
        db_table = "Brand"
        verbose_name_plural = "Brand"
        managed = False

    def __str__(self):
        return self.brand_name


class Product(DescriptiveModel):
    description = 'Anything sold by a Store'
    product_name = models.CharField(max_length=80)
    product_desc = models.CharField(max_length=200, blank=True, null=True)
    product_price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    product_brand = models.ForeignKey(Brand, on_delete=models.RESTRICT)
    product_tags = models.ManyToManyField(ProductTag, through="ProductProductTag")
    load_order = 2

    class Meta:
        db_table = "Product"
        verbose_name_plural = "Product"
        managed = False

    def __str__(self):
        return self.product_name


class ProductProductTag(StatusCode):
    description = 'Used to associate a ProductTag with a Product'
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    product_tag = models.ForeignKey(ProductTag, on_delete=models.RESTRICT)
    load_order = 3

    class Meta:
        db_table = "ProductProductTag"
        verbose_name_plural = "Product Product Tag"
        managed = False
