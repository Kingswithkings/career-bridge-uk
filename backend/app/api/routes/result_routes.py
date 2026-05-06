from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...api.dependencies import get_current_user
from ...database import get_db
from ...models.result_model import SavedResult
from ...schemas.result_schema import (
    SaveResultRequest,
    SaveResultResponse,
    SavedResultItem,
)

router = APIRouter(prefix="/api/results", tags=["Results"])


@router.post("/save", response_model=SaveResultResponse)
def save_result(
    request: SaveResultRequest,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):

    saved = SavedResult(
        feature_type=request.feature_type,
        target_role=request.target_role,
        location=request.location,
        input_text=request.input_text,
        result_text=request.result_text,
    )

    db.add(saved)
    db.commit()
    db.refresh(saved)

    return SaveResultResponse(
        id=saved.id,
        message="Result saved successfully",
    )


@router.get("/", response_model=list[SavedResultItem])
def get_results(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):

    return db.query(SavedResult).order_by(SavedResult.created_at.desc()).all()
