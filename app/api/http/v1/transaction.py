from uuid import UUID
from fastapi import APIRouter, Depends, Response, Request
from starlette.responses import JSONResponse

from app.api.http.depends import DIContainer, DB, Transaction

router = APIRouter(prefix="/transaction", tags=["transactions"])


@router.get("/begin/")
def begin_transaction(
    db: DB = Depends(DIContainer.get_db),
    transactions: dict = Depends(DIContainer.get_transactions_obj)
):
    transaction_id = db.begin(transactions)

    response = Response()
    response.set_cookie("X-Transaction-id", str(transaction_id))
    return response


@router.get("/commit/")
def commit_transactions(
    response: Response,
    db: DB = Depends(DIContainer.get_db),
    transaction_obj: dict = Depends(DIContainer.get_transactions_obj),
    transaction_id: UUID = Depends(DIContainer._get_transaction_id),
) -> None:
    transaction = transaction_obj.get(transaction_id)

    if not transaction:
        return JSONResponse(status_code=400, content="Transaction not found")

    response.delete_cookie("X-Transaction-id")

    del transaction_obj[transaction_id]

    db.commit(transaction)


@router.get("/rollback/")
def delete_data(
    response: Response,
    transaction_obj: dict = Depends(DIContainer.get_transactions_obj),
    transaction_id: UUID = Depends(DIContainer._get_transaction_id),
) -> None:
    transaction = transaction_obj.get(transaction_id)

    if not transaction:
        return JSONResponse(status_code=400, content="Transaction not found")

    response.delete_cookie("X-Transaction-id")

    del transaction_obj[transaction_id]
