from django.db import models

class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def availability(self):
        return "Low Stock" if self.quantity < 10 else "Available"

    def __str__(self):
        return self.item_name      