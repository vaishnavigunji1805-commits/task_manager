from database.database import get_connection


def add_task(title, description, category, priority, due_date):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO tasks
        (title, description, category, priority, due_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, description, category, priority, due_date)
    )

    connection.commit()
    connection.close()


def get_all_tasks():
    connection = get_connection()

    tasks = connection.execute(
        """
        SELECT *
        FROM tasks
        ORDER BY created_at DESC
        """
    ).fetchall()

    connection.close()

    return tasks


def get_task(task_id):
    connection = get_connection()

    task = connection.execute(
        """
        SELECT *
        FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    ).fetchone()

    connection.close()

    return task


def update_task(
    task_id,
    title,
    description,
    category,
    priority,
    due_date,
    status
):
    connection = get_connection()

    connection.execute(
        """
        UPDATE tasks
        SET title = ?,
            description = ?,
            category = ?,
            priority = ?,
            due_date = ?,
            status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            title,
            description,
            category,
            priority,
            due_date,
            status,
            task_id
        )
    )

    connection.commit()
    connection.close()


def delete_task(task_id):
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    connection.commit()
    connection.close()


def complete_task(task_id):
    connection = get_connection()

    connection.execute(
        """
        UPDATE tasks
        SET status = 'Completed',
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (task_id,)
    )

    connection.commit()
    connection.close()