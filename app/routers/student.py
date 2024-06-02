from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile

from app.tasks import process_excel_data

router = APIRouter()


@router.post('/students/upload-excel/')
async def upload_excel(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail='Invalid file type. Only .xlsx files are supported.')

    content = await file.read()
    background_tasks.add_task(process_excel_data, content)
    return {'filename': file.filename, 'detail': 'File processing started in the background'}
