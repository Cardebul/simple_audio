import uuid

import aiofiles
from fastapi import HTTPException, UploadFile, status

MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024
BASE_PATH = 'audio/'
ALLOWED_AUDIO_TYPES = {
    'audio/mpeg': '.mp3',
    'audio/wav': '.wav',
    'audio/ogg': '.ogg',
}


def create_filename(name: str, filename: str, type: str) -> tuple[str, uuid.UUID]:
    type = ALLOWED_AUDIO_TYPES[type]
    name = name if name else filename
    name = name if name.endswith(type) else f'{name}{type}'
    id = uuid.uuid4()
    full_name = f'{str(id)}{name}'
    return full_name, id
    
async def _upload_audio(file: UploadFile, name: str) -> tuple[str, str, uuid.UUID]:
    if file.content_type not in ALLOWED_AUDIO_TYPES: raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='not allowed type'
    )
    full_name, id = create_filename(name, file.filename, file.content_type)
    full_path = BASE_PATH + full_name
    content = await file.read()
    if len(content) > MAX_FILE_SIZE: raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='len(content) > MAX_FILE_SIZE(1GB)'
    )
    async with aiofiles.open(full_path, 'wb') as f:
        await f.write(content)
    return full_path, full_name, id
