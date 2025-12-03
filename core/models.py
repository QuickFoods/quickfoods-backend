# core/models.py
from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)  # used by the app
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Deal(models.Model):
    SEGMENT_CHOICES = [
        ("deal", "Deal"),
        ("redeem", "Redeem"),
        ("my", "My Rewards"),
    ]

    CATEGORY_CHOICES = [
        ("all", "All"),
        ("combos", "Combos"),
        ("drinks", "Drinks"),
        ("energy", "Energy"),
        ("snacks", "Snacks"),
        ("bakery", "Bakery"),
        ("candy", "Candy"),
        ("more", "More Deals"),
    ]

    # leave this BLANK in admin = all stores
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="deals",
        null=True,
        blank=True,
    )

    tag = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="deals/",
        blank=True,
        null=True,
    )

    segment = models.CharField(
        max_length=20,
        choices=SEGMENT_CHOICES,
        default="deal",
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="all",
    )

    points_required = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    show_on_home = models.BooleanField(
        default=False,
        help_text="If checked, can appear in Home 'Deals for you'.",
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class FreshItem(models.Model):
    CATEGORY_CHOICES = [
        ("subs", "Subs"),
        ("wraps", "Wraps"),
        ("salads", "Salads"),
        ("soups", "Soups"),
    ]

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="fresh_items",
        null=True,
        blank=True,
        help_text="Leave empty to show in ALL stores.",
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price_label = models.CharField(
        max_length=50,
        help_text='What you want to show like "$7.99" or "From $6.49".',
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="subs",
    )

    image = models.ImageField(
        upload_to="fresh_items/",
        blank=True,
        null=True,
        help_text="Product photo shown in Fresh Food list & detail.",
    )

   
    breads = models.JSONField(default=list, blank=True)
    cheeses = models.JSONField(default=list, blank=True)
    meats = models.JSONField(default=list, blank=True)
    toppings = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
