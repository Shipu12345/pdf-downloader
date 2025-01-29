import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import asyncio
from calcutta_gazette import download_and_convert_images
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import json


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

ALLOWED_ACCESS = {
    "shipu": "password",
}

@app.get("/progress")
async def progress_stream(request: Request):
    async def event_generator():
        while True:
            try:
                if not os.path.exists('./data/temp_images'):
                    yield f"data: {json.dumps({'status': 'closed', 'message': 'Download directory not found'})}\n\n"
                    break

                image_count = len([f for f in os.listdir('./data/temp_images') if f.endswith(('.jpg', '.png'))])
                yield f"data: {json.dumps({'image_count': image_count})}\n\n"

                await asyncio.sleep(2)
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index-progress.html", {"request": request})

@app.post("/download")
async def download_image(request: Request):
    form = await request.form()
    username = form.get("username")
    access_token = form.get("access_token")
    image_url = form.get("image_url")

    if not username or not access_token or ALLOWED_ACCESS.get(username.lower()) != access_token:
        raise HTTPException(status_code=403, detail="Access denied")

    file_path = await asyncio.to_thread(
        download_and_convert_images, 
        image_url
    )
    
    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type='application/pdf'
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)