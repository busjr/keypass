import io
import pyAesCrypt
import json
from setting import BUFFER_SIZE

def check_valid(path, master):
    """Проверяет, можно ли расшифровать файл с заданным паролем"""
    try:
        with open(path, "rb") as fIn:
            fCiph = io.BytesIO(fIn.read())

        fDec = io.BytesIO()
        # Попытка расшифровки данных
        pyAesCrypt.decryptStream(fCiph, fDec, master, BUFFER_SIZE)
        return True
    except Exception as e:
        return False
    
def decrypt(path, master):
        try:
            with open(path, "rb") as fIn:
                fCiph = io.BytesIO(fIn.read())

            fDec = io.BytesIO()
            pyAesCrypt.decryptStream(fCiph, fDec, master, BUFFER_SIZE)
            decrypted_data = fDec.getvalue().decode("utf-8")
            data = json.loads(decrypted_data)
            return data
        except Exception as e:
            print("Ошибка загрузки паролей:", e)
            return None
