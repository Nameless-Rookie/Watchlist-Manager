from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, WatchItemForm
from .models import WatchItem


def home(request):
    return render(request, "watchlist/home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created. Welcome to Watchlist Manager!")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def logout_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


@login_required
def dashboard(request):
    items = WatchItem.objects.filter(user=request.user)
    counts = {
        "total": items.count(),
        "want": items.filter(status=WatchItem.Status.WANT_TO_WATCH).count(),
        "watching": items.filter(status=WatchItem.Status.WATCHING).count(),
        "watched": items.filter(status=WatchItem.Status.WATCHED).count(),
    }
    average_rating = items.filter(rating__isnull=False).aggregate(Avg("rating"))["rating__avg"]
    return render(
        request,
        "watchlist/dashboard.html",
        {"counts": counts, "average_rating": average_rating, "recent_items": items[:6]},
    )


@login_required
def watchlist(request):
    items = WatchItem.objects.filter(user=request.user)
    query = request.GET.get("q", "").strip()
    selected_type = request.GET.get("type", "")
    selected_genre = request.GET.get("genre", "")
    selected_status = request.GET.get("status", "")
    selected_sort = request.GET.get("sort", "recent")

    if query:
        items = items.filter(Q(title__icontains=query) | Q(review__icontains=query))
    if selected_type in dict(WatchItem.ItemType.choices):
        items = items.filter(item_type=selected_type)
    if selected_genre in dict(WatchItem.Genre.choices):
        items = items.filter(genre=selected_genre)
    if selected_status in dict(WatchItem.Status.choices):
        items = items.filter(status=selected_status)

    sort_options = {
        "recent": ("-created_at",),
        "title": ("title",),
        "rating": ("-rating", "title"),
    }
    items = items.order_by(*sort_options.get(selected_sort, sort_options["recent"]))
    return render(
        request,
        "watchlist/watchlist.html",
        {
            "items": items,
            "query": query,
            "selected_type": selected_type,
            "selected_genre": selected_genre,
            "selected_status": selected_status,
            "selected_sort": selected_sort,
            "type_choices": WatchItem.ItemType.choices,
            "genre_choices": WatchItem.Genre.choices,
            "status_choices": WatchItem.Status.choices,
        },
    )


@login_required
def item_create(request):
    if request.method == "POST":
        form = WatchItemForm(request.POST, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, f'“{item.title}” was added to your watchlist.')
            return redirect("item_detail", pk=item.pk)
    else:
        form = WatchItemForm(user=request.user)
    return render(request, "watchlist/item_form.html", {"form": form, "page_title": "Add to watchlist", "submit_label": "Add item"})


@login_required
def item_detail(request, pk):
    item = get_object_or_404(WatchItem, pk=pk, user=request.user)
    return render(request, "watchlist/item_detail.html", {"item": item})


@login_required
def item_update(request, pk):
    item = get_object_or_404(WatchItem, pk=pk, user=request.user)
    if request.method == "POST":
        form = WatchItemForm(request.POST, instance=item, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'“{item.title}” was updated.')
            return redirect("item_detail", pk=item.pk)
    else:
        form = WatchItemForm(instance=item, user=request.user)
    return render(request, "watchlist/item_form.html", {"form": form, "page_title": "Edit item", "submit_label": "Save changes", "item": item})


@login_required
def item_delete(request, pk):
    item = get_object_or_404(WatchItem, pk=pk, user=request.user)
    if request.method == "POST":
        title = item.title
        item.delete()
        messages.success(request, f'“{title}” was deleted from your watchlist.')
        return redirect("watchlist")
    return render(request, "watchlist/item_confirm_delete.html", {"item": item})
