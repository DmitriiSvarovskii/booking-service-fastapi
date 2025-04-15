import logging

from functools import wraps
from fastapi import HTTPException
from sqlalchemy.exc import (
    DBAPIError, IntegrityError,
    OperationalError, StatementError
)

logger = logging.getLogger(__name__)


def handle_db_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            logger.exception("Integrity error occurred")
            raise HTTPException(
                status_code=409,
                detail=f"Integrity error: {str(e.orig)}"
            )
        except DBAPIError as e:
            logger.exception("DBAPI error occurred")
            raise HTTPException(
                status_code=500,
                detail=f"Database connection error: {str(e)}"
            )
        except StatementError as e:
            logger.exception("Statement error occurred")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid SQL statement: {str(e)}"
            )
        except OperationalError as e:
            logger.exception("Operational error occurred")
            raise HTTPException(
                status_code=503,
                detail=f"Operational error: {str(e)}"
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.exception("Unexpected error occurred")
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )
    return wrapper
