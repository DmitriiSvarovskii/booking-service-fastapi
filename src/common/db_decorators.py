from functools import wraps
from fastapi import HTTPException
from sqlalchemy.exc import (
    DBAPIError, IntegrityError,
    OperationalError, StatementError
)


def handle_db_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            raise HTTPException(
                status_code=409,
                detail=f"Integrity error: {str(e.orig)}"
            )
        except DBAPIError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database connection error: {str(e)}"
            )
        except StatementError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid SQL statement: {str(e)}"
            )

        except OperationalError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Operational error: {str(e)}"
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )
    return wrapper
