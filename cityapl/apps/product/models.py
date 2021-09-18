import datetime

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class State(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=128)

    class Meta:
        db_table = 'state'


class City(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    state = models.ForeignKey(State,
        on_delete=models.CASCADE, db_column='stateId')
    cityName = models.CharField(max_length=128)

    class Meta:
        db_table = 'city'


class Category(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=128, unique=True)
    catImg = models.FileField(upload_to='product/category')
    isActive = models.BooleanField(default=True)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    updatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='cat_updated_by')
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='cat_created_by')

    class Meta:
        db_table = 'category'


class SubCategory(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category,
        on_delete=models.CASCADE, db_column='categoryId')
    subCategoryName = models.CharField(max_length=128, unique=True)
    subCatImg = models.FileField(upload_to='product/subcategory')
    isActive = models.BooleanField(default=True)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    updatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,db_column='updatedById', related_name='subcat_updated_by')
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,db_column='createdById', related_name='subcat_created_by')

    class Meta:
        db_table = 'subcategory'




class Vertical(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    subCategory = models.ForeignKey(SubCategory,
        on_delete=models.CASCADE, db_column='subCategoryId',)
    verticalName = models.CharField(max_length=128, unique=True)
    verticalImg = models.FileField(upload_to='product/vertical')
    isActive = models.BooleanField()
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    updatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,db_column='updatedById', related_name='vartical_updated_by')
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,db_column='createdById', related_name='vartical_created_by')

    class Meta:
        db_table = 'vertical'


class Brand(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    brandName = models.CharField(max_length=128, unique=True)
    brandImg = models.FileField(blank=True, null=True, upload_to='product/brand')
    description = models.TextField(blank=True, null=True)

    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    updatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,db_column='updatedById', related_name='brand_updated_by')
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,db_column='createdById', related_name='brand_created_by')

    vertical = models.ManyToManyField(Vertical,
        through='BrandInVertical')

    class Meta:
        db_table = 'brands'


class BrandInVertical(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brand,
        on_delete=models.CASCADE, db_column='brandId')
    vertical = models.ForeignKey(Vertical,
        on_delete=models.CASCADE, db_column='verticalId')
    isActive = models.BooleanField(default=True)
    brandRating = models.FloatField(default=0.0)

    class Meta:
        db_table = 'brand_in_vertical'


class AttributeSection(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'attribute_section'


class Attribute(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    attribute_name = models.CharField(max_length=255, unique=True)
    displayName = models.CharField(max_length=255)
    fieldType = models.CharField(max_length=64, blank=True)
    isRequired = models.BooleanField(default=False)
    isMultiselect = models.BooleanField(default=False)
    options = ArrayField(models.CharField(max_length=200), blank=True)

    parent_id = models.ForeignKey('self',
        on_delete=models.CASCADE, db_column='parentVerticalId',
        blank=True, null=True)
    sectionType = models.ForeignKey(AttributeSection,
        on_delete=models.CASCADE, db_column='sectionTypeId')

    vertical = models.ManyToManyField(Vertical,
        through='AttributeInVertical') 

    class Meta:
        db_table = 'attribute'


class AttributeInVertical(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    vertical = models.ForeignKey(Vertical,
        on_delete=models.CASCADE, db_column='verticalId')
    attribute = models.ForeignKey(Attribute,
        on_delete=models.CASCADE, db_column='attributeId')

    class Meta:
        db_table = 'attribute_in_vertical'


class Product(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category,
        on_delete=models.CASCADE, db_column='categoryId')
    subCategory = models.ForeignKey(SubCategory,
        on_delete=models.CASCADE,db_column='subCategoryId')
    vertical = models.ForeignKey(Vertical,
        on_delete=models.CASCADE, related_name='product', db_column='verticalId')

    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand,
        on_delete=models.CASCADE, related_name='product_brand', db_column='BrandId')
    description = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    searchTags = models.TextField(blank=True, null=True)

    attributs = models.ManyToManyField(Attribute,
        through='AttributeInProduct') 

    mrp = models.PositiveIntegerField(blank=True, null=True)
    isActive = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)

    rating = models.FloatField(default=0.0)

    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    updatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,db_column='updatedById', related_name='product_updated_by')
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,db_column='createdById',  related_name='product_created_by')

    class Meta:
        db_table = 'product'


class AttributeInProduct(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    attribute = models.ForeignKey(Attribute,
        on_delete=models.CASCADE, db_column='attributeId')
    product = models.ForeignKey(Product,
        on_delete=models.CASCADE, db_column='productId')
    values = ArrayField(models.CharField(max_length=200), blank=True)

    class Meta:
        db_table = 'attribute_in_product'


class ProductImage(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product,
        on_delete=models.CASCADE, db_column='productId')
    image = models.ImageField(upload_to='product/product')
    isMain = models.BooleanField(default=False)
    createdAt = models.DateTimeField()
    
    class Meta:
        db_table = 'product_image'