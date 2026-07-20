from source import get_camera_position, CameraPosition
from pprint import pprint

# CameraPosition：Pydantic Model

def main():
    data:list[CameraPosition] = get_camera_position() #從source.py匯入取得資料的函式
    pprint(data)

if __name__ == "__main__":
    main()