import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="Pwd1234567A")


@pytest.fixture
def auth_client(client, user):
    client.login(username="alice", password="Pwd1234567A")
    return client


@pytest.mark.django_db
def test_labels_require_login(client):
    resp = client.get(reverse("labels_index"))
    assert resp.status_code in (301, 302)


@pytest.mark.django_db
def test_create_update_delete_label(auth_client):
    r = auth_client.post(reverse("labels_create"), {"name": "bug"})
    assert r.status_code == 302
    lbl = Label.objects.get(name="bug")
    r = auth_client.post(
        reverse("labels_update", args=[lbl.pk]),
        {"name": "feature"},
    )
    assert r.status_code == 302
    lbl.refresh_from_db()
    assert lbl.name == "feature"
    r = auth_client.post(reverse("labels_delete", args=[lbl.pk]))
    assert r.status_code == 302
    assert not Label.objects.filter(pk=lbl.pk).exists()


@pytest.mark.django_db
def test_cannot_delete_label_in_use(auth_client):
    st = Status.objects.create(name="new")
    u = User.objects.get(username="alice")
    t = User.objects.create_user(username="exec", password="Xx1234567890")
    lbl = Label.objects.create(name="in-use")
    task = Task.objects.create(
        name="T",
        description="",
        status=st,
        author=u,
        executor=t,
    )
    task.labels.add(lbl)

    r = auth_client.post(reverse("labels_delete", args=[lbl.pk]))
    assert r.status_code == 302
    assert Label.objects.filter(pk=lbl.pk).exists()
