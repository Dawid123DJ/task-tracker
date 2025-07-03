from task_tracker import add_task, remove_task, search_tasks, edit_task, tasks

def test_search_integration():
    # Reset globalnej listy zadań
    tasks.clear()
    
    # Dodaj przykładowe zadania
    add_task("Kupić jajka")
    add_task("Zrobić zakupy")
    add_task("Napisać raport miesięczny")
    
    # Wyszukaj
    results = search_tasks(tasks, "raport miesięczny")
    
    # Asercje
    assert len(results) == 1
    assert "Napisać raport miesięczny" in results

def test_edit_integration():
    # Reset globalnej listy zadań
    tasks.clear()
    
    # Dodaj zadanie
    add_task("Pierwotna treść")
    
    # Edytuj zadanie
    edit_task(tasks, 0, "Zmieniona treść")
    
    # Sprawdź wynik
    assert tasks[0] == "Zmieniona treść"
    assert len(tasks) == 1
