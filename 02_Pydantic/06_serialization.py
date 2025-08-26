from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    zip: str

class Patient(BaseModel):
    name: str
    age: int
    address: Address

address_dict = {'city': 'karachi', 'state': 'Sindh', 'zip': '74200'}

address1 = Address(**address_dict)

patient_dict = {'name': 'saboor', 'age': 30, 'address': address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(include=['address'])
temp1 = patient1.model_dump_json(exclude=['address'])

print(temp)
print(type(temp))

print(temp1)
print(type(temp1))