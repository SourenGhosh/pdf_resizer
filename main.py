import io
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from PyPDF2 import PdfFileReader, PdfFileWriter
from fastapi.responses import FileResponse


from utils import process_file
app = FastAPI()


@app.post("/resize_file/")
def resizer(file: UploadFile = File(description="Return Pdf")):
    try:
        contents = file.file.read()
        process_file(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    working_dir = Path().absolute().joinpath('expected_out.pdf')

    return FileResponse(path=working_dir, filename='expected_output', media_type="application/pdf",)


