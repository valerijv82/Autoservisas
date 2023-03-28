from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField

from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    name = models.CharField(_('Name'), max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Name')
        verbose_name_plural = _("Name's")


class CarModel(models.Model):
    marke = models.CharField(_("Brand"), max_length=100)
    model = models.CharField(_("Model"), max_length=100)

    class Meta:
        db_table = 'car_model'
        verbose_name = _('Car model')
        verbose_name_plural = _('car model')
        ordering = ['marke', 'model']

    def __str__(self):
        return f'{self.marke} : {self.model}'


class Car(models.Model):
    cover = models.ImageField(_('Cover'), upload_to='covers', default='no_car.png', null=True, blank=True)
    valstybinis_nr = models.CharField(_("License plate"), max_length=12)
    car_model_id = models.ForeignKey("CarModel", on_delete=models.SET_NULL, null=True)
    vin_code = models.CharField(_('VIN code'), max_length=20)
    customer = models.CharField(_("Client"), max_length=100)
    description = HTMLField(_('Description'), default='')

    class Meta:
        db_table = 'car'
        verbose_name = _('Car object')
        verbose_name_plural = _("Car object's")
        ordering = ['customer', 'vin_code', 'customer']

    def __str__(self):
        return f'{self.customer}'


class ServicePrice(models.Model):
    service_id = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    car_ids = models.ManyToManyField(CarModel)
    price = models.FloatField(_("Price"))

    def __str__(self):
        return f"{self.service_id}: {self.price}"

    def automobiliai(self):
        return ', '.join(f"{auto.marke} {auto.model}" for auto in self.car_ids.all())

    automobiliai.short_description = _("Car's")

    class Meta:
        verbose_name = _('Service price')
        verbose_name_plural = _('Service price')


class Order(models.Model):
    data = models.DateField(_("Date"), null=True, blank=True)
    car_id = models.ForeignKey("Car", on_delete=models.SET_NULL, null=True)
    useris = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)

    SERVISAI = (
        ('p', _('Confirmed')),
        ('v', _('In progress')),
        ('a', _('Done')),
        ('t', _('Cancelled'))
    )
    servis = models.CharField(_("Service name"), choices=SERVISAI, blank=True, default='p', max_length=50)

    class Meta:
        db_table = 'order'
        verbose_name = _("Order")
        verbose_name_plural = _("Order's")
        ordering = ['data']

    def __str__(self):
        return f'Order: {self.car_id} - {self.data}'

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

    def get_absolute_url(self):
        return reverse('my_order', args=[str(self.id)])


class OrderLine(models.Model):
    service_id = models.ForeignKey("Service", on_delete=models.SET_NULL, null=True)
    order_id = models.ForeignKey("Order", related_name='eilutes', on_delete=models.SET_NULL, null=True)
    quantity = models.CharField(_("Quantity"), max_length=10)
    price = models.CharField(_("Price"), max_length=10)

    class Meta:
        db_table = 'order_line'
        verbose_name = _('Order line')
        verbose_name_plural = _("Order line's")
        ordering = ['quantity', 'price']

    def __str__(self):
        return 'Order Line'

    @property
    def suma(self):
        return float(self.quantity) * float(self.price)

    def is_valid(self):
        pass

    def get_absolute_url(self):
        return reverse('user_add_line_to_order', kwargs={'pk': self.pk})


class OrderReview(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(_('Comment'), max_length=2000)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comment's")
        ordering = ['-date_created']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default='no_image.png', upload_to='profile_pics')

    class Meta:
        verbose_name = _('UserProfile')
        verbose_name_plural = _("UserProfile's")

    def __str__(self):
        return _("%s profile") % self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # print(self.nuotrauka.path)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.nuotrauka.path)
