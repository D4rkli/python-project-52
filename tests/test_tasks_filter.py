import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tasks.models import Task

@pytest.fixture
def data(db):
    author = User.objects.create_user(username="author", password="Pwd1234567A")
    exec1  = User.objects.create_user(username="exe1", password="Pwd1234567A")
    exec2  = User.objects.create_user(username="exe2", password="Pwd1234567A")
    st_new = Status.objects.create(name="new")
    st_done = Status.objects.create(name="done")
    l_bug = Label.objects.create(name="bug")
    l_feat = Label.objects.create(name="feature")
    t1 = Task.objects.create(name="T1", description="", status=st_new,  author=author, executor=exec1)
    t2 = Task.objects.create(name="T2", description="", status=st_done, author=author, executor=exec2)
    t1.labels.add(l_bug)
    t2.labels.add(l_feat)
    return locals()

@pytest.mark.django_db
def test_filter_by_status(client, data):
    client.login(username="author", password="Pwd1234567A")
    url = reverse("tasks_index") + f"?status={data['st_new'].pk}"
    resp = client.get(url)
    assert b"T1" in resp.content and b"T2" not in resp.content

@pytest.mark.django_db
def test_filter_by_executor(client, data):
    client.login(username="author", password="Pwd1234567A")
    url = reverse("tasks_index") + f"?executor={data['exec2'].pk}"
    resp = client.get(url)
    assert b"T2" in resp.content and b"T1" not in resp.content

@pytest.mark.django_db
def test_filter_by_label(client, data):
    client.login(username="author", password="Pwd1234567A")
    url = reverse("tasks_index") + f"?label={data['l_bug'].pk}"
    resp = client.get(url)
    assert b"T1" in resp.content and b"T2" not in resp.content

@pytest.mark.django_db
def test_filter_self_tasks(client, data):
    other = User.objects.create_user(username="other", password="Pwd1234567A")
    Task.objects.create(name="T3", description="", status=data['st_new'], author=other, executor=data['exec1'])

    client.login(username="author", password="Pwd1234567A")
    url = reverse("tasks_index") + "?self_tasks=on"
    resp = client.get(url)
    content = resp.content
    assert b"T1" in content and b"T2" in content and b"T3" not in content
