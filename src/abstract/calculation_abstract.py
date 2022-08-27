from abc import ABC, ABCMeta, abstractmethod
from kivy.uix.screenmanager import Screen


class Calculation_Abstract_Meta(ABCMeta, type(Screen)):
    """
    Meta class that combine ABC and the Screen meta class.
    Workaround to avoid: 
        TypeError: metaclass conflict
    """
    pass


class Calculation_Abstract(ABC, metaclass=Calculation_Abstract_Meta):
    """
    Abstract class for calculation screens.
    """

    @abstractmethod
    def generate_num(self, nums_range):
        """
        Generate number/s for UI used in kv file.

        Args:
            nums_range:
                range for randint to generate number/s.
        """
        pass

    @abstractmethod
    def set_num(self, ids_to_set, generated_nums=None) -> None:
        """
        Set number/s in UI (kv file).

        This function used only when correct answer given or at first app run to populate numbers if UI fields empty.
        If leaving screen or wrong answer - numbers stay unchanged until task completed succesfullfy by user.

        Args:
            ids_to_set: 
                id's from kv screen - from which numbers are taken/ or set if empty.

            genearated_nums:
                Numbers are generated at first app start or when good answer.
                If generated_nums != None: values will be inserted in UI (kv file).
                Defaults to None.
        """
        pass

    @abstractmethod
    def show_result(self, num_ids, nums_range) -> bool:
        """
        Notify user in UI (kv) about right/ wrong result.
        If correct answer arrange new task in UI.

        Args:
            num_ids: numbers taken from id's fields in kv file.
            nums_range: range used by randint for number/s generation.

        Returns:
            bool:
                True if correct answer,
                False if wrong answer.
        """
        pass
