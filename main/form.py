from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from .models import Product, Order

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 60}),
            'short_description': forms.TextInput(attrs={'size': 80}),
        }

    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data.get('stock_quantity')
        if stock_quantity < 0:
            raise forms.ValidationError("Stock quantity cannot be negative.")
        return stock_quantity

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'full_address': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        }

    def clean_total_amount(self):
        subtotal = self.cleaned_data.get('subtotal', 0)
        shipping_cost = self.cleaned_data.get('shipping_cost', 0)
        total_amount = self.cleaned_data.get('total_amount', 0)
        
        expected_total = subtotal + shipping_cost
        if abs(total_amount - expected_total) > 0.01:  # Allow for small rounding differences
            raise forms.ValidationError(
                f"Total amount should be {expected_total:.2f} (subtotal + shipping)"
            )
        return total_amount
