from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class WatchItem(models.Model):
    """One movie or TV show saved by one user."""

    class ItemType(models.TextChoices):
        MOVIE = "movie", "Movie"
        TV_SHOW = "tv", "TV Show"

    class Status(models.TextChoices):
        WANT_TO_WATCH = "want", "Want to Watch"
        WATCHING = "watching", "Watching"
        WATCHED = "watched", "Watched"

    class Genre(models.TextChoices):
        ACTION = "Action", "Action"
        COMEDY = "Comedy", "Comedy"
        DOCUMENTARY = "Documentary", "Documentary"
        DRAMA = "Drama", "Drama"
        HORROR = "Horror", "Horror"
        ROMANCE = "Romance", "Romance"
        SCI_FI = "Sci-Fi", "Sci-Fi"
        THRILLER = "Thriller", "Thriller"
        OTHER = "Other", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watch_items",
    )
    title = models.CharField(max_length=150)
    item_type = models.CharField(max_length=10, choices=ItemType.choices)
    genre = models.CharField(max_length=30, choices=Genre.choices)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.WANT_TO_WATCH,
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Optional. Give a rating from 0 to 10 after watching.",
    )
    review = models.TextField(blank=True, max_length=1000, verbose_name="Review / notes")
    release_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1888), MaxValueValidator(2100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "title", "item_type", "release_year"],
                name="unique_watch_item_per_user",
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.get_item_type_display()})"
