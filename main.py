import shutil
import subprocess
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/")
def read_root():
    content = """
    <!DOCTYPE html>
    <html>
    <body>
    <form ENCTYPE="multipart/form-data" method="post" action="/">
    <input name="file" type="file"/>
    <input type="submit" value="upload"/>
    </form>
    </body>
    </html>
    """
    return HTMLResponse(content=content)


@app.post("/")
def word2pdf(file: UploadFile = File(...)):
    suffix = file.filename.split(".")[-1]
    if not suffix in ("docx", ".doc"):
        raise HTTPException(500, "Only .doc or .docx.")

    with tempfile.NamedTemporaryFile(suffix=f".{suffix}") as temp:
        shutil.copyfileobj(file.file, temp)
        temp.seek(0)

        input_file = Path(temp.name)
        output_file = Path(temp.name).with_suffix(".pdf")
        tmp_name = temp.name.split(".")[0]
        proc = subprocess.run(
            f"libreoffice --invisible --headless --nologo -env:UserInstallation=file:///tmp/{tmp_name} --convert-to pdf --outdir {input_file.parent.resolve()} {input_file.resolve()}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode > 0:
            print(proc.stdout.decode())
            print(proc.stderr.decode())
            raise HTTPException(500, "Conversion failed.")

    return FileResponse(output_file, media_type="application/pdf")
