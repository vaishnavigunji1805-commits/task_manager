from flask import Flask, render_template, request, redirect, url_for

from database.database import create_tables

from services.task_service import (
    add_task,
    get_all_tasks,
    get_task,
    update_task,
    delete_task,
    complete_task
)

app = Flask(__name__)

# Create database tables when the application starts
create_tables()


# =========================
# DASHBOARD
# =========================
@app.route("/")
def dashboard():
    tasks = get_all_tasks()

    total_tasks = len(tasks)

    pending_tasks = sum(
        1 for task in tasks
        if task["status"] == "Pending"
    )

    in_progress_tasks = sum(
        1 for task in tasks
        if task["status"] == "In Progress"
    )

    completed_tasks = sum(
        1 for task in tasks
        if task["status"] == "Completed"
    )

    # Completion percentage
    if total_tasks > 0:
        completion_percentage = round(
            (completed_tasks / total_tasks) * 100
        )
    else:
        completion_percentage = 0

    # Priority counts
    high_priority = sum(
        1 for task in tasks
        if task["priority"] == "High"
    )

    medium_priority = sum(
        1 for task in tasks
        if task["priority"] == "Medium"
    )

    low_priority = sum(
        1 for task in tasks
        if task["priority"] == "Low"
    )

    # Category counts
    work_tasks = sum(
        1 for task in tasks
        if task["category"] == "Work"
    )

    study_tasks = sum(
        1 for task in tasks
        if task["category"] == "Study"
    )

    personal_tasks = sum(
        1 for task in tasks
        if task["category"] == "Personal"
    )

    fitness_tasks = sum(
        1 for task in tasks
        if task["category"] == "Fitness"
    )

    return render_template(
        "dashboard.html",
        tasks=tasks,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        completed_tasks=completed_tasks,
        completion_percentage=completion_percentage,
        high_priority=high_priority,
        medium_priority=medium_priority,
        low_priority=low_priority,
        work_tasks=work_tasks,
        study_tasks=study_tasks,
        personal_tasks=personal_tasks,
        fitness_tasks=fitness_tasks
    )
    tasks = get_all_tasks()

    total_tasks = len(tasks)

    pending_tasks = sum(
        1 for task in tasks
        if task["status"] == "Pending"
    )

    in_progress_tasks = sum(
        1 for task in tasks
        if task["status"] == "In Progress"
    )

    completed_tasks = sum(
        1 for task in tasks
        if task["status"] == "Completed"
    )

    return render_template(
        "dashboard.html",
        tasks=tasks,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        completed_tasks=completed_tasks
    )


# =========================
# VIEW ALL TASKS
# =========================
@app.route("/tasks")
def tasks():
    search = request.args.get("search", "")
    category = request.args.get("category", "")
    priority = request.args.get("priority", "")
    status = request.args.get("status", "")

    all_tasks = get_all_tasks()

    filtered_tasks = []

    for task in all_tasks:

        if search and search.lower() not in task["title"].lower():
            continue

        if category and task["category"] != category:
            continue

        if priority and task["priority"] != priority:
            continue

        if status and task["status"] != status:
            continue

        filtered_tasks.append(task)

    return render_template(
        "tasks.html",
        tasks=filtered_tasks,
        search=search,
        category=category,
        priority=priority,
        status=status
    )


# =========================
# ADD TASK
# =========================
@app.route("/tasks/add", methods=["GET", "POST"])
def add_task_page():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]
        priority = request.form["priority"]
        due_date = request.form["due_date"]

        add_task(
            title,
            description,
            category,
            priority,
            due_date
        )

        return redirect(url_for("tasks"))

    return render_template("add_task.html")


# =========================
# EDIT TASK
# =========================
@app.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):

    task = get_task(task_id)

    if task is None:
        return "Task not found", 404

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]
        priority = request.form["priority"]
        due_date = request.form["due_date"]
        status = request.form["status"]

        update_task(
            task_id,
            title,
            description,
            category,
            priority,
            due_date,
            status
        )

        return redirect(url_for("tasks"))

    return render_template(
        "edit_task.html",
        task=task
    )


# =========================
# DELETE TASK
# =========================
@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task_page(task_id):

    delete_task(task_id)

    return redirect(url_for("tasks"))


# =========================
# COMPLETE TASK
# =========================
@app.route("/tasks/complete/<int:task_id>", methods=["POST"])
def complete_task_page(task_id):

    complete_task(task_id)

    return redirect(url_for("tasks"))


# =========================
# RUN APPLICATION
# =========================
if __name__ == "__main__":
    app.run(debug=True)