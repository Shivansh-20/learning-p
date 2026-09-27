import sys
import json
from datetime import datetime
#welcome feature
if sys.argv[1].strip().lower() == "welcome":
    print("""Welcome, command words for input
-- for adding task -> "add" ,"task detail"
-- for checking tasks -> "list"  as action - > payload accepted ->  "done" and -> "not done"
-- for  printing all tasks -> use only "list"
-- To delete a task - >"delete" "task ID as payload" """)
#initializing action and payload
action = sys.argv[1].strip().lower()
#payload = sys.argv[2]
print(f"Action -> {action}")
payload = " ".join(sys.argv[2:]).strip().lower()
print("Payload is", payload or None)
#initalizing "DATA"
with open("data.txt", "r") as file:
    data = json.load(file)
#initial feature deisgn, ignore
'''
def read_name(data):
    print(data["name"])

def read_age():
    with open("data.txt", "r") as file:
        data = json.load(file)
    print(data["age"])
'''

'''
def change_name(data,new):
    data["name"] = new
    with open("data.txt", "w") as file:
        json.dump(data,file)

'''
#actual function design
def add_task(data,payload):
    if data:
        max_id = max(item['id']for item in data)
        new_id = max_id + 1
    else: new_id = 1
    new_task = {
        "id":new_id,
        "task":payload,
        "created at":datetime.now().isoformat(),
        "status": "not done"
    }
    data.append(new_task)
    with open("data.txt" , "w") as file:
        json.dump(data, file, indent = 4)
#delete func
def delete_tasks(data,payload):
    task_id = int(payload)
    for i, item in enumerate(data):
        if item["id"] == task_id:
            data.pop(i)
            print("deleted successfully")
            break
    else:
            print("Task not found")
#commiting back to file
    with open("data.txt", "w") as file:
        json.dump(data,file,indent=4)
#calling the functions
if action == "add":
    add_task(data,payload)
    print("task added successfully")
elif action == "list":
    if len(sys.argv) > 2: #to make sure it does not give out of bound error while checking
        if payload == "done":
            print([items for items in data if items.get("status")== "done"] or None)
        elif payload == "not done":
            print([items for items in data if items.get("status")== "not done"] or None)
    elif not payload:
        #new design
        if data:
            for item in data:
                print(item)
        else:
            print("nothing to show")
            #initial design
        '''for item in data:
            print(item or "nothing to show")
            For every item in data, print the item; if that particular item is empty, print "nothing to show"'''
elif action == "delete":
    delete_tasks(data,payload)

    


 
