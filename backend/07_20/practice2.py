# 最簡單的api架構

from fastapi import FastAPI
import uvicorn
from source import get_camera_position, CameraPosition

app = FastAPI()

# # 建立一個 FastAPI「實例」
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}

# # 資料來源為source.py
# @app.get("/")
# def read_root():
#     data:list[CameraPosition] = get_camera_position()
#     return data


# 資料來源為source.py
@app.get("/")
def read_root(burean:str | None = None):
    data:list[CameraPosition] = get_camera_position()
    if not burean:
        return data
    
    burean_datas:list[CameraPosition] = []
    for camera in data:
        if camera.bureau == burean:
            burean_datas.append(camera)
    return burean_datas

if __name__ == "__main__":
    uvicorn.run("practice2:app",reload=True)