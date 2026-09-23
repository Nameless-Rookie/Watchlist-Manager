from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import WatchItem


class WatchlistSecurityTests(TestCase):
    """Small tests for the most important login and ownership rules."""

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="safe-password-123")
        self.other_user = User.objects.create_user(username="other", password="safe-password-123")
        self.item = WatchItem.objects.create(
            user=self.owner,
            title="Arrival",
            item_type=WatchItem.ItemType.MOVIE,
            genre=WatchItem.Genre.SCI_FI,
            status=WatchItem.Status.WATCHED,
            rating=8.5,
            release_year=2016,
        )

    def test_protected_page_redirects_anonymous_users_to_login(self):
        response = self.client.get(reverse("watchlist"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('watchlist')}")

    def test_public_pages_and_templates_load(self):
        for url in (reverse("home"), reverse("login"), reverse("register")):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_user_cannot_open_another_users_item(self):
        self.client.login(username="other", password="safe-password-123")
        for view_name in ("item_detail", "item_update", "item_delete"):
            with self.subTest(view_name=view_name):
                response = self.client.get(reverse(view_name, args=[self.item.pk]))
                self.assertEqual(response.status_code, 404)

    def test_watchlist_only_displays_the_logged_in_users_items(self):
        WatchItem.objects.create(
            user=self.other_user,
            title="Hidden Title",
            item_type=WatchItem.ItemType.TV_SHOW,
            genre=WatchItem.Genre.DRAMA,
            status=WatchItem.Status.WANT_TO_WATCH,
            release_year=2020,
        )
        self.client.login(username="owner", password="safe-password-123")
        response = self.client.get(reverse("watchlist"))
        self.assertContains(response, "Arrival")
        self.assertNotContains(response, "Hidden Title")

    def test_authenticated_user_can_add_a_watched_item_with_rating(self):
        self.client.login(username="owner", password="safe-password-123")
        response = self.client.post(
            reverse("item_create"),
            {
                "title": "The Bear",
                "item_type": WatchItem.ItemType.TV_SHOW,
                "genre": WatchItem.Genre.DRAMA,
                "release_year": 2022,
                "status": WatchItem.Status.WATCHED,
                "rating": "9.0",
                "review": "A sharp, memorable show.",
            },
        )
        item = WatchItem.objects.get(title="The Bear")
        self.assertRedirects(response, reverse("item_detail", args=[item.pk]))
        self.assertEqual(item.user, self.owner)

    def test_all_owned_pages_and_templates_load(self):
        self.client.login(username="owner", password="safe-password-123")
        urls = [
            reverse("dashboard"),
            reverse("watchlist"),
            reverse("item_create"),
            reverse("item_detail", args=[self.item.pk]),
            reverse("item_update", args=[self.item.pk]),
            reverse("item_delete", args=[self.item.pk]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_filtering_and_full_update_delete_flow(self):
        WatchItem.objects.create(
            user=self.owner,
            title="Planet Earth",
            item_type=WatchItem.ItemType.TV_SHOW,
            genre=WatchItem.Genre.DOCUMENTARY,
            status=WatchItem.Status.WANT_TO_WATCH,
            release_year=2006,
        )
        self.client.login(username="owner", password="safe-password-123")
        filtered = self.client.get(reverse("watchlist"), {"status": WatchItem.Status.WATCHED})
        self.assertContains(filtered, "Arrival")
        self.assertNotContains(filtered, "Planet Earth")

        update = self.client.post(
            reverse("item_update", args=[self.item.pk]),
            {
                "title": "Arrival (revisited)",
                "item_type": WatchItem.ItemType.MOVIE,
                "genre": WatchItem.Genre.SCI_FI,
                "release_year": 2016,
                "status": WatchItem.Status.WATCHED,
                "rating": "9.0",
                "review": "Even better on a second watch.",
            },
        )
        self.assertRedirects(update, reverse("item_detail", args=[self.item.pk]))
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "Arrival (revisited)")
        self.assertEqual(str(self.item.rating), "9.0")

        deletion = self.client.post(reverse("item_delete", args=[self.item.pk]))
        self.assertRedirects(deletion, reverse("watchlist"))
        self.assertFalse(WatchItem.objects.filter(pk=self.item.pk).exists())

# Create your tests here.
