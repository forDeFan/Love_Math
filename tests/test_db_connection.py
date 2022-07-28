import sqlite3

import pytest
from pytest_mock import mocker
from src.db_connection import Db_Connection


class Test_Db_Connection:

    @pytest.fixture
    def db_setup(self):
        sqlite3.connect(":memory:")
        db = Db_Connection(":memory:", [
                           "test_cat1", "test_cat2"])
        yield db
        # Teardown
        db.__del__()

    def test_if_result_receieved_from_db(self, db_setup):
        res_cat1 = db_setup.get_result("test_cat1")
        res_cat2 = db_setup.get_result("test_cat2")
        assert res_cat1 == 0
        assert res_cat2 == 0

    def test_if_all_categories_received_from_db(self, db_setup):
        categories = db_setup.get_results()

        assert "test_cat1" in categories[0]
        assert "test_cat2" in categories[1]

    def test_if_category_points_updated(self, db_setup):
        db_setup.get_result("test_cat1")
        db_setup.update_result("test_cat1")
        upd_res1 = db_setup.get_result("test_cat1")
        db_setup.update_result("test_cat1")
        upd_res2 = db_setup.get_result("test_cat1")

        assert upd_res1 == 1
        assert upd_res2 == 2

    def test_if_question_no_received_from_db(self, db_setup):
        qn = db_setup.get_question_no("test_cat1")

        assert qn == 0

    def test_if_question_no_updated_in_db(self, db_setup):
        qn1 = int(db_setup.get_question_no("test_cat1"))
        db_setup.update_question_no("test_cat1")
        qn2 = int(db_setup.get_question_no("test_cat1"))

        assert qn1 == 0
        assert qn2 == 1

    def test_if_percentage_received_from_db(self, db_setup):
        pr = int(db_setup.get_percent("test_cat1"))

        assert pr == 0

    def test_if_percentage_calculated(self, mocker, db_setup):
        """
        2 asked question
        1 correct answer
        Should return 50(%)
        """
        mock_qno = mocker.patch.object(
            Db_Connection, "get_question_no")
        mock_qno.return_value = 2
        mock_gres = mocker.patch.object(
            Db_Connection, "get_result")
        mock_gres.return_value = 1
        db_setup.update_percent("test_cat1")
        per = int(db_setup.get_percent("test_cat1"))

        assert per == 50

    def test_if_percent_returns_minus_one_if_no_question_asked(self, db_setup):
        """
        No question answered should return -1.
        """
        db_setup.update_percent("test_cat1")
        per = int(db_setup.get_percent("test_cat1"))
        
        assert per == -1
