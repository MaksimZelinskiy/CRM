from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from datetime import datetime


class Device(models.Model):
    """Модель оборудования"""

    class Meta:
        db_table = "devices"
        verbose_name = "Доступное оборудование"
        verbose_name_plural = "Доступное оборудование"

    manufacturer = models.TextField(verbose_name="Производитель")
    model = models.TextField(verbose_name="Модель")

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

class Customer(models.Model):
    """Конечные пользователи оборудования"""

    class Meta:
        db_table = "customers"
        verbose_name = "Контрагента"
        verbose_name_plural = "Контрагенты"

    customer_name = models.TextField(verbose_name="Наименование организации")
    customer_address = models.TextField(verbose_name="Адрес")
    customer_city = models.TextField(verbose_name="Город")

    def __str__(self):
        return f"{self.customer_name} по адресу {self.customer_address}"

class DeviceInField(models.Model):
    """Оборудование в полях"""

    class Meta:
        db_table = "devices_in_fields"
        verbose_name = "Оборудование в полях"
        verbose_name_plural = "Оборудование в полях"

    serial_number = models.TextField(verbose_name="Серийный номер")
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Идентификатор контрагента")
    analyzer = models.ForeignKey(Device, on_delete=models.RESTRICT, verbose_name="Идентификатор оборудования")
    owner_status = models.TextField(verbose_name="Статус принадлежности")

    def __str__(self):
        return f"{self.analyzer} с/н {self.serial_number} в {self.customer}"

def status_validator(order_status):
    if order_status not in ["open", "closed", "in progress", "need info"]:
        raise ValidationError(
            gettext_lazy('%(order_status)s is wrong order status'),
            params={'order_status': order_status}
        )


class Order(models.Model):
    """Класс для описания заявки"""

    class Meta:
        db_table = "orders"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"



    device = models.ForeignKey(DeviceInField, verbose_name="Оборудование", on_delete=models.RESTRICT)
    order_description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    last_updated_at = models.DateTimeField(verbose_name="Последние изменение", blank=True, null=True)
    order_status = models.TextField(verbose_name="Статус заявки", validators=[status_validator])

    def __str__(self):
        return f"Заявка №{self.id} для {self.device}"

    def save(self, *args, **kwargs):
        self.last_updated_at = datetime.now()
        super().save(*args, **kwargs)
