import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_users_list_public(client):
    resp = client.get(reverse("users_index"))
    assert resp.status_code == 200
    assert b"Users" in resp.content


@pytest.mark.django_db
def test_register_redirects_to_login(client):
    resp = client.post(reverse("users_create"), {
        "username": "neo",
        "password1": "SuperStrongPass123",
        "password2": "SuperStrongPass123",
    })
    assert resp.status_code == 302
    assert resp.url == reverse("login")
    assert User.objects.filter(username="neo").exists()


@pytest.mark.django_db
def test_login_redirects_home(client, django_user_model):
    django_user_model.objects.create_user(
        username="trinity",
        password="pwd1234567A",
    )
    resp = client.post(
        reverse("login"),
        {"username": "trinity", "password": "pwd1234567A"},
    )
    assert resp.status_code == 302
    assert resp.url == "/"


@pytest.mark.django_db
def test_user_can_update_self(client, django_user_model):
    u = django_user_model.objects.create_user(
        username="morpheus",
        password="Pwd1234567A",
    )
    client.login(
        username="morpheus",
        password="Pwd1234567A",
    )
    resp = client.post(
        reverse("users_update", args=[u.pk]),
        {"username": "morpheus2"},
    )
    assert resp.status_code == 302
    u.refresh_from_db()
    assert u.username == "morpheus2"


@pytest.mark.django_db
def test_user_cannot_update_others(client, django_user_model):
    u1 = django_user_model.objects.create_user(
        username="u1",
        password="pwd1234567A",
    )
    u2 = django_user_model.objects.create_user(
        username="u2",
        password="pwd1234567A",
    )
    client.login(username=u1, password="pwd1234567A")
    resp = client.post(
        reverse("users_update", args=[u2.pk]),
        {"username": "hacker"},
    )
    assert resp.status_code == 302
    u2.refresh_from_db()
    assert u2.username == "u2"
