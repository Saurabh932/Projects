class ToDO:
    def __init__(self):
        print("___Welcome____to___TO-DO___List_____")
        # Creating empty task list
        self.tasks = []

    def add_task(self, task: str):
        """Add a new task"""
        self.tasks.append(task)
        return self.tasks

    def update_task(self, old_task: str, new_task: str):
        """Update an existing task"""
        if old_task in self.tasks:
            index = self.tasks.index(old_task)
            self.tasks[index] = new_task
        return self.tasks

    def delete_task(self, task: str):
        """Delete a task"""
        if task in self.tasks:
            self.tasks.remove(task)
        return self.tasks

    def view_tasks(self):
        """Return all tasks"""
        return self.tasks
            

if __name__ == '__main__':          
    todo = ToDO()