from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product Name")
    description = models.TextField(verbose_name="Product Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(verbose_name="Stock Quantity", validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Product Image")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.IntegerField(verbose_name="Quantity", validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"Cart for {self.user.username} with {self.quantity} x {self.product.name}"

    def total_price(self):
        return self.quantity * self.product.price

    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError(f"Only {self.product.stock} units of {self.product.name} are available.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ['-created_at']
        unique_together = ['user', 'product']  # Prevent duplicate items in the cart