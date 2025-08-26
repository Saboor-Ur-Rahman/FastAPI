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

print(patient1)
print(patient1.name)
print(patient1.age)
print(patient1.address.city)
print(patient1.address.state)
print(patient1.address.zip)