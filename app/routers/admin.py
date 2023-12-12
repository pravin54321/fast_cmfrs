from fastapi import APIRouter
from ..dependencies import *
from ..models.models import *
from ..schemas.schemas import *
from .authentication import *
router = APIRouter()

#---------------master--------------------------
@router.get('/get_state',response_model=list[StateGet],tags=['Master_state'])
async def get_state(db:Session=Depends(getdb)):
    all_state = db.query(StateModel).order_by(StateModel.id.desc()).all()
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
#--------head_office---------
@router.post('/headoffice_create',response_model=HeadOfficeBase,tags=['Master_HeadOffice'])
async def headoffice_create(headoffice:HeadOfficeBase,db:Session=Depends(getdb)):
    headoffice_exist = db.query(HeadOfficeModel).filter(HeadOfficeModel.HeadOffice==headoffice.HeadOffice).first()
    if headoffice_exist:
        raise HTTPException(detail=f'{headoffice.HeadOffice} already exist',status_code=400)
    head_office = HeadOfficeModel(**headoffice.model_dump())
    db.add(head_office)
    db.commit()
    db.refresh(head_office)
    return head_office
@router.get('/get_headoffice',response_model=list[HeadOfficeGet],tags=['Master_HeadOffice'])    
async def get_headoffice(db:Session=Depends(getdb)):
    all_headoffice=db.query(HeadOfficeModel).order_by(HeadOfficeModel.id.desc()).all()
    return all_headoffice
@router.put('/update_headoffice/{headoffice_id}',response_model=HeadOfficeBase,tags=['Master_HeadOffice'])
async def  update_headoffice(headoffice_id:int,headoffice:HeadOfficeBase,db:Session=Depends(getdb)):
    dupilicate_exist= db.query(HeadOfficeModel).filter(HeadOfficeModel.HeadOffice==headoffice.HeadOffice).first()
    if dupilicate_exist:
        raise HTTPException(detail=f' headoffice {headoffice.HeadOffice} already exist',status_code=400)
    headoffice_exist= db.query(HeadOfficeModel).filter(HeadOfficeModel.id == headoffice_id).first()
    if headoffice_exist:
        headoffice_exist.HeadOffice=headoffice.HeadOffice
        headoffice_exist.State_id=headoffice_exist.HeadOffice
        headoffice_exist.Region_id=headoffice.Region_id
        headoffice_exist.Distric_id=headoffice.Distric_id
        headoffice_exist.update_date=datetime.utcnow()
        db.commit()
        db.refresh(headoffice_exist)
        return headoffice_exist
    raise HTTPException(detail=f'headoffice {headoffice_id} does not exist',status_code=400)
@router.delete('/del_headoffice/{headoffice_id}',tags=['Master_HeadOffice'])
async def del_headoffice(head_office_id:int,db:Session=Depends(getdb)):
    headoffice_exist=db.query(HeadOfficeModel).filter(HeadOfficeModel.id==head_office_id).first()
    if headoffice_exist:
        db.delete(headoffice_exist)
        db.commit()
        return Response(content=f"headoffice has been deleted successfully",status_code=200)
    raise HTTPException(detail=f"headoffice id {head_office_id} does not exist",status_code=400) 
#------subdivision----------------#
@router.post('/crete_subdivision',response_model=SubdivisionBase,tags=['Master_Subdivision'])
async def create_subdivision(subdivision:SubdivisionBase,db:Session=Depends(getdb)):
    subdivision_exist=db.query(SubdivisionModel).filter(SubdivisionModel.Subdivision==subdivision.Subdivision).first()
    if subdivision_exist:
        raise HTTPException(detail=f'{subdivision.Subdivision} subdivision already exist',status_code=400)
    subdivision=SubdivisionModel(**subdivision.model_dump())
    db.add(subdivision)
    db.commit()
    db.refresh(subdivision)
    return subdivision
@router.get('/get_subdivision',response_model=list[SubdivisionGet],tags=['Master_Subdivision'])
async def get_subdivision(db:Session=Depends(getdb)):
    all_subdiviion=db.query(SubdivisionModel).order_by(SubdivisionModel.id.desc()).all()
    return all_subdiviion
@router.put('/update_subdivision/{sudivision_id}',response_model=SubdivisionBase,tags=['Master_Subdivision'])
async def update_subdivision(subdivision_id:int,subdivision:SubdivisionBase,db:Session=Depends(getdb)):
    subdivision_duplicate=db.query(SubdivisionModel).filter(SubdivisionModel.Subdivision==subdivision.Subdivision).first()
    if subdivision_duplicate:
        raise HTTPException(detail=f'{subdivision.Subdivision} subdivision already exist',status_code=400)
    subdivision_exist=db.query(SubdivisionModel).filter(SubdivisionModel.id==subdivision_id).first()
    if subdivision_exist:
       subdivision_exist.Subdivision=subdivision.Subdivision
       subdivision_exist.State_id=subdivision.State_id
       subdivision_exist.Region_id=subdivision.Region_id
       subdivision_exist.Distric_id=subdivision.Distric_id
       subdivision_exist.HeadOffice_id=subdivision.HeadOffice_id
       subdivision_exist.update_date=datetime.utcnow()
       db.commit()
       db.refresh(subdivision_exist)
       return subdivision_exist   
    raise HTTPException(detail=f'subdivision id {subdivision_id} does not exist',status_code=400) 
@router.delete('/del_subdivision/{subdivision_id}',tags=['Master_Subdivision'])
async def del_subdivision(subdivision_id:int,db:Session=Depends(getdb)):
    subdivision_exit=db.query(SubdivisionModel).filter(SubdivisionModel.id==subdivision_id).first()
    if subdivision_exit:
        db.delete(subdivision_exit)
        db.commit()
        return Response(content=f'subdivision id {subdivision_id} has deleted successfully',status_code=200)
    raise HTTPException(detail=f'subdivision id {subdivision_id} does not exist',status_code=400) 
#-----taluka---------
@router.post('/create_taluka',response_model=TalukaBase,tags=['Master_Taluka'])
async def create_taluka(taluka:TalukaBase,db:Session=Depends(getdb)):
    taluka_exit=db.query(TalukaModel).filter(TalukaModel.Taluka==taluka.Taluka).first()
    if taluka_exit:
        raise HTTPException(detail=f'{taluka.Taluka} taluka already exist',status_code=400)
    taluka_item=TalukaModel(**taluka.model_dump())
    db.add(taluka_item)
    db.commit()
    db.refresh(taluka_item) 
    return taluka_item
@router.get('/get_taluka',response_model=list[TalukaGet],tags=['Master_Taluka'])
async def get_taluka(db:Session=Depends(getdb)):
    all_taluka=db.query(TalukaModel).order_by(TalukaModel.id.desc()).all()
    return all_taluka
@router.put('update_taluka/{taluka_id}',response_model=TalukaBase,tags=['Master_Taluka'])
async def update_taluka(taluka_id:int,taluka:TalukaBase,db:Session=Depends(getdb)):
    duplicate_taluka=db.query(TalukaModel).filter(TalukaModel.Taluka==taluka.Taluka).first()
    if duplicate_taluka:
        raise HTTPException(detail=f'{taluka.Taluka} already exist',status_code=400)
    taluka_exist=db.query(TalukaModel).filter(TalukaModel.id==taluka_id).first()
    if taluka_exist:
        taluka_exist.Taluka=taluka.Taluka
        taluka_exist.State_id=taluka.State_id
        taluka_exist.Region_id=taluka.Region_id
        taluka_exist.Distric_id=taluka.Distric_id
        taluka_exist.HeadOffice_id=taluka.HeadOffice_id
        taluka_exist.Subdivision_id=taluka.Subdivision_id
        taluka_exist.update_date=datetime.utcnow()
        db.commit()
        db.refresh(taluka_exist)
        return taluka_exist
@router.delete('del_taluka/{taluka_id}',tags=['Master_Taluka'])
async def del_taluka(taluka_id:int,db:Session=Depends(getdb)):
    taluka_exist=db.query(TalukaModel).filter(TalukaModel.id==taluka_id)
    if taluka_exist:
        db.delete(taluka_exist)
        return Response(content=f'taluka id {taluka_id} has been deleted successfully',status_code=200)
    raise HTTPException(detail=f'tauka id {taluka_id} does not exist')    

#--------police_station-----------
@router.post('/create_policestation',response_model=PoliceStationBase,tags=['Master_Policestation'])
async def create_policestation(policestation:PoliceStationBase,db:Session=Depends(getdb)):
    policestation_exist=db.query(PoliceStationModel).filter(PoliceStationModel.PoliceStation==policestation.PoliceStation).first()
    if policestation_exist:
        raise HTTPException(detail=f'{policestation.PoliceStation} police station already exists',status_code=400)
    policestation_item=PoliceStationModel(**policestation.model_dump())
    db.add(policestation_item)
    db.commit()
    db.refresh(policestation_item)
    return policestation_item
@router.get('/get_policestation',response_model=list[PoliceStationGet],tags=['Master_Policestation'])
async def get_policestation(db:Session=Depends(getdb)):
    all_policestation=db.query(PoliceStationModel).order_by(PoliceStationModel.id.desc()).all()
    return all_policestation
@router.put('/update_policestation/{policestation_id}',response_model=PoliceStationBase,tags=['Master_Policestation'])
async def update_policestation(policestation_id:int,policestation:PoliceStationBase,db:Session=Depends(getdb)):
    policestation_duplicate=db.query(PoliceStationModel).filter(PoliceStationModel.PoliceStation==policestation.PoliceStation).first()
    if policestation_duplicate:
        raise HTTPException(detail=f'{policestation.PoliceStation} policestation already exist',status_code=400)
    policestation_exit=db.query(PoliceStationModel).filter(PoliceStationModel.id==policestation_id).first()
    if policestation_exit:
        policestation_exit.PoliceStation=policestation.PoliceStation
        policestation_exit.State_id=policestation.State_id
        policestation_exit.Distric_id=policestation.Distric_id
        policestation_exit.HeadOffic_id=policestation.HeadOffice_id
        policestation_exit.Subdivision_id=policestation.Subdivision_id
        policestation_exit.Taluka_id=policestation.Taluka_id
        policestation_exit.update_date=datetime.utcnow()
        db.commit()
        db.refresh(policestation_exit)
        return policestation_exit
@router.delete('/del_policestation/{policestation_id}',tags=['Master_Policestation'])
async def del_policestation(policestation_id:int,db:Session=Depends(getdb)):
    policestation_exist=db.query(PoliceStationModel).filter(PoliceStationModel.id==policestation_id).first()  
    if policestation_exist: 
        db.delete(policestation_exist)
        return Response(content=f' police station id {policestation_id}  has been deleted successfully',status_code=200) 
    raise HTTPException(detail=f'police id {policestation_id} ddoes not exist', status_code=400)