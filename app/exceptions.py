from fastapi import HTTPException, status

not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='not found'
)

su_not_allowed = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='have not permission for this operation'
)