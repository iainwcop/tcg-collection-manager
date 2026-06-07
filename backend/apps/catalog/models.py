from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CardSet(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="sets")
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    release_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-release_date", "name"]
        unique_together = [("game", "code")]

    def __str__(self):
        return f"{self.name} ({self.code})"


class CardDefinition(models.Model):
    set = models.ForeignKey(CardSet, on_delete=models.CASCADE, related_name="cards")
    name = models.CharField(max_length=200)
    collector_number = models.CharField(max_length=20)
    rarity = models.CharField(max_length=50, blank=True)
    image_url = models.URLField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["set", "collector_number"]
        unique_together = [("set", "collector_number")]

    def __str__(self):
        return f"{self.name} ({self.set.code} #{self.collector_number})"
