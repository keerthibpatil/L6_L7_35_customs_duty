
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


# -------------------------
# duty_rate() tests
# -------------------------

def test_books_are_duty_free():
    assert duty_rate("books", "FTA") == 0


def test_electronics_fta():
    assert duty_rate("electronics", "FTA") == 0.10


def test_electronics_non_fta():
    assert duty_rate("electronics", "US") == 0.20


def test_clothing_fta():
    assert duty_rate("clothing", "FTA") == 0.05


def test_clothing_non_fta():
    assert duty_rate("clothing", "US") == 0.12


def test_unknown_category():
    assert duty_rate("furniture", "US") == 0.15


@pytest.mark.parametrize("category", ["weapons", "narcotics"])
def test_prohibited_items_raise_error(category):
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate(category, "US")


# -------------------------
# total_duty() tests
# -------------------------

def test_low_value_personal_import():
    assert total_duty("books", 500, "US", False) == 0


def test_negative_value_raises_error():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("electronics", -1, "US", False)


def test_non_gift_value_exactly_1000():
    assert total_duty("electronics", 1000, "US", False) == 0


def test_non_gift_value_above_1000():
    assert total_duty("electronics", 2000, "FTA", False) == 200


def test_gift_value_exactly_5000():
    assert total_duty("electronics", 5000, "FTA", True) == 0


def test_gift_value_above_5000():
    assert total_duty("electronics", 6000, "FTA", True) == 100



def test_minimum_duty_applies():
    assert total_duty("clothing", 5001, "FTA", True) == 50

def test_duty_exactly_50():
    # 1000 is exempt for non-gifts, so use a gift:
    # (6000 - 5000) * 5% = 50.
    assert total_duty("clothing", 6000, "FTA", True) == 50


def test_duty_above_minimum():
    assert total_duty("electronics", 2000, "FTA", False) == 200


def test_prohibited_item_reached_during_calculation():
    with pytest.raises(ValueError, match="prohibited item"):
        total_duty("weapons", 2000, "US", False)


# -------------------------
# clearance_channel() tests
# -------------------------

@pytest.mark.parametrize("category", ["weapons", "narcotics"])
def test_clearance_refuses_prohibited_items(category):
    assert clearance_channel(100, category, True) == "refuse"


def test_clearance_inspects_value_above_100000():
    assert clearance_channel(100001, "electronics", True) == "inspect"


def test_clearance_value_exactly_100000():
    assert clearance_channel(100000, "electronics", True) == "green"


def test_clearance_inspects_missing_documents():
    assert clearance_channel(25000, "electronics", False) == "inspect"


def test_clearance_value_exactly_20000_without_documents():
    assert clearance_channel(20000, "electronics", False) == "green"


def test_clearance_documents_present():
    assert clearance_channel(25000, "electronics", True) == "green"


def test_clearance_ordinary_value():
    assert clearance_channel(10000, "electronics", False) == "green"
