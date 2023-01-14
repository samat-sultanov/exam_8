from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import get_object_or_404

from webapp.forms import ReviewUserForm, ReviewModeratorForm
from webapp.models import Product, Review


class ReviewCreateView(LoginRequiredMixin, CreateView):
    form_class = ReviewUserForm
    template_name = "reviews/create.html"

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        author = self.request.user
        form.instance.author = author
        form.instance.product = product
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.object.product.pk})


class ReviewUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = ReviewUserForm
    template_name = "reviews/update.html"
    permission_required = "webapp.change_review"
    model = Review

    def get_form_class(self):
        if self.request.user.has_perm("webapp.change_review"):
            return ReviewModeratorForm
        return ReviewUserForm

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.object.product.pk})


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "webapp.change_review"
    model = Review

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.object.product.pk})


class NotModeratedReview(PermissionRequiredMixin, ListView):
    queryset = Review.objects.filter(is_moderated=False)
    context_object_name = "reviews"
    template_name = "reviews/not_moderated.html"
    ordering = ['-updated_at']
    permission_required = "webapp.review_not_moderated"
