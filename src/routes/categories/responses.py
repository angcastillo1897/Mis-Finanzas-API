from src.entities.category.serializer import CategorySerializer
from src.entities import SerializerModel


class CategoryResponse(SerializerModel):
    data: CategorySerializer


class CategoryListResponse(SerializerModel):
    data: list[CategorySerializer]
