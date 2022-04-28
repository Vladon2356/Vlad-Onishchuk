# Cars App
CRUD with PostgreSQL database
##Owners
GET /owners - list owners

GET /owners [?name='Ferdinand']  - list owners [with name Ferdinand]

GET /owners [?age='19']  - list owners [with age 19]

POST /owners  - create an owner

GET /owners/{id}  - get owners by id

PATCH /owners/{id}  - update owner by id

DELETE /users/{id}  - delete owner by id

##Cars
GET /cars/{id}  - get car by id

GET /cars [?owner_id=1] - list cars [with owner_id - 1]

GET /cars [?brand='Porsche'] - list cars [with brand - Porsche]

GET /cars [?price=35000] - list cars [with price - 35000]

GET /cars [?model='911'] - list cars [with model - 911]

POST /cars  - create a car

PATCH /cars/{id}  - update cars by id

DELETE /cars/{id}  - delete cars by id



# How to run it
1. pip install -r requirements.txt
2. Change in file .end DB_STRING for your user
3. alembic upgrade head
4. From root:
```python run.py```
