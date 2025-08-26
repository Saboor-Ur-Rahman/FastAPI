from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('patients.json') as file:
        data = json.load(file)
    return data

@app.get('/')
def hello():
    return {'message': 'Patient Management System API'}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/view/{patient_id}')
def view_patient(patient_id: str =  Path(...,description="The ID of the patient to view", example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort(sort_by: str = Query(..., description="Field to sort by: 'height', 'weight', 'bmi'"), order: str = Query('asc', description="Order of sorting: 'asc' or 'desc'")):
    
    valid_sort_fields = ['height', 'weight', 'bmi']
    valid_order_fields = ['asc', 'desc']

    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {valid_sort_fields}")
    
    if order not in valid_order_fields:
        raise HTTPException(status_code=400, detail=f"Invalid order field. Valid fields are: {valid_order_fields}")
    
    data = load_data()

    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data