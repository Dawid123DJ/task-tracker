import pytest
from task_tracker import search_tasks

def test_search_single_keyword():
    """
    Test wyszukiwania pojedynczego słowa kluczowego
    """
    tasks = ["Kupić mleko", "Napisać raport", "Spotkanie z zespołem"]
    results = search_tasks(tasks, "raport")
    assert results == ["Napisać raport"]

def test_search_multiple_keywords():
    """
    Test wyszukiwania wieloma słowami kluczowymi (AND)
    """
    tasks = ["Kupić mleko", "Napisać raport", "Spotkanie z zespołem"]
    results = search_tasks(tasks, "spotkanie zespołem")
    assert results == ["Spotkanie z zespołem"]

def test_search_case_insensitive():
    """
    Test niezależności od wielkości liter
    """
    tasks = ["Kupić mleko", "Napisać raport", "Spotkanie z zespołem"]
    results = search_tasks(tasks, "RAPORT")
    assert results == ["Napisać raport"]

def test_search_no_results():
    """
    Test braku wyników
    """
    tasks = ["Kupić mleko", "Napisać raport"]
    results = search_tasks(tasks, "spotkanie")
    assert results == []