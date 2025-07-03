import pytest
from task_tracker import edit_task

def test_edit_task():
    tasks = ["Kupić mleko", "Napisać raport"]
    edit_task(tasks, 0, "Kupić mleko i chleb")
    assert tasks == ["Kupić mleko i chleb", "Napisać raport"]

def test_edit_invalid_index():
    tasks = ["Zadanie testowe"]
    with pytest.raises(IndexError):
        edit_task(tasks, 2, "Nowa treść")  # Niedozwolony indeks

def test_edit_empty_content():
    tasks = ["Zadanie testowe"]
    with pytest.raises(ValueError):
        edit_task(tasks, 0, "   ")  # Pusta treść
