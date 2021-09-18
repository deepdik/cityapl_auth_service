from .models import *
from django.contrib import admin


admin.site.register([Category, SubCategory, Brand, Vertical, Product,
	 Attribute, BrandInVertical, AttributeSection, AttributeInVertical,
	 AttributeInProduct, ProductImage])