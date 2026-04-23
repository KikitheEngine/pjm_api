from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pjm_datalayer import *

app = FastAPI()

# --- ROOT (serve UI) ---
import os
from fastapi.responses import HTMLResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/", response_class=HTMLResponse)
def serve_index():
    path = os.path.join(BASE_DIR, "frontend", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# --- GET ---

@app.get("/users")
def get_user_endpoint():
    rows = get_user()
    return [{"user_id": r[0], "user_name": r[1], "user_email": r[2]} for r in rows]


@app.get("/projects")
def get_projects_endpoint(user_id: int | None = None):
    rows = get_project(user_id)
    return [
        {
            "project_id": r[0],
            "project_name": r[1],
            "project_type": r[2],
            "project_segment": r[3],
            "project_supplier": r[4],
            "project_value": r[5],
            "project_priority": r[6],
            "project_create_date": str(r[7]),
            "project_due_date": str(r[8]),
            "user_id": r[9],
        }
        for r in rows
    ]


@app.get("/actions")
def get_action_endpoint(project_id: int | None = None):
    rows = get_action(project_id)
    return [
        {
            "action_id": r[0],
            "action_name": r[1],
            "action_priority": r[2],
            "action_due_date": str(r[3]),
            "action_create_date": str(r[4]),
            "action_description": r[5],
            "project_id": r[6],
        }
        for r in rows
    ]


@app.get("/subactions")
def get_subaction_endpoint(action_id: int | None = None):
    rows = get_subaction(action_id)
    return [
        {
            "subaction_id": r[0],
            "subaction_name": r[1],
            "subaction_description": r[2],
            "subaction_create_date": str(r[3]),
            "subaction_due_date": str(r[4]),
            "subaction_priority": r[5],
            "action_id": r[6],
        }
        for r in rows
    ]


# --- CREATE ---

@app.post("/users")
def create_user_endpoint(name: str, email: str):
    return {"user_id": create_user(name, email)}


@app.post("/projects")
def create_project_endpoint(name: str, type: str, segment: str, supplier: str, value: int, priority: str, due: str, user: int):
    return {"project_id": create_project(name, type, segment, supplier, value, priority, due, user)}


@app.post("/actions")
def create_action_endpoint(name: str, priority: str, due: str, description: str, project: int):
    return {"action_id": create_action(name, priority, due, description, project)}


@app.post("/subactions")
def create_subaction_endpoint(name: str, description: str, due: str, priority: str, action: int):
    return {"subaction_id": create_subaction(name, description, due, priority, action)}


# --- UPDATE ---

@app.put("/projects/{project_id}")
def update_project_endpoint(project_id: int, name: str, type: str, segment: str, supplier: str, value: int, priority: str, due: str):
    return {"rows_updated": update_project(project_id, name, type, segment, supplier, value, priority, due)}


@app.put("/actions/{action_id}")
def update_action_endpoint(action_id: int, name: str, priority: str, due: str, description: str):
    return {"rows_updated": update_action(action_id, name, priority, due, description)}


@app.put("/subactions/{subaction_id}")
def update_subaction_endpoint(subaction_id: int, name: str, description: str, due: str, priority: str):
    return {"rows_updated": update_subaction(subaction_id, name, description, due, priority)}


# --- DELETE ---

@app.delete("/projects/{project_id}")
def delete_project_endpoint(project_id: int):
    return {"rows_deleted": delete_project(project_id)}


@app.delete("/actions/{action_id}")
def delete_action_endpoint(action_id: int):
    return {"rows_deleted": delete_action(action_id)}


@app.delete("/subactions/{subaction_id}")
def delete_subaction_endpoint(subaction_id: int):
    return {"rows_deleted": delete_subaction(subaction_id)}


#COMPLETE

@app.put("/actions/complete/{action_id}")
def complete_action_endpoint(action_id: int):
    return {"updated": complete_action(action_id)}


@app.put("/subactions/complete/{subaction_id}")
def complete_subaction_endpoint(subaction_id: int):
    return {"updated": complete_subaction(subaction_id)}


# --- STATIC FILES (optional, for future css/js) ---

app.mount("/static", StaticFiles(directory="frontend"), name="static")