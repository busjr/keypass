import json
import io
import pyAesCrypt
from setting import BUFFER_SIZE

def encrypt(path_file, master_entry, data={"passwords": []}):
    json_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")

    input_buffer = io.BytesIO(json_bytes)
    try:
        with open(path_file, "wb") as out_f:
            pyAesCrypt.encryptStream(input_buffer, out_f, master_entry, BUFFER_SIZE)
        print(f"Хранилище создано: {path_file}")
    except Exception as e:
        print("Ошибка при создании хранилища:", e)
