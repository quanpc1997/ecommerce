from abc import ABC
from typing import Optional, TypeVar

T = TypeVar("T")


class BaseRepository(ABC):
    async def create(self, obj: T):
        """
        Inserts an object into the database.

        Raises RepositoryException of failure.
        """
        raise NotImplementedError

    async def get_by_id(self, obj_id: str) -> Optional[T]:
        """
        Retrieves an object by it's ID and if the movie is not found it will return None.
        """
        raise NotImplementedError

    async def update(self, obj_id: str, update_parameters: dict):
        """
        Update an object by it's id.
        """
        raise NotImplementedError

    async def delete(self, obj_id: str):
        """
        Deletes an object by it's id.

        Raises RepositoryException of failure.
        """
        raise NotImplementedError
