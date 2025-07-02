tasks = []


def add_task(task):
    tasks.append(task)
    print(f"Dodano zadanie: {task}")


def remove_task(index):
    if index < len(tasks):
        removed = tasks.pop(index)
        print(f"Usunięto zadanie: {removed}")
    else:
        print("Nie ma zadania o podanym indeksie")


def list_tasks():
    if not tasks:
        print("Brak zadań.")
    else:
        print("Lista zadań:")
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task}")


if __name__ == "__main__":
    while True:
        print("\n1. Dodaj zadanie")
        print("2. Usuń zadanie")
        print("3. Wyświetl zadania")
        print("4. Wyjdź")
        choice = input("Wybierz opcję: ")

        if choice == '1':
            task = input("Podaj treść zadania: ")
            add_task(task)
        elif choice == '2':
            index = int(input("Podaj indeks zadania do usunięcia: ")) - 1
            remove_task(index)
        elif choice == '3':
            list_tasks()
        elif choice == '4':
            break
        else:
            print("Nieprawidłowa opcja")