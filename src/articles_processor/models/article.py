from pydantic import BaseModel, Field


class ArticleMetadata(BaseModel):
    """Модель для валидации метаданных научной статьи перед обработкой."""

    title: str = Field(min_length=1, max_length=500, description="Title of the article")
    scopus_eid: str = Field(default="unknown", description="Scopus EID identifier")
    abstract: str | None = Field(default=None, max_length=5000)
    keywords: list[str] = Field(default_factory=list, description="List of article keywords")

    model_config = {"extra": "ignore"}
