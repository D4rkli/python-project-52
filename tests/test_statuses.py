import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="Pwd1234567A")


@pytest.fixture
def auth_client(client, user):
    client.login(username="alice", password="Pwd1234567A")
    return client


@pytest.mark.django_db
def test_statuses_require_login(client):
    resp = client.get(reverse("statuses_index"))
    assert resp.status_code in (302, 301)
    assert "/login/" in resp.url


@pytest.mark.django_db
def test_create_status(auth_client):
    resp = auth_client.post(reverse("statuses_create"), {"name": "new"})
    assert resp.status_code == 302
    assert Status.objects.filter(name="new").exists()


@pytest.mark.django_db
def test_update_status(auth_client):
    s = Status.objects.create(name="old")
    resp = auth_client.post(
        reverse("statuses_update", args=[s.pk]),
        {"name": "updated"},
    )
    assert resp.status_code == 302
    s.refresh_from_db()
    assert s.name == "updated"


@pytest.mark.django_db
def test_delete_status(auth_client):
    s = Status.objects.create(name="temp")
    resp = auth_client.post(reverse("statuses_delete", args=[s.pk]))
    assert resp.status_code == 302
    assert not Status.objects.filter(pk=s.pk).exists()
