from task_tracker import add_task, remove_task, search_tasks, tasks

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
