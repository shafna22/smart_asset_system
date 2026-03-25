from django.db import models
from django.conf import settings
from asset_management.models import Asset


class AssetAssignment(models.Model):

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE
    )

    assigned_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.asset.asset_id} -> {self.employee.username}"