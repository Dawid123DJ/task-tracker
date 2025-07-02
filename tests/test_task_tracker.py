import unittest
from task_tracker import add_task, remove_task, tasks as global_tasks

class TestTaskTracker(unittest.TestCase):
    def setUp(self):
        # Resetuj listę zadań przed każdym testem
        global_tasks.clear()
    
    def test_add_task(self):
        add_task('Test task')
        self.assertEqual(global_tasks, ['Test task'])
    
    def test_remove_task(self):
        global_tasks.append('Task 1')
        global_tasks.append('Task 2')
        remove_task(0)
        self.assertEqual(global_tasks, ['Task 2'])

if __name__ == '__main__':
    unittest.main()