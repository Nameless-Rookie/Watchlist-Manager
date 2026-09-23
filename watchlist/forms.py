from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import WatchItem


class RegisterForm(UserCreationForm):
    """Django's secure registration form with friendly field labels."""

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        labels = {"password1": "Password", "password2": "Confirm password"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["autofocus"] = True


class WatchItemForm(forms.ModelForm):
    class Meta:
        model = WatchItem
        fields = ("title", "item_type", "genre", "release_year", "status", "rating", "review")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "For example: Inception"}),
            "release_year": forms.NumberInput(attrs={"min": 1888, "max": date.today().year + 5}),
            "rating": forms.NumberInput(attrs={"min": 0, "max": 10, "step": 0.1, "placeholder": "0–10"}),
            "review": forms.Textarea(attrs={"rows": 5, "placeholder": "Your personal notes or review..."}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_release_year(self):
        year = self.cleaned_data["release_year"]
        if year > date.today().year + 5:
            raise forms.ValidationError("Please enter a reasonable release year.")
        return year

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get("rating")
        status = cleaned_data.get("status")
        if rating is not None and status != WatchItem.Status.WATCHED:
            self.add_error("rating", "A rating can be added after the item is marked as Watched.")

        # The user is not part of the visible form, so check this simple
        # duplicate rule here before the view saves the item.
        title = cleaned_data.get("title")
        item_type = cleaned_data.get("item_type")
        release_year = cleaned_data.get("release_year")
        if self.user and title and item_type and release_year:
            duplicates = WatchItem.objects.filter(
                user=self.user,
                title__iexact=title,
                item_type=item_type,
                release_year=release_year,
            )
            if self.instance.pk:
                duplicates = duplicates.exclude(pk=self.instance.pk)
            if duplicates.exists():
                self.add_error("title", "You already have this title and year in your watchlist.")
        return cleaned_data
