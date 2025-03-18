from fastapi import FastAPI, Query
import uvicorn
from aiohttp import ClientSession

import db

URL = "https://jsonplaceholder.typicode.com/users/"

# db.create_db()

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.database.connect()
    

@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()



@app.post("/add_user/")
async def add_user(name: str = Query()):
    query = db.users.insert().values(name=name)
    await db.database.execute(query)
    return dict(msg="Користувача успішно створено.")


@app.get("/users/")
async def get_users():
    users = await fetch()
    # query = db.users.select()
    # users = await db.database.fetch_all(query)
    return dict(msg="Okey", users=users)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    query = db.users.select().where(db.users.c.id==user_id)
    user = await db.database.fetch_one(query)
    return dict(msg="Okey", user=user)


async def fetch(url: str = URL):
    async with ClientSession(trust_env=True) as session:
        result = await session.get(url)
        return await result.json()
    

@app.post("/delete_user/")
async def del_user(user_id: int = Query()):
    query = db.users.delete().where(db.users.c.id==user_id)
    await db.database.execute(query)
    return dict(msg="")
    



if __name__ == "__main__":
    uvicorn.run("main:app")