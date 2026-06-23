from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Ürün Adı")
    slug = models.SlugField(max_length=200, unique=True)
    image_url = models.URLField(max_length=1000, blank=True, verbose_name="Tedarikçi Resim URL")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Satış Fiyatı")
    available = models.BooleanField(default=True, verbose_name="Satışta mı?")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Ürünler"

    def __str__(self):
        return self.name

class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Ad")
    last_name = models.CharField(max_length=50, verbose_name="Soyad")
    email = models.EmailField(verbose_name="E-posta")
    address = models.TextField(verbose_name="Açık Adres")
    postal_code = models.CharField(max_length=20, verbose_name="Posta Kodu")
    city = models.CharField(max_length=100, verbose_name="Şehir")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name="Ödendi mi?")
    shopier_order_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Shopier No")

    class Meta:
        verbose_name_plural = "Siparişler"
        ordering = ['-created']

    def __str__(self):
        return f"Sipariş #{self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity