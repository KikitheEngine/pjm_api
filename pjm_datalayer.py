import psycopg2
import os


def get_connection():
    return psycopg2.connect(
        host="dpg-d7kjaeosfn5c73dg0gb0-a.oregon-postgres.render.com",
        database="projectmanagement_ckmw",
        user="projectmanagement_ckmw_user",
        password="dX9UgUX36rXJFuJG6EUGN25vUjOn0U7A",
        port=5432,
        sslmode="require"
    )


# --- GET ---

def get_user():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


def get_project(user_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    if user_id:
        cursor.execute("SELECT * FROM projects WHERE user_id = %s", (user_id,))
    else:
        cursor.execute("SELECT * FROM projects")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


def get_action(project_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    if project_id:
        cursor.execute("SELECT * FROM actions WHERE project_id = %s", (project_id,))
    else:
        cursor.execute("SELECT * FROM actions")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


def get_subaction(action_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    if action_id:
        cursor.execute("SELECT * FROM subactions WHERE action_id = %s", (action_id,))
    else:
        cursor.execute("SELECT * FROM subactions")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


# --- CREATE ---

def create_user(name, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (user_name, user_email) VALUES (%s, %s) RETURNING user_id",
        (name, email)
    )

    row = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()
    return row[0] if row else None


def create_project(name, type, segment, supplier, value, priority, due, user):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO projects (
            project_name, project_type, project_segment, project_supplier, project_value,
            project_priority, project_due_date, user_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING project_id
    """, (name, type, segment, supplier, value, priority, due, user))

    row = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()
    return row[0] if row else None


def create_action(name, priority, due, description, project, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO actions (
            action_name, action_priority, action_due_date,
            action_description, project_id, action_status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING action_id
    """, (name, priority, due, description, project, status))

    row = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()
    return row[0] if row else None


def create_subaction(name, description, due, priority, action, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subactions (
            subaction_name, subaction_description,
            subaction_due_date, subaction_priority, action_id, subaction_status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING subaction_id
    """, (name, description, due, priority, action))

    row = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()
    return row[0] if row else None


# --- UPDATE ---

def update_project(project_id, name, type, segment, supplier, value, priority, due):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE projects
        SET
            project_name = %s,
            project_type = %s,
            project_segment = %s,
            project_supplier = %s,
            project_value = %s,
            project_priority = %s,
            project_due_date = %s
        WHERE project_id = %s
    """, (name, type, segment, supplier, value, priority, due, project_id))

    conn.commit()
    rows_updated = cursor.rowcount

    cursor.close()
    conn.close()
    return rows_updated


def update_action(action_id, name, priority, due, description, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE actions
        SET
            action_name = %s,
            action_priority = %s,
            action_due_date = %s,
            action_description = %s, 
            action_status = %s
        WHERE action_id = %s
    """, (name, priority, due, description, action_id, status))

    conn.commit()
    rows_updated = cursor.rowcount

    cursor.close()
    conn.close()
    return rows_updated


def update_subaction(subaction_id, name, description, due, priority, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE subactions
        SET
            subaction_name = %s,
            subaction_description = %s,
            subaction_due_date = %s,
            subaction_priority = %s, 
            subaction_status = %s
        WHERE subaction_id = %s
    """, (name, description, due, priority, subaction_id, status))

    conn.commit()
    rows_updated = cursor.rowcount

    cursor.close()
    conn.close()
    return rows_updated


# --- DELETE ---

def delete_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM projects WHERE project_id = %s", (project_id,))
    rows_deleted = cursor.rowcount

    conn.commit()
    cursor.close()
    conn.close()
    return rows_deleted


def delete_action(action_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM actions WHERE action_id = %s", (action_id,))
    rows_deleted = cursor.rowcount

    conn.commit()
    cursor.close()
    conn.close()
    return rows_deleted


def delete_subaction(subaction_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM subactions WHERE subaction_id = %s", (subaction_id,))
    rows_deleted = cursor.rowcount

    conn.commit()
    cursor.close()
    conn.close()
    return rows_deleted


#COMPLETE 

def complete_action(action_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE actions SET action_status = TRUE WHERE action_id = %s",
        (action_id,)
    )
    conn.commit()
    cur.close()
    conn.close()
    return action_id


def complete_subaction(subaction_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE subactions SET subaction_status = TRUE WHERE subaction_id = %s",
        (subaction_id,)
    )
    conn.commit()
    cur.close()
    conn.close()
    return subaction_id


