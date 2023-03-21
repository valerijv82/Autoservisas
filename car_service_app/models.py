from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField


class CarModel(models.Model):
    marke = models.CharField("Marke", max_length=100)
    model = models.CharField("Modelis", max_length=100)

    class Meta:
        db_table = 'car_model'
        verbose_name = 'Car model'
        verbose_name_plural = 'car model'
        ordering = ['marke', 'model']

    def __str__(self):
        return f'{self.marke} : {self.model}'


class Car(models.Model):
    cover = models.ImageField('Virselis', upload_to='covers', null=True, blank=True)
    valstybinis_nr = models.CharField("Valstybinis numeris", max_length=12)
    car_model_id = models.ForeignKey("CarModel", on_delete=models.SET_NULL, null=True)
    vin_code = models.CharField('VIN', max_length=20)
    customer = models.CharField("Klientas", max_length=100)
    description = HTMLField('Aprasymas', default='')

    class Meta:
        db_table = 'car'
        verbose_name = 'Car object'
        verbose_name_plural = 'car object'
        ordering = ['customer', 'vin_code', 'customer']

    def __str__(self):
        return f'{self.customer}'


class Order(models.Model):
    data = models.DateTimeField("Data", null=True, blank=True)
    car_id = models.ForeignKey("Car", on_delete=models.SET_NULL, null=True)
    suma = models.CharField("Suma", max_length=10)
    useris = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)

    SERVISAI = (
        ('p', 'Patvirtintas'),
        ('v', 'Vykdoma'),
        ('a', 'Atlikta'),
        ('t', 'Atsaukta')
    )
    servis = models.CharField("Serviso pavadinimas", choices=SERVISAI, blank=True, default='p', max_length=50)

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'order'
        ordering = ['data', 'suma']

    def __str__(self):
        return f'Order: {self.car_id} - {self.data} - suma: {self.suma}'

    @property
    def is_overdue(self):
        # return self.due_back is not None and self.due_back < datetime.today().replace(tzinfo=pytz.utc)
        return self.data is not None and self.data < timezone.now()

    @property
    def is_viso(self):
        is_viso = 0
        orders = OrderLine.objects.filter(order_id=self.id)
        for line in orders:
            is_viso += float(line.price) * float(line.quantity)
        return is_viso


class OrderLine(models.Model):
    service_id = models.ForeignKey("Service", on_delete=models.SET_NULL, null=True)
    order_id = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True)
    quantity = models.CharField("Kiekis", max_length=10)
    price = models.CharField("Kaina", max_length=10)

    class Meta:
        db_table = 'order_line'
        verbose_name = 'Order line'
        verbose_name_plural = 'order line'
        ordering = ['quantity', 'price']

    def __str__(self):
        return 'Order Line'


class Service(models.Model):
    SERVICES = (
        ('p', 'patikra'),
        ('a', 'alyva'),
        ('s', 'sankaba'),
    )
    name = models.CharField("Paslaugos pavadinimas", choices=SERVICES, blank=True, default='p', max_length=5)
    price = models.CharField("Paslaugos kaina", max_length=10)

    class Meta:
        db_table = 'service'
        verbose_name = 'Service'
        verbose_name_plural = 'service'
        ordering = ['name', 'price']

    def __str__(self):
        return f'{self.name}'


class OrderReview(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comment's"
        ordering = ['-date_created']