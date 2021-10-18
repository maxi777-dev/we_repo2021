from haystack import indexes
from sitio.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='title')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Queremos que se indexen todas las noticias que tengan archivada=False"""
        return self.get_model().objects.filter(state=0)