from django.db.models.deletion import ProtectedError

class UserDeleteView(LoginRequiredMixin, SelfOnlyMixin, DeleteView):
    # ...
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            messages.success(self.request, "User was deleted successfully")
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, "Cannot delete user because it is in use")
            return redirect("users_index")
