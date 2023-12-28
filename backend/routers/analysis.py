from fastapi import APIRouter

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def get_analysis():
    return {"data": {}}
