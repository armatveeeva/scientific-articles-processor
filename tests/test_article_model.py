import pytest
from pydantic import ValidationError

from articles_processor.models.article import ArticleMetadata


def test_article_metadata_valid():
    article = ArticleMetadata(title="Test Article", scopus_eid="2-s2.0-123")
    assert article.title == "Test Article"
    assert article.keywords == []


def test_article_metadata_empty_title():
    with pytest.raises(ValidationError):
        ArticleMetadata(title="")
