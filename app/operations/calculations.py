from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from app.operations import add, subtract, multiply, divide


def compute_result(calc_in: schemas.CalculationCreate) -> float:
    t = calc_in.type
    if t == models.CalculationType.ADD:
        return add(calc_in.a, calc_in.b)
    if t == models.CalculationType.SUBTRACT:
        return subtract(calc_in.a, calc_in.b)
    if t == models.CalculationType.MULTIPLY:
        return multiply(calc_in.a, calc_in.b)
    if t == models.CalculationType.DIVIDE:
        return divide(calc_in.a, calc_in.b)
    raise ValueError("Unsupported calculation type")


def create_calculation(db: Session, calc_in: schemas.CalculationCreate, store_result: bool = True) -> models.Calculation:
    result = None
    if store_result:
        result = compute_result(calc_in)

    calc = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
    )
    db.add(calc)
    try:
        db.commit()
        db.refresh(calc)
    except IntegrityError as e:
        db.rollback()
        raise
    return calc
