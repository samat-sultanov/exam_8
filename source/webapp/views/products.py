from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProductForm
from webapp.models import Product


class IndexView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    paginate_by = 3


class ProductDetailView(DetailView):
    template_name = "products/detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.object.reviews.all()
        if not self.request.user.has_perm("webapp.view_not_moderated_review"):
            reviews = reviews.filter(is_moderated=True)
        context['reviews'] = reviews.order_by("-edited_at")
        return context


class ProductCreateView(CreateView):
    form_class = ProductForm
    template_name = "products/create.html"

    def get_success_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.object.pk})


class ProductUpdateView(UpdateView):
    form_class = ProductForm
    template_name = "products/update.html"
    model = Product
    permission_required = "webapp.change_product"

    def get_success_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/delete.html"
    success_url = reverse_lazy('webapp:index')
    permission_required = "webapp.delete_product"
