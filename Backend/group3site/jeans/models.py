from django.db import models
from django import forms
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator
from decimal import Decimal
from django.forms.widgets import Input


IsManaged = False


class MoneyField(models.DecimalField):
    pass


class PhoneField(models.CharField):
    pass


def past_validator(value):
    if value > timezone.now().date():
        raise forms.ValidationError("The date must be in the past!")
    return value


def not_zero_validator(value):
    if value == 0:
        raise forms.ValidationError("The value cannot be zero")


def not_zero_validator(value):
    if value == 0:
        raise forms.ValidationError("The value cannot be zero")


class DescriptiveModel(models.Model):
    id = models.AutoField(primary_key=True)
    description = "Blank Description"
    pk_desc = "Standard Auto-Increment PK"
    load_order = -1

    class Meta:
        abstract = True
        managed = IsManaged


# Used as an abstract parent for status codes
class StatusCode(DescriptiveModel):
    description = "Used to soft delete rows with a reason name and desc"
    status_name = models.CharField(max_length=40, verbose_name="Name")
    status_desc = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    list_fields = ["status_name", "status_desc"]
    category = "Other"

    def __str__(self):
        return self.status_name

    class Meta:
        abstract = True
        managed = IsManaged


# Used as an abstract parent for labels
class LabelCode(DescriptiveModel):
    description = "Allows for multiple named categories"
    type_name = models.CharField(max_length=40, verbose_name="Name")
    type_desc = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    category = "Other"
    load_order = 1

    def __str__(self):
        return self.type_name

    class Meta:
        abstract = True
        managed = IsManaged


class Country(DescriptiveModel):
    description = 'A nation that an address can be located within'
    country_name = models.CharField(max_length=60, verbose_name="Name")
    load_order = 1
    list_fields = ["country_name"]

    def __str__(self):
        return self.country_name

    class Meta:
        db_table = "Country"
        verbose_name_plural = "Countries"
        verbose_name = "Country"
        managed = False


class State(DescriptiveModel):
    description = 'A state/province that an address can be located within'
    state_name = models.CharField(max_length=60, verbose_name="Name")
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, default=233, verbose_name="Country")
    load_order = 2
    list_fields = ["state_name", "country"]

    def __str__(self):
        return self.state_name

    class Meta:
        db_table = "StateProvince"
        verbose_name_plural = "State/Province"
        verbose_name = "State/Province"
        managed = False


class CustomerStatus(StatusCode):
    description = 'Refers to the current state of the customer'
    load_order = 1

    class Meta:
        db_table = "CustomerStatus"
        verbose_name = "Customer Status"
        verbose_name_plural = "Customer Status"
        managed = IsManaged


class ProductStatus(StatusCode):
    description = 'Refers to the current state of the product'
    load_order = 1

    class Meta:
        db_table = "ProductStatus"
        verbose_name = "Product Status"
        verbose_name_plural = "Product Status"
        managed = IsManaged


class PromoStatus(StatusCode):
    description = 'Refers to the current state of the promo'
    load_order = 1

    class Meta:
        db_table = "PromoStatus"
        verbose_name = "Promo Status"
        verbose_name_plural = "Promo Status"
        managed = IsManaged


class ProductTag(DescriptiveModel):
    description = 'Used to categorize Products. Each Product can an arbitrary number of tags'
    tag_name = models.CharField(max_length=40, verbose_name="Name")
    tag_desc = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    list_fields = ["tag_name", "tag_desc"]
    load_order = 1

    class Meta:
        db_table = "ProductTag"
        verbose_name = "Product Tag"
        verbose_name_plural = "Product Tags"
        managed = IsManaged

    def __str__(self):
        return self.tag_name


class Brand(DescriptiveModel):
    description = 'The company that owns the Brand for a product'
    brand_name = models.CharField(max_length=40, verbose_name="Name")
    brand_desc = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    brand_site = models.URLField(verbose_name="Website URL")
    load_order = 1
    list_fields = ["brand_name", "brand_site"]

    class Meta:
        db_table = "Brand"
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        managed = IsManaged

    def __str__(self):
        return self.brand_name


class Product(DescriptiveModel):
    description = 'Anything sold by a Store.'
    product_name = models.CharField(max_length=80, verbose_name="Name")
    product_desc = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    product_price = MoneyField(max_digits=19, decimal_places=4, verbose_name="Price $", default=0.00)
    product_brand = models.ForeignKey(Brand, on_delete=models.RESTRICT, blank=True, null=True, verbose_name="Brand")
    product_status = models.ForeignKey(ProductStatus, on_delete=models.RESTRICT, blank=True, null=True, verbose_name="Status")
    product_tags = models.ManyToManyField(ProductTag, through="ProductProductTag")
    created_date = models.DateField(verbose_name="Created Date")
    load_order = 2
    list_fields = ["product_name", "created_date", "product_status", "get_current_price"]
    list_func_names = {"get_current_price": "Price"}

    def get_current_price(self):
        test = "${0:.2f}".format(float(self.product_price))
        return test

    class Meta:
        db_table = "Product"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        managed = IsManaged

    def __str__(self):
        return self.product_name


class Promo(DescriptiveModel):
    description = 'Describes a promotion for a group of products most often a sale'
    promo_name = models.CharField(max_length=80, verbose_name="Name")
    promo_code = models.CharField(max_length=10, unique=True, verbose_name="Redemption Code")
    promo_status = models.ForeignKey(PromoStatus, on_delete=models.RESTRICT, verbose_name="Status")
    promo_products = models.ManyToManyField(Product, through="ProductPromo")
    created_date = models.DateField(verbose_name="Created Date")
    end_date = models.DateField(verbose_name="End Date", blank=True, null=True)
    promo_desc = models.TextField(max_length=400, verbose_name="Description", blank=True, null=True)
    load_order = 2
    list_fields = ["promo_name", "promo_code", "created_date", "end_date", "promo_status"]

    class Meta:
        db_table = "Promo"
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        managed = IsManaged

    def __str__(self):
        return self.promo_name


class ProductProductTag(DescriptiveModel):
    description = 'Used to associate a ProductTag with a Product'
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_tag = models.ForeignKey(ProductTag, on_delete=models.CASCADE)
    created_date = models.DateField()
    load_order = 3

    class Meta:
        db_table = "ProductProductTag"
        verbose_name_plural = "Product Product Tag"
        managed = IsManaged
        constraints = [
            models.UniqueConstraint(fields=['product', 'product_tag'], name='unique_product_tag')
        ]


class ProductImage(DescriptiveModel):
    description = 'An image with a caption that displays a product'
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    primary_image = models.BooleanField(verbose_name="Primary", default=False)
    image_url = models.URLField(verbose_name="Image URL")
    image_caption = models.CharField(max_length=200, blank=True, null=True, verbose_name="Caption")
    load_order = 3

    def getfk(self):
        return self.product

    def __str__(self):
        return self.image_caption

    class Meta:
        db_table = "ProductImage"
        verbose_name = "Product Image"
        verbose_name_plural = "Product Image"
        managed = IsManaged


class ProductPromo(DescriptiveModel):
    description = 'Used to associate a Product with a Promo and stores promo price data'
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE, verbose_name="Promo")
    current_price = MoneyField(max_digits=19, decimal_places=4, verbose_name="Current Price $", default=0.00)
    promo_price = MoneyField(max_digits=19, decimal_places=4, verbose_name="Promo Price $", default=0.00)
    display_product = models.BooleanField(verbose_name="Display", default=True)
    load_order = 4

    def getfk(self):
        return self.promo

    class Meta:
        db_table = "ProductPromo"
        verbose_name = "Product Promo"
        verbose_name_plural = "Product Promo"
        managed = IsManaged


class Customer(DescriptiveModel):
    description = 'Name and email for a customer who will recieve promo emails'
    first_name = models.CharField(max_length=200, verbose_name="First Name")
    last_name = models.CharField(max_length=200, verbose_name="Last Name")
    email = models.EmailField(verbose_name="Email Address")
    phone_regex = RegexValidator(regex=r'[0-9]{3}-[0-9]{3}-[0-9]{4}',
                                 message="Phone number must be entered in the format: 'xxx-xxx-xxxx'.")
    created_date = models.DateField(verbose_name="Created Date")
    customer_status = models.ForeignKey(CustomerStatus, on_delete=models.RESTRICT, verbose_name="Status")
    phone_number = PhoneField(validators=[phone_regex], max_length=12, blank=True,
                              null=True, verbose_name="Phone Number")  # Validators should be a list
    zip_code = models.CharField(max_length=10, verbose_name="Zip Code")
    city = models.CharField(max_length=35, default="Houston", verbose_name="City")
    address = models.CharField(max_length=100, default="3242 StreetName", verbose_name="Address")
    state = models.ForeignKey(State, on_delete=models.RESTRICT, default=1407, verbose_name="State")
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, default=233, verbose_name="Country")
    load_order = 3
    list_fields = ["first_name", "last_name", "email", 'phone_number', "created_date", "customer_status"]

    def __str__(self):
        return self.email

    class Meta:
        db_table = "Customer"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        managed = IsManaged


class CustomerPromo(DescriptiveModel):
    description = 'Records when a customer redeems a promo. Key data point for promo success'
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE, verbose_name="Promo")
    total_spent = MoneyField(max_digits=19, decimal_places=4, verbose_name="Total Spent $", default=0.00)
    total_discount = MoneyField(max_digits=19, decimal_places=4, verbose_name="Total Discount $", default=0.00)
    created_date = models.DateField(verbose_name="Created Date")
    load_order = 5

    list_fields = ["customer", "promo", "created_date"]

    def __str__(self):
        return str(self.customer) + " (" + str(self.id) + ")"

    class Meta:
        db_table = "CustomerPromo"
        verbose_name = "Customer Promo"
        verbose_name_plural = "Customer Promo"
        managed = IsManaged


class CustomerProductPromo(DescriptiveModel):
    description = 'Records the promotional products a customer redeems a promo for'
    customer_promo = models.ForeignKey(CustomerPromo, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    normal_price = MoneyField(max_digits=19, decimal_places=4, verbose_name="Normal Price $", default=0.00)
    promo_price = MoneyField(max_digits=19, decimal_places=4, verbose_name="Promo Price $", default=0.00)
    line_total = MoneyField(max_digits=19, decimal_places=4, verbose_name="Line Total $", default=0.00)
    line_discount = MoneyField(max_digits=19, decimal_places=4, verbose_name="Line Discount $", default=0.00)
    one_validator = MinValueValidator(limit_value=1, message="Value cannot be less then one")
    quantity = models.IntegerField(verbose_name="Quantity", default=1, validators=[one_validator])
    load_order = 6

    list_fields = []

    class Meta:
        db_table = "CustomerProductPromo"
        verbose_name = "Customer Product Promo"
        verbose_name_plural = "Customer Product Promo"
        managed = IsManaged
        constraints = [
            models.UniqueConstraint(fields=['customer_promo', 'product'], name='unique_line_products')
        ]