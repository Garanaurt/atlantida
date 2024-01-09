from fastapi import FastAPI
from datetime import datetime
from db_interface import DbSpamer

app = FastAPI()


def is_activation_valid(end_date: str):
    current_date = datetime.now().date()
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
    return current_date <= end_date_obj


@app.get("/check_activation/{activation_code}/hwid/{hwid}")
async def check_activation(activation_code: str, hwid: str):
    with DbSpamer() as db:
        user = db.get_user_data(activation_code)

    if not user:
        return {"status": "code_not_valid"}
    
    if user[4] == hwid:
        if is_activation_valid(user[3]):
            return {"status": "valid", "end": f"{user[3]}"}
        else:
            return {"status": "licence_expired"}
        
    elif user[4] == None:
        if is_activation_valid(user[3]):
            with DbSpamer() as db:
                db.set_hwid_to_user(hwid, activation_code)
            return {"status": "added_hwid", "end": f"{user[3]}"}
             
    else:
        return {"status": "hwid_not_valid"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
