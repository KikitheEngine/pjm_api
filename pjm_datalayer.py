import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        r"SERVER=yukiprojectmanagement.database.windows.net;"
        "DATABASE=projectmanagement;"
        "UID=kieranapgar;"
        "PWD=Servantleadership@ABGO1;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )

#entry point testing
if __name__ == "__main__":
    conn = get_connection()
    print("Connected!")
    conn.close()


#GET

def get_user():
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM dbo.users")
    rows = cursor.fetchall()

    conn.close()

    return rows


def get_project(): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dbo.projects")
    rows = cursor.fetchall()

    conn.close()

    return rows


def get_action(): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dbo.actions")

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_subaction(): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dbo.subactions")

    rows = cursor.fetchall()

    conn.close()

    return rows


#CREATE

def create_user(name, email):
    conn = get_connection()
    cursor = conn.cursor() 

    cursor.execute("""INSERT INTO dbo.users (user_name, user_email) OUTPUT INSERTED.user_id values(?, ?) """, (name, email)
    )
    
    row = cursor.fetchone()

    conn.commit()
    conn.close()

    return row[0] if row else None
             
def create_project(name, type, segment, supplier, value, priority, created, due, user): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO dbo.projects (project_name, project_type, project_segment, project_supplier, project_value, 
                   project_priority, project_create_date, project_due_date, user_id) OUTPUT INSERTED.project_id 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """, (name, type, segment, supplier, value, priority, created, due, user)
    )

    row = cursor.fetchone()

    conn.commit()
    conn.close()

    return row[0] if row else None


def create_action(name, priority, due, created, description, project): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO dbo.actions (action_name, action_priority, action_due_date, action_create_date, 
                   action_description, project_id) OUTPUT INSERTED.action_id 
                   VALUES (?, ?, ?, ?, ?, ?)""", (name, priority, due, created, description, project)
    )


    row = cursor.fetchone()

    conn.commit()
    conn.close()

    return row[0] if row else None


def create_subaction(name, description, created, due, priority, action): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO dbo.subactions (subaction_name, subaction_description, subaction_create_date, subaction_due_date,
                   subaction_priority, action_id) OUTPUT INSERTED.subaction_id 
                   VALUES (?, ?, ?, ?, ?, ?)""", (name, description, created, due, priority, action)
    )

    row = cursor.fetchone()

    conn.commit()
    conn.close()

    return row

#UPDATE

def update_project(project_id, name, type, segment, supplier, value, priority, created, due, user): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""UPDATE dbo.projects 
            SET
                project_name = ?, 
                project_type = ?, 
                project_segment = ?, 
                project_supplier = ?, 
                project_value = ?, 
                project_priority = ?, 
                project_create_date = ?, 
                project_due = ?, 
                project_user = ?,
                project_due_date = ?
            WHERE project_id = ?
        """,
        (project_id, name, type, segment, supplier, value, priority, created, due, user)
    )

    conn.commit()
    rows_updated = cursor.rowcount 
    
    conn.close()

    return rows_updated


def update_action(action_id, name, priority, due, created, description): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""UPDATE dbo.actions 
            SET 
                action_name = ?, 
                action_priority = ?, 
                action_due_date = ?, 
                action_create_date = ?,
                action_description = ?
            WHERE action_id = ?
            """, 
            (action_id, name, priority, due, created, description)
    )

    conn.commit()
    rows_updated = cursor.rowcount 

    conn.close() 

    return rows_updated


def update_subaction(subaction_id, name, description, created, due, priority): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""UPDATE dbo.subactions
            SET 
                subaction_name = ?, 
                subaction_description = ?, 
                subaction_create_date = ?,
                subaction_due_date = ?, 
                subaction_priority = ?
            WHERE subaction_id = ? 
        """, (subaction_id, name, description, created, due, priority)
    )

    conn.commit() 
    rows_updated = cursor.rowcount 

    conn.close()

    return rows_updated


#DELETE

def delete_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""DELETE FROM dbo.projects WHERE project_id = ?""", (project_id,)
    )

    rows_deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return rows_deleted

  
def delete_action(action_id): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""DELETE FROM dbo.actions where action_id = ?""", (action_id,)
    )

    rows_deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return rows_deleted

def delete_subaction(subaction_id): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""DELETE FROM dbo.subactions where sub_id = ?""", (subaction_id,)
    )

    rows_deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return rows_deleted

