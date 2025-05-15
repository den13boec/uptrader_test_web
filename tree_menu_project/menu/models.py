from django.db import models
from django.urls import reverse

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='children'
    )
    menu_name = models.CharField(max_length=50)
    named_url = models.CharField(max_length=200, blank=True, null=True)
    explicit_url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slug', 'menu_name'], name='unique_slug_per_menu')
        ]

    def __str__(self):
        return self.name

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except:
                return '#'
        elif self.explicit_url:
            return self.explicit_url
        return '#'
