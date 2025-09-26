from django.contrib.auth import get_user_model
from django.views.generic import ListView
User = get_user_model()

class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    ordering = get_user_model().objects.all().order_by("id")

