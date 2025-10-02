from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class AddPatient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient', examples=['John Doe'])]
    city: Annotated[str, Field(..., description='City of the patient', examples=['New York'])]
    age: Annotated[int, Field(..., description='Age of the patient', examples=[30])]
    gender: Annotated[Literal['male','female','others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in meters', examples=[1.75])]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in KG', examples=[85])]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi

    @computed_field
    @property        
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
        
class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(default=None, description='Name of the patient', examples=['John Doe'])]
    city: Annotated[Optional[str], Field(default=None, description='City of the patient', examples=['New York'])]
    age: Annotated[Optional[int], Field(default=None, description='Age of the patient', examples=[30])]
    gender: Annotated[Optional[Literal['male','female','others']], Field(default=None, description='Gender of the patient')]
    height: Annotated[Optional[float], Field(default=None, gt=0, description='Height of the patient in meters', examples=[1.75])]
    weight: Annotated[Optional[float], [Field(default=None, gt=0, description='Weight of the patient in KG', examples=[85])]]

def load_data():
    with open('patients.json') as file:
        data = json.load(file)
    return data

def save_data(data):
    with open('patients.json', 'w') as file:
        data = json.dump(data, file)
    return data

def update_data(data):
    with open('patients.json', 'w') as file:
        data =json.dump(data, file)
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

@app.post('/create')
def create_patient(patient: AddPatient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: UpdatePatient):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_data_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_data_info[key] = value

    # existing_data_info -> pydantic object -> updated bmi + verdict 
    existing_data_info['id'] = patient_id
    patient_pydantic_obj = AddPatient(**existing_data_info)

    # -> pydantic object -> python dict 
    existing_data_info = patient_pydantic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_data_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully'})