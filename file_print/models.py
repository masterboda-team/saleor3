from django.db import models
from django.db.models import JSONField

from saleor.attribute.models import Attribute, AttributeValue
from saleor.order.models import Order
from saleor.checkout.models import Checkout


class UploadedFile(models.Model):  # models.Model
    """A one UploadedFile can be conected to multiple checkout/order line
    threw UploadedFileLine.
    """
    hash = models.CharField(max_length=32, null=False, db_index=True, unique=True)
    extension = models.CharField(max_length=16)
    name = models.CharField(max_length=127, db_index=True)
    base_url = models.CharField(max_length=127, blank=True)
    page_count = models.IntegerField(null=True)
    colored_pages = JSONField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    description = models.TextField(blank=True)
    text_attribute = models.ForeignKey(
        Attribute,
        related_name="files",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    class Meta:
        ordering = ("pk", "hash", )

    def __str__(self) -> str:
        return self.hash

    def __repr__(self):
        class_ = type(self)
        return "<%s.%s(pk=%r, hash=%s, file_name=%s)>" % (
            class_.__module__,
            class_.__name__,
            self.pk,
            self.hash,
            self.name
        )


class UploadedFileLine(models.Model):
    """A multiple UploadedFileLine are conected to one checkout line
    and after confirm checkout -> to order line.
    """
    hash = models.CharField(max_length=32, null=True, db_index=True)
    name = models.CharField(max_length=127, null=True, db_index=True)
    order = models.ForeignKey(
        Order,
        related_name="file_lines",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column='order_token',
    )
    checkout = models.ForeignKey(
        Checkout,
        related_name="file_lines",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    choosed_colored_pages = JSONField(null=True)
    duplex = models.BooleanField(default=False, null=True, blank=True)
    copies = models.IntegerField(default=1)
    role = models.CharField(max_length=16, default="pdf")
    file = models.ForeignKey(
        UploadedFile,
        related_name="file_lines",
        on_delete=models.CASCADE,
        to_field="hash",
        name="file",
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True, null=True)
    cover_file = models.ForeignKey(
        UploadedFile,
        related_name="cover_lines",
        on_delete=models.CASCADE,
        to_field="hash",
        name="cover",
        blank=True,
        null=True
    )
    pages_per_sheet = models.IntegerField(default=1, null=True)
    #? user_message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("hash", "pk", )

    def __str__(self) -> str:
        return "%d %s" % (self.pk, self.hash)

    def __repr__(self):
        class_ = type(self)
        return "<%s.%s(pk=%r, hash=%s, file_name=%s)>" % (
            class_.__module__,
            class_.__name__,
            self.pk,
            self.hash,
            self.name
        )
