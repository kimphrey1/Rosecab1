from django import forms
from store.models import ProductVariant, Product, Size
from order.models import Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'desc', 'image', 'product_category']

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['title', 'size', 'price']

ProductVariantFormSet = forms.inlineformset_factory(
    parent_model=Product,
    model=ProductVariant,
    form=ProductVariantForm,
    extra=3,  # Set this to the number of forms you want to display initially
    can_delete=True,  # Set this to False to disable the delete checkbox
)





class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'paid']