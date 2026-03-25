from django.db import models
from inventory_management.models import Inventory


class Asset(models.Model):

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Assigned', 'Assigned'),
        ('Under Repair', 'Under Repair'),
        ('Retired', 'Retired'),
    ]

    asset_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)

    inventory_item = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available'
    )

    def __str__(self):
        return f"{self.asset_id} - {self.name} ({self.brand})"