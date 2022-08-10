from abc import ABC, abstractmethod
from typing import List, Tuple


class Abstract_db(ABC):
    """
    Abstract class for database implementation.
    """

    @abstractmethod
    def __init__(self, db_name: str, categories: List[str]) -> None:
        """
        Initialize DB.

        Args:
            db_name (str): database filename.
            categories (List[str]): from constants - to automatically fill out db columns.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @abstractmethod
    def __del__(self) -> None:
        """
        Remove database at exit from app.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @abstractmethod
    def update_result(self, category_name: str) -> None:
        """
        Update point result for specified category.

        Args:
            category_name (str): specified category.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @abstractmethod
    def get_result(self, category_name: str) -> str:
        """
        Get point result from database for specified category.

        Args:
            category_name (str): specified category.

        Returns:
            str: points for specified category.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @abstractmethod
    def get_results(self) -> List[Tuple[str, str]]:
        """
        Get point result from database for all categories.

        Returns:
            List[Tuple[str, str]]: List of Tuples[category, points]

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @abstractmethod
    def update_question_no(self, category_name: str) -> None:
        """
        Update number of asked questions in database in specified category - for percentage calculation.

        Args:
            category_name (str): specified category.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @abstractmethod
    def get_question_no(self, category_name: str) -> str:
        """
        Get number of asked questions from database in specified category - for percentage calculation.

        Args:
            category_name (str): specified category.

        Returns:
            str: number of asked questions in specified category.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @abstractmethod
    def update_percent(self, category_name: str) -> None:
        """
        Update percenatge of answered questions in database for spefied category.

        Args:
            category_name (str): specified category.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @abstractmethod
    def get_percent(self, category_name: str) -> str:
        """
        Get percentage of properly answered questions from database in spefied category.

        Args:
            category_name (str): specified category.

        Returns:
            str: percentage of correct answers.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError
