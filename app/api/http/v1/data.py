from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.http.depends import DIContainer, ItemUseCase, TransactionItemUseCase

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/")
def fetch_data(
    usecase: ItemUseCase | TransactionItemUseCase = Depends(
        DIContainer.get_item_usecase
    ),
):
    return usecase.fetch_items()


@router.post("/create")
def create_data(
    value: str,
    usecase: ItemUseCase | TransactionItemUseCase = Depends(
        DIContainer.get_item_usecase
    ),
) -> int:
    a = usecase.create_item({"value": value})
    return a


@router.delete("/delete")
def delete_data(
    id: int,
    usecase: ItemUseCase | TransactionItemUseCase = Depends(
        DIContainer.get_item_usecase
    ),
) -> None:
    try:
        return usecase.delete_item(id)
    except ValueError as error:
        return JSONResponse(status_code=404, content=str(error))
