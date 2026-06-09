from haystack import indexes

from .models import News


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr="title")
    content = indexes.CharField(model_attr="content")
    published_at = indexes.DateTimeField(model_attr="published_at")

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
