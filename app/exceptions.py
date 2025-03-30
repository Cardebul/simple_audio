from fastapi import HTTPException, status

not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='not found'
)

su_not_allowed = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='have not permission for this operation'
)

invalid_token_type = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid token type"
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)