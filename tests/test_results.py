
import pytest
from pytest_mock import mocker
from src.results import Results


class Test_Results:

    @pytest.fixture
    def db_setup(self, mocker):
        db = mocker.patch(
            'src.db_connection.__init__')
        return db

    @pytest.fixture
    def mock_db_get_results(self, mocker, db_setup):
        mock_db_get_results = mocker.patch.object(
            db_setup, "get_results")

        return mock_db_get_results

    @pytest.fixture
    def mock_db_get_percent(self, mocker, db_setup):
        mock_db_get_percent = mocker.patch.object(
            db_setup, "get_percent")

        return mock_db_get_percent

    def test_if_results_returned_with_format(self, mock_db_get_results, db_setup):
        mock_db_get_results.return_value = [
            ("test_cat1", "0", "0", "0"), ("test_cat2", "1", "2", "50")]
        formatted_results = Results.get_results(
            self, db=db_setup)

        assert "test_cat1: n/d" in formatted_results
        assert "test_cat2: 50%" in formatted_results

    def test_if_percentage_returned_formatted(self, mock_db_get_percent, db_setup):
        mock_db_get_percent.return_value = "10"
        formatted_percent = Results.get_percentage(
            self, db=db_setup, category="no_check_as_mock_val")
        assert "10%" in formatted_percent

    def test_if_get_percentage_recognize_not_started_math_task(self, mock_db_get_percent, db_setup):
        mock_db_get_percent.return_value = "0"
        formatted_percent = Results.get_percentage(
            self, db=db_setup, category="no_check_as_mock_val")

        assert "Nie zaczęto" in formatted_percent

    def test_if_result_updated_when_good_answer(self, mocker, db_setup):
        mock = mocker.patch.object(db_setup, "update_result")
        Results.update_result(
            self, db=db_setup, category_name="no_check_as_mock_val", good_answer=True)

        assert mock.call_count == 1

    def test_if_result_not_updated_when_wrong_answer(self, mocker, db_setup):
        mock = mocker.patch.object(db_setup, "update_result")
        Results.update_result(
            self, db=db_setup, category_name="no_check_as_mock_val", good_answer=False)

        assert mock.call_count == 0
