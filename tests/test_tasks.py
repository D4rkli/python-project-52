import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


@pytest.fixture
def users(db):
    return (
        User.objects.create_user(username="author", password="Pwd1234567A"),
        User.objects.create_user(username="exec", password="Pwd1234567A"),
        User.objects.create_user(username="other", password="Pwd1234567A"),
    )


@pytest.fixture
def status(db):
    return Status.objects.create(name="new")


@pytest.mark.django_db
def test_create_task_requires_login(client):
    assert client.get(reverse("tasks_create")).status_code in (302, 301)


@pytest.mark.django_db
def test_create_task(client, users, status):
    author, execu, _ = users
    client.login(username="author", password="Pwd1234567A")
    resp = client.post(reverse("tasks_create"), {
        "name": "T1",
        "description": "desc",
        "status": status.pk,
        "executor": execu.pk,
    })
    assert resp.status_code == 302
    t = Task.objects.get(name="T1")
    assert t.author == author


@pytest.mark.django_db
def test_only_author_can_delete(client, users, status):
    author, execu, _ = users
    t = Task.objects.create(
        name="T", description="",
        status=status,
        author=author,
        executor=execu,
    )
    client.login(username="other", password="Pwd1234567A")
    resp = client.post(reverse("tasks_delete", args=[t.pk]))
    assert resp.status_code == 302
    assert Task.objects.filter(pk=t.pk).exists()
