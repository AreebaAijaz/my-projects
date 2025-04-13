import click
import json
import os

TODO_FILE = "todo.json"

def load_tasks():
    if not os.path.exists(TODO_FILE):  # If file doesn't exist, return an empty list
        return []
    
    with open(TODO_FILE, "r") as file:
        return json.load(file)

def save_tasks(task):
    with open(TODO_FILE, "w") as file:
        json.dump(task, file, indent=4)

@click.group()
def cli():
    """A simple CLI for managing your todo tasks."""
    pass

@click.command()
@click.argument("task")
def add(task):
    """Add a new task to the todo list."""
    tasks = load_tasks()
    tasks.append({"task": task , "done": False})
    save_tasks(tasks)
    click.echo(f"Task '{task}' successfully added to the todo list.")
    
@click.command()
def list():
    """"List all the tasks in the todo list."""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks to display.")
        return
    
    for index,task in enumerate(tasks, 1):
        status = "done" if task["done"] else "not done" 
        click.echo(f"{index}. {task['task']} - {status}")

@click.command()  # Define a command called 'complete'
@click.argument("task_number", type=int)  # Accepts a task number as an integer
def complete(task_number):
    """Mark a task as completed"""
    tasks = load_tasks()  # Load existing tasks
    if 0 < task_number <= len(tasks):  # Ensure task number is valid
        tasks[task_number - 1]["done"] = True  # Mark as done
        save_tasks(tasks)  # Save updated tasks
        click.echo(f"Task {task_number} marked as completed!")  # Print success message
    else:
        click.echo("Invalid task number.")  # Handle invalid numbers


@click.command()  # Define a command called 'remove'
@click.argument("task_number", type=int)  # Accepts a task number as an integer
def remove(task_number):
    """Remove a task from the list"""
    tasks = load_tasks()  # Load existing tasks
    if 0 < task_number <= len(tasks):  # Ensure task number is valid
        removed_task = tasks.pop(task_number - 1)  # Remove the task
        save_tasks(tasks)  # Save updated tasks
        click.echo(f"Removed task: {removed_task['task']}")  # Print removed task
    else:
        click.echo("Invalid task number.")  # Handle invalid numbers



cli.add_command(add)
cli.add_command(list)
cli.add_command(complete)
cli.add_command(remove)
if __name__ == "__main__":
    cli()

