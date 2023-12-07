from fastapi import APIRouter
from ..dependencies import *
from ..models.models import *
from ..schemas.schemas import *
from .authentication import *
router = APIRouter()

#---------------master--------------------------
@router.get('/get_state',response_model=list[StateGet],tags=['Master_state'])
async def get_state(db:Session=Depends(getdb)):
    all_state = db.query(StateModel).order_by(RegionModel.id.desc()).all()
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
#--------master_region---------
@router.get('/get_region',response_model=list[RegionGet],tags=['Master_region'])
async def get_region(db:Session=Depends(getdb)):
    all_region = db.query(RegionModel).order_by(RegionModel.id.desc()).all()
    return all_region
@router.post('/create_region',response_model=RegionBase,tags=['Master_region'])
async def create_region(region:RegionBase,db:Session=Depends(getdb)):
    region_exist = db.query(RegionModel).filter(RegionModel==region.Region).first()
    if region_exist:
        raise HTTPException(status_code=400,detail='Region already exist')
    region = RegionModel(**region.model_dump())
    db.add(region)
    db.commit()
    db.refresh(region)
    return region
@router.put('/update_region/{region_id}',response_model=RegionBase,tags=['Master_region'])
async def update_region(region_id:int,region:RegionBase,db:Session=Depends(getdb)):
    duplicate_exist = db.query(RegionModel).filter(RegionModel.Region==region.Region).first()
    if duplicate_exist:
        raise HTTPException(detail='Region already exists',status_code=400)
    region_exist = db.query(RegionModel).filter(RegionModel.id==region_id).first()
    if region_exist:
        region_exist.Region = region.Region
        region_exist.update_date = datetime.utcnow()
        db.commit()
        db.refresh(region_exist)
        return region_exist
    raise HTTPException(detail='region id does not exists',status_code=400)
@router.delete('/del_region/{region_id}',tags=['Master_region'])
async def del_region(region_id:int,db:Session=Depends(getdb)):
    region_exist = db.query(RegionModel).filter(RegionModel.id == region_id ).first()
    if region_exist:
        db.delete(region_exist)
        db.commit()
        return Response(content='region has been deleted successfully',status_code=200)
    raise HTTPException(detail='region id doess not exist',status_code=400)
#---------master_distric------------------------
@router.get('/get_distric',response_model=list[DistricGet],tags=['Master_Distric'])
async def get_distric(db:Session=Depends(getdb)):
    all_distric = db.query(DistricModel).order_by(DistricModel.id.desc()).all()
    return all_distric
@router.post('/distric_create',response_model=DistricBase,tags=['Master_Distric'])
async def distric_create(distric:DistricBase,db:Session=Depends(getdb)):
    distric_exist = db.query(DistricModel).filter(DistricModel.Distric==distric.Distric).first()
    if distric_exist:
        raise HTTPException(detail='Distric already exists',status_code=400)
    distric_item = DistricModel(**distric.model_dump())
    db.add(distric_item)
    db.commit()
    db.refresh(distric_item)
    return distric_item
@router.put('/update_distric/{distric_id}',response_model=DistricBase,tags=['Master_Distric'])
async def update_distric(distric_id:int,distric:DistricBase,db:Session=Depends(getdb)):
    duplicate_exist = db.query(DistricModel).filter(DistricModel.Distric==distric.Distric).first()
    if duplicate_exist:
        raise HTTPException(detail='Distric already Available',status_code=400)
    distric_exist = db.query(DistricModel).filter(DistricModel.id==distric_id).first()
    if distric_exist:
        distric_exist.Distric =  distric.Distric
        distric_exist.update_date = datetime.utcnow()
        db.commit()
        db.refresh(distric_exist)
        return distric_exist
    raise HTTPException(detail=f"distric id {distric_id} does not exist",status_code=400)
@router.delete('/del_distric/{distric_id}',tags=['Master_Distric'])
async def del_distric(distric_id:int,db:Session=Depends(getdb)):
    distric_exist = db.query(DistricModel).filter(DistricModel.id==distric_id).first()
    if distric_exist:
        db.delete(distric_exist)
        db.commit()
        return Response(content="distric has been delete successfully",status_code=200)
    raise HTTPException(detail=f"distric id {distric_id} does not exists",status_code=400)
    



    


