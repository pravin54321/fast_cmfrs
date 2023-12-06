from fastapi import APIRouter
from ..dependencies import *
from ..models.models import *
from ..schemas.schemas import *
from .authentication import *
router = APIRouter()

#---------------master--------------------------
@router.get('/get_state',response_model=list[StateGet],tags=['Master_state'])
async def get_state(db:Session=Depends(getdb)):
    all_state = db.query(StateModel).all()
    return all_state
@router.post('/state',tags=['Master_state'])
async def state_create(state:StateBase,db:Session=Depends(getdb)):
    state_exist = db.query(StateModel).filter(StateModel.State==state.State).first()
    if state_exist:
        raise HTTPException(status_code=400,detail='State already exist')
    state = StateModel(**state.model_dump())
    db.add(state)
    db.commit()
    db.refresh(state)
    return state
@router.put('/update_state/{state_id}',response_model=StateBase,tags=['Master_state'])
async def update_state(state_id:int,state:StateBase,db:Session=Depends(getdb)):
    duplicate_state = db.query(StateModel).filter(StateModel.State==state.State).first()
    if duplicate_state:
        raise HTTPException(status_code=400,detail="State already exists")
    state_exist = db.query(StateModel).filter(StateModel.id==state_id).first()
    if state_exist:
        state_exist.State = state.State
        state_exist.update_date = datetime.utcnow()
        db.commit()
        db.refresh(state_exist)
        return state_exist
    raise HTTPException(status_code=404,detail="State not present") 
@router.delete('/delete_state/{state_id}',tags=['Master_state'])
async def delete_state(state_id:int,db:Session=Depends(getdb)):
    state_exist = db.query(StateModel).filter(StateModel.id==state_id).first()
    if state_exist:
        db.delete(state_exist)
        db.commit()
    return Response(content=f"State has been deleted successfully",status_code=200) 



