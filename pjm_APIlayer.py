from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

from pjm_datalayer import ( 
    get_user, 
    get_project, 
    get_action,
    get_subaction,
    create_user, 
    create_project, 
    create_action, 
    create_subaction, 
    update_project, 
    update_action, 
    update_subaction, 
    delete_project, 
    delete_action, 
    delete_subaction
)

#GET

@app.get("/users")
def get_user_endpoint():
    rows = get_user()

    return [
        {
            "user_id": r[0],
            "user_name": r[1],
            "user_email": r[2]
        } for r in rows
    ]

@app.get("/projects")
def get_projects_endpoint(user_id: int = None):
    
    rows = get_project(user_id) if user_id else get_project()

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
            "user_id": r[9]
        } for r in rows
    ]


@app.get("/actions")
def get_action_endpoint(project_id: int):

    rows = get_action(project_id)

    return [
        {
            "action_id": r[0],
            "action_name": r[1],
            "action_priority": r[2],
            "action_due_date": str(r[3]),
            "action_create_date": str(r[4]),
            "action_description": r[5],
            "project_id": r[6]
        } for r in rows
    ]


@app.get("/subactions")
def get_subaction_endpoint(action_id: int):

    rows = get_subaction(action_id)

    return [
        {
            "subaction_id": r[0],
            "subaction_name": r[1],
            "subaction_description": r[2],
            "subaction_create_date": str(r[3]),
            "subaction_due_date": str(r[4]),
            "subaction_priority": r[5],
            "action_id": r[6] 
        }  for r in rows
    ]


#UPDATE

@app.put("/projects/{project_id}")
def update_project_endpoint(project_id: int, name: str, type: str, segment: str, supplier: str, value: int, priority: str, created: str, due: str, user_id: int):
    return update_project(project_id, name, type, segment, supplier, value, priority, created, due, user_id)


@app.put("/actions/{action_id}")
def update_action_endpoint(action_id: int, name: str, priority: str, due: str, created: str, description: str, project_id: int):
    return update_action(action_id, name, priority, due, created, description, project_id)


@app.put("/subactions/{subaction_id}")
def update_subaction_endpoint(subaction_id: int, name: str, description: str, created: str, due: str, priority: str, action_id: int):
    return update_subaction(subaction_id, name, description, created, due, priority, action_id)


#CREATE

@app.post("/users")
def create_user_endpoint(name: str, email: str):
    return create_user(name, email)


@app.post("/projects")
def create_project_endpoint(name: str, type: str, segment: str, supplier: str, value: int, priority: str, created: str, due: str, user_id: int):
    return create_project(name, type, segment, supplier, value, priority, created, due, user_id)


@app.post("/actions")
def create_action_endpoint(name: str, priority: str, due: str, created: str, description: str, project_id: int):
    return create_action(name, priority, due, created, description, project_id)


@app.post("/subactions")
def create_subaction_endpoint(name: str, description: str, created: str, due: str, priority: str, action_id: int):
    return create_subaction(name, description, created, due, priority, action_id)


#DELETE 

@app.delete("/projects/{project_id}")
def delete_project_endpoint(project_id: int):
    return delete_project(project_id)


@app.delete("/actions/{action_id}")
def delete_action_endpoint(action_id: int):
    return delete_action(action_id)


@app.delete("/subactions/{subaction_id}")
def delete_subaction_endpoint(sub_id: int):
    return delete_subaction(sub_id)









