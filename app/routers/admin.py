from fastapi import APIRouter
from ..dependencies import *
from ..models.models import *
from ..schemas.schemas import *
from .authentication import *

router = APIRouter()

#---------------master--------------------------
@router.get('/get_state',response_model=list[StateGet],tags=['Master_state'])
async def get_state(current_user:Annotated[UserBase,Depends(get_current_active_user)],db:Session=Depends(getdb)):
    all_state = db.query(StateModel).order_by(StateModel.id.desc()).all()
    return all_state
@router.post('/state',response_model=StateGet,tags=['Master_state'])
async def state_create(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       state:StateBase,db:Session=Depends(getdb)):
    state_exist = db.query(StateModel).filter(StateModel.State==state.State).first()
    if state_exist:
        raise HTTPException(status_code=400,detail='State already exist')
    state = StateModel(**state.model_dump())
    db.add(state)
    db.commit()
    db.refresh(state)
    return state
@router.put('/update_state/{state_id}',response_model=StateGet,tags=['Master_state'])
async def update_state(current_user:Annotated[UserBase,Depends(get_current_active_user)]
                       ,state_id:int,state:StateBase,db:Session=Depends(getdb)):
    duplicate_state = db.query(StateModel).filter(StateModel.State==state.State).first()
    if duplicate_state:
        raise HTTPException(status_code=400,detail=f"{state.State} already exists")
    state_exist = db.query(StateModel).filter(StateModel.id==state_id).first()
    if state_exist:
        state_exist.State = state.State
        db.commit()
        db.refresh(state_exist)
        return state_exist
    raise HTTPException(status_code=404,detail=f"id-{state_id} does not exist",) 
@router.delete('/delete_state/{state_id}',tags=['Master_state'])
async def delete_state(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       state_id:int,db:Session=Depends(getdb)):
    state_exist = db.query(StateModel).filter(StateModel.id==state_id).first()
    if state_exist:
        db.delete(state_exist)
        db.commit()
        return Response(content=f"State_id {state_id} has been deleted successfully",status_code=200) 
    raise HTTPException(detail=f"id-{state_id} does not exist",status_code=status.HTTP_404_NOT_FOUND)
    
#--------master_region---------
@router.get('/get_region',response_model=list[RegionGet],tags=['Master_region'])
async def get_region(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                     db:Session=Depends(getdb)):
    all_region = db.query(RegionModel).order_by(RegionModel.id.desc()).all()
    return all_region
@router.post('/create_region',response_model=RegionGet,tags=['Master_region'])
async def create_region(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                        region:RegionBase,db:Session=Depends(getdb)):
    region_exist = db.query(RegionModel).filter(RegionModel==region.Region).first()
    if region_exist:
        raise HTTPException(status_code=400,detail=f'{region.Region} already exist')
    region = RegionModel(**region.model_dump())
    db.add(region)
    db.commit()
    db.refresh(region)
    return region
@router.put('/update_region/{region_id}',response_model=RegionGet,tags=['Master_region'])
async def update_region(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                        region_id:int,region:RegionBase,db:Session=Depends(getdb)):
    duplicate_exist = db.query(RegionModel).filter(RegionModel.Region==region.Region,RegionModel.id !=region_id).first()
    if duplicate_exist:
        raise HTTPException(detail=f'{region.Region} already exists',status_code=400)
    region_exist = db.query(RegionModel).filter(RegionModel.id==region_id).first()
    if region_exist:
        region_exist.Region = region.Region
        region_exist.State_id=region.State_id     
        db.commit()
        db.refresh(region_exist)
        return region_exist
    raise HTTPException(detail=f'id-{region_id} does not exist',status_code=400)
@router.delete('/del_region/{region_id}',tags=['Master_region'])
async def del_region(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                     region_id:int,db:Session=Depends(getdb)):
    region_exist = db.query(RegionModel).filter(RegionModel.id == region_id ).first()
    if region_exist:
        db.delete(region_exist)
        db.commit()
        return Response(content=f'id-{region_id} has been deleted successfully',status_code=200)
    raise HTTPException(detail=f'id-{region_id} doess not exist',status_code=400)
#---------master_distric------------------------
@router.get('/get_distric',response_model=list[DistricGet],tags=['Master_Distric'])
async def get_distric(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                      db:Session=Depends(getdb)):
    all_distric = db.query(DistricModel).order_by(DistricModel.id.desc()).all()
    return all_distric
@router.post('/distric_create',response_model=DistricGet,tags=['Master_Distric'])
async def distric_create(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         distric:DistricBase,db:Session=Depends(getdb)):
    distric_exist = db.query(DistricModel).filter(DistricModel.Distric==distric.Distric).first()
    if distric_exist:
        raise HTTPException(detail=f'{distric.Distric} already exists',status_code=400)
    distric_item = DistricModel(**distric.model_dump())
    db.add(distric_item)
    db.commit()
    db.refresh(distric_item)
    return distric_item
@router.put('/update_distric/{distric_id}',response_model=DistricGet,tags=['Master_Distric'])
async def update_distric(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                        distric_id:int,distric:DistricBase,db:Session=Depends(getdb)):
    duplicate_exist = db.query(DistricModel).filter(DistricModel.Distric==distric.Distric,DistricModel.id !=distric_id).first()
    if duplicate_exist:
        raise HTTPException(detail=f'{distric.Distric} already Available',status_code=400)
    distric_exist = db.query(DistricModel).filter(DistricModel.id==distric_id).first()
    if distric_exist:
        distric_exist.Distric =  distric.Distric 
        distric_exist.State_id=distric.State_id
        distric_exist.Region_id=distric.Region_id   
        db.commit()
        db.refresh(distric_exist)
        return distric_exist
    raise HTTPException(detail=f"id {distric_id} does not exist",status_code=400)
@router.delete('/del_distric/{distric_id}',tags=['Master_Distric'])
async def del_distric(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                     distric_id:int,db:Session=Depends(getdb)):
    distric_exist = db.query(DistricModel).filter(DistricModel.id==distric_id).first()
    if distric_exist:
        db.delete(distric_exist)
        db.commit()
        return Response(content=f"distric id-{distric_id} has been delete successfully",status_code=200)
    raise HTTPException(detail=f"distric id {distric_id} does not exists",status_code=400)
@router.get('/state_region/{state_id}',response_model=list[StateRegion],tags=['Master_Distric'])
async def state_region(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       state_id:int,db:Session=Depends(getdb)):
    region_exist=db.query(RegionModel).filter(RegionModel.State_id==state_id).all()
    return region_exist
#--------head_office---------
@router.post('/headoffice_create',response_model=HeadOfficeGet,tags=['Master_HeadOffice'])
async def headoffice_create(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            headoffice:HeadOfficeBase,db:Session=Depends(getdb)):
    headoffice_exist = db.query(HeadOfficeModel).filter(HeadOfficeModel.HeadOffice==headoffice.HeadOffice).first()
    if headoffice_exist:
        raise HTTPException(detail=f'{headoffice.HeadOffice} already exist',status_code=400)
    head_office = HeadOfficeModel(**headoffice.model_dump())
    db.add(head_office)
    db.commit()
    db.refresh(head_office)
    return head_office
@router.get('/get_headoffice',response_model=list[HeadOfficeGet],tags=['Master_HeadOffice'])    
async def get_headoffice(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         db:Session=Depends(getdb)):
    all_headoffice=db.query(HeadOfficeModel).order_by(HeadOfficeModel.id.desc()).all()
    return all_headoffice
@router.put('/update_headoffice/{headoffice_id}',response_model=HeadOfficeGet,tags=['Master_HeadOffice'])
async def  update_headoffice(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             headoffice_id:int,headoffice:HeadOfficeBase,db:Session=Depends(getdb)):
    dupilicate_exist= db.query(HeadOfficeModel).filter(HeadOfficeModel.HeadOffice==headoffice.HeadOffice,HeadOfficeModel.id != headoffice_id).first()
    if dupilicate_exist:
        raise HTTPException(detail=f' headoffice {headoffice.HeadOffice} already exist',status_code=400)
    headoffice_exist= db.query(HeadOfficeModel).filter(HeadOfficeModel.id == headoffice_id).first()
    if headoffice_exist:
        headoffice_exist.HeadOffice=headoffice.HeadOffice
        headoffice_exist.State_id=headoffice.State_id
        headoffice_exist.Region_id=headoffice.Region_id
        headoffice_exist.Distric_id=headoffice.Distric_id      
        db.commit()
        db.refresh(headoffice_exist)
        return headoffice_exist
    raise HTTPException(detail=f'headoffice {headoffice_id} does not exist',status_code=400)
@router.delete('/del_headoffice/{headoffice_id}',tags=['Master_HeadOffice'])
async def del_headoffice(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         headoffice_id:int,db:Session=Depends(getdb)):
    headoffice_exist=db.query(HeadOfficeModel).filter(HeadOfficeModel.id==headoffice_id).first()
    if headoffice_exist:
        db.delete(headoffice_exist)
        db.commit()
        return Response(content=f"headoffice id-{headoffice_id} has been deleted successfully",status_code=200)
    raise HTTPException(detail=f"headoffice id {headoffice_id} does not exist",status_code=400) 
@router.get('/region_distric/{region_id}',response_model=list[RegionDistric],tags=['Master_HeadOffice'])
async def region_distric(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         region_id:int,db:Session=Depends(getdb)):
    list_distric=db.query(DistricModel).filter(DistricModel.Region_id==region_id).all()
    return list_distric
#------subdivision----------------#
@router.post('/crete_subdivision',response_model=SubdivisionGet,tags=['Master_Subdivision'])
async def create_subdivision(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             subdivision:SubdivisionBase,db:Session=Depends(getdb)):
    subdivision_exist=db.query(SubdivisionModel).filter(SubdivisionModel.Subdivision==subdivision.Subdivision).first()
    if subdivision_exist:
        raise HTTPException(detail=f'{subdivision.Subdivision} subdivision already exist',status_code=400)
    subdivision=SubdivisionModel(**subdivision.model_dump())
    db.add(subdivision)
    db.commit()
    db.refresh(subdivision)
    return subdivision
@router.get('/get_subdivision',response_model=list[SubdivisionGet],tags=['Master_Subdivision'])
async def get_subdivision(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          db:Session=Depends(getdb)):
    all_subdiviion=db.query(SubdivisionModel).order_by(SubdivisionModel.id.desc()).all()
    return all_subdiviion
@router.put('/update_subdivision/{sudivision_id}',response_model=SubdivisionBase,tags=['Master_Subdivision'])
async def update_subdivision(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             subdivision_id:int,subdivision:SubdivisionBase,db:Session=Depends(getdb)):
    subdivision_duplicate=db.query(SubdivisionModel).filter(SubdivisionModel.Subdivision==subdivision.Subdivision,SubdivisionModel.id!=subdivision_id).first()
    if subdivision_duplicate:
        raise HTTPException(detail=f'{subdivision.Subdivision} subdivision already exist',status_code=400)
    subdivision_exist=db.query(SubdivisionModel).filter(SubdivisionModel.id==subdivision_id).first()
    if subdivision_exist:
       subdivision_exist.Subdivision=subdivision.Subdivision
       subdivision_exist.State_id=subdivision.State_id
       subdivision_exist.Region_id=subdivision.Region_id
       subdivision_exist.Distric_id=subdivision.Distric_id
       subdivision_exist.HeadOffice_id=subdivision.HeadOffice_id     
       db.commit()
       db.refresh(subdivision_exist)
       return subdivision_exist   
    raise HTTPException(detail=f'subdivision id {subdivision_id} does not exist',status_code=400) 
@router.delete('/del_subdivision/{subdivision_id}',tags=['Master_Subdivision'])
async def del_subdivision(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          subdivision_id:int,db:Session=Depends(getdb)):
    subdivision_exit=db.query(SubdivisionModel).filter(SubdivisionModel.id==subdivision_id).first()
    if subdivision_exit:
        db.delete(subdivision_exit)
        db.commit()
        return Response(content=f'subdivision id {subdivision_id} has deleted successfully',status_code=200)
    raise HTTPException(detail=f'subdivision id {subdivision_id} does not exist',status_code=400)
@router.get('/distric_headoffice/{distric_id}',response_model=list[DistricHeadoffice],tags=['Master_Subdivision'])
async def distric_headoffice(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             distric_id:int,db:Session=Depends(getdb)):
    list_headoffice=db.query(HeadOfficeModel).filter(HeadOfficeModel.Distric_id==distric_id).all()
    return list_headoffice

#-----taluka---------
@router.post('/create_taluka',response_model=TalukaGet,tags=['Master_Taluka'])
async def create_taluka(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                        taluka:TalukaBase,db:Session=Depends(getdb)):
    taluka_exit=db.query(TalukaModel).filter(TalukaModel.Taluka==taluka.Taluka).first()
    if taluka_exit:
        raise HTTPException(detail=f'{taluka.Taluka} taluka already exist',status_code=400)
    taluka_item=TalukaModel(**taluka.model_dump())
    db.add(taluka_item)
    db.commit()
    db.refresh(taluka_item) 
    return taluka_item
@router.get('/get_taluka',response_model=list[TalukaGet],tags=['Master_Taluka'])
async def get_taluka(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                     db:Session=Depends(getdb)):
    all_taluka=db.query(TalukaModel).order_by(TalukaModel.id.desc()).all()
    return all_taluka
@router.put('/update_taluka/{taluka_id}',response_model=TalukaGet,tags=['Master_Taluka'])
async def update_taluka(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                        taluka_id:int,taluka:TalukaBase,db:Session=Depends(getdb)):
    duplicate_taluka=db.query(TalukaModel).filter(TalukaModel.Taluka==taluka.Taluka,TalukaModel.id!=taluka_id).first()
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
        db.commit()
        db.refresh(taluka_exist)
        return taluka_exist
@router.delete('/del_taluka/{taluka_id}',tags=['Master_Taluka'])
async def del_taluka(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                     taluka_id:int,db:Session=Depends(getdb)):
    taluka_exist=db.query(TalukaModel).filter(TalukaModel.id==taluka_id).first()
    if taluka_exist:
        db.delete(taluka_exist)
        db.commit()
        return Response(content=f'taluka id {taluka_id} has been deleted successfully',status_code=200)
    raise HTTPException(detail=f'tauka id {taluka_id} does not exist') 
@router.get('/headoffice_subdivision/{headoffice_id}',response_model=list[HodSubdivision],tags=['Master_Taluka'])
async def hod_subdivision(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          headoffice_id:int,db:Session=Depends(getdb)):
    list_subdivision=db.query(SubdivisionModel).filter(SubdivisionModel.HeadOffice_id==headoffice_id).all()
    return list_subdivision   

#--------police_station-----------
@router.post('/create_policestation',response_model=PoliceStationGet,tags=['Master_Policestation'])
async def create_policestation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                               policestation:PoliceStationBase,db:Session=Depends(getdb)):
    policestation_exist=db.query(PoliceStationModel).filter(PoliceStationModel.PoliceStation==policestation.PoliceStation).first()
    if policestation_exist:
        raise HTTPException(detail=f'{policestation.PoliceStation} police station already exists',status_code=400)
    policestation_item=PoliceStationModel(**policestation.model_dump())
    db.add(policestation_item)
    db.commit()
    db.refresh(policestation_item)
    return policestation_item
@router.get('/get_policestation',response_model=list[PoliceStationGet],tags=['Master_Policestation'])
async def get_policestation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            db:Session=Depends(getdb)):
    all_policestation=db.query(PoliceStationModel).order_by(PoliceStationModel.id.desc()).all()
    return all_policestation
@router.put('/update_policestation/{policestation_id}',response_model=PoliceStationGet,tags=['Master_Policestation'])
async def update_policestation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                               policestation_id:int,policestation:PoliceStationBase,db:Session=Depends(getdb)):
    policestation_duplicate=db.query(PoliceStationModel).filter(PoliceStationModel.PoliceStation==policestation.PoliceStation,PoliceStationModel.id!=policestation_id).first()
    if policestation_duplicate:
        raise HTTPException(detail=f'{policestation.PoliceStation} policestation already exist',status_code=400)
    policestation_exit=db.query(PoliceStationModel).filter(PoliceStationModel.id==policestation_id).first()
    if policestation_exit:
        policestation_exit.PoliceStation=policestation.PoliceStation
        policestation_exit.State_id=policestation.State_id
        policestation_exit.Region_id=policestation.Region_id
        policestation_exit.Distric_id=policestation.Distric_id
        policestation_exit.HeadOffice_id=policestation.HeadOffice_id
        policestation_exit.Subdivision_id=policestation.Subdivision_id
        policestation_exit.Taluka_id=policestation.Taluka_id
        db.commit()
        db.refresh(policestation_exit)
        return policestation_exit
@router.delete('/del_policestation/{policestation_id}',tags=['Master_Policestation'])
async def del_policestation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            policestation_id:int,db:Session=Depends(getdb)):
    policestation_exist=db.query(PoliceStationModel).filter(PoliceStationModel.id==policestation_id).first()  
    if policestation_exist: 
        db.delete(policestation_exist)
        db.commit()
        return Response(content=f' police station id {policestation_id}  has been deleted successfully',status_code=200) 
    raise HTTPException(detail=f'police id {policestation_id} ddoes not exist', status_code=400)
@router.get('/subdivision_taluka/{subdivision_id}',response_model=list[SubdivisionTaluka],tags=['Master_Policestation'])
async def subdivision_taluka(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             subdivision_id:int,db:Session=Depends(getdb)):
    list_taluka=db.query(TalukaModel).filter(TalukaModel.Subdivision_id==subdivision_id).all()
    return list_taluka
#--------post------------
@router.post('/create_post',response_model=PostGet,tags=['Master_Post'])
async def post_create(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                      post:PostBase,db:Session=Depends(getdb)):
    post_exist=db.query(PostModel).filter(PostModel.Post==post.Post).first()
    if post_exist:
        raise HTTPException(detail=f'{post.Post} post already exist',status_code=400)
    post_item=PostModel(**post.model_dump())
    db.add(post_item)
    db.commit()
    db.refresh(post_item)
    return post_item
@router.get('/get_post',response_model=list[PostGet],tags=['Master_Post'])
async def get_post(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                   db:Session=Depends(getdb)):
   all_post=db.query(PostModel).order_by(PostModel.id.desc()).all()
   return all_post
@router.put('/update/{post_id}',response_model=PostGet,tags=['Master_Post'])
async def update_post(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                      post_id:int,post:PostBase,db:Session=Depends(getdb)):
    post_duplicate=db.query(PostModel).filter(PostModel.Post==post.Post,PostModel.id!=post_id).first()
    if post_duplicate:
        raise HTTPException(detail=f"{post.Post} post already exist",status_code=400)
    post_exit=db.query(PostModel).filter(PostModel.id==post_id).first()
    if post_exit:
        post_exit.Post=post.Post
        post_exit.State_id=post.State_id
        post_exit.Region_id=post.Region_id
        post_exit.Distric_id=post.Distric_id
        post_exit.HeadOffice_id=post.HeadOffice_id
        post_exit.Subdivision_id=post.Subdivision_id
        post_exit.Taluka_id=post.Subdivision_id
        post_exit.PoliceStation_id=post.PoliceStation_id
        db.commit()
        db.refresh(post_exit)
        return post_exit
    raise HTTPException(detail=f'{post_id} id does not exist',status_code=status.HTTP_404_NOT_FOUND)
@router.delete('/del_post/{post_id}',tags=['Master_Post'])
async def del_post(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                  post_id:int,db:Session=Depends(getdb)):
    post_exist=db.query(PostModel).filter(PostModel.id==post_id).first()
    if post_exist:
        db.delete(post_exist)
        db.commit()
        return Response(content=f' id {post_id} has been deleted successfully',status_code=200)
    raise HTTPException(detail=f'id-{post_id} does not exist',status_code=status.HTTP_404_NOT_FOUND)
@router.get('/taluka_policestation/{taluka_id}',response_model=list[TalukaPolicestation],tags=['Master_Post'])
async def taluka_policestation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                                taluka_id:int,db:Session=Depends(getdb)):
    list_policestation=db.query(PoliceStationModel).filter(PoliceStationModel.Taluka_id==taluka_id).all()
    return list_policestation
#_____________________________master_cast_______________________________________
@router.post('/create_religion',response_model=ReligionGet,tags=['Master_Religion'])
async def religion_create(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          religion:ReligionBase,db:Session=Depends(getdb)):
    religion_exist=db.query(ReligionModel).filter(ReligionModel.Religion==religion.Religion).first()
    if religion_exist:
        raise HTTPException(detail=f'{religion.Religion} religion already exist',status_code=400)
    religion_item=ReligionModel(**religion.model_dump())
    db.add(religion_item)
    db.commit()
    db.refresh(religion_item) 
    return religion_item
@router.get('/get_religion',response_model=list[ReligionGet],tags=['Master_Religion'])
async def get_religion(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       db:Session=Depends(getdb)):
    all_religion=db.query(ReligionModel).order_by(ReligionModel.id.desc()).all()
    return all_religion
@router.put('/update_religion/{religion_id}',response_model=ReligionGet,tags=['Master_Religion'])
async def religion_update(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          religion_id:int,religion:ReligionBase,db:Session=Depends(getdb)):
    duplicate_religion=db.query(ReligionModel).filter(ReligionModel.Religion==religion.Religion,ReligionModel.id!=religion_id).first()
    if duplicate_religion:
        raise HTTPException(detail=f'{religion.Religion} religion already exist',status_code=400)
    religion_exist=db.query(ReligionModel).filter(ReligionModel.id==religion_id).first()
    if religion_exist:
        religion_exist.Religion=religion.Religion
        db.commit()
        db.refresh(religion_exist)
        return religion_exist
    raise HTTPException(detail=f'{religion_id} id does not exist ',status_code=status.HTTP_404_NOT_FOUND)
@router.delete('/religion_del/{religion_id}',tags=['Master_Religion'])
async def religion_del(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       religion_id=int,db:Session=Depends(getdb)):
    religion_exist=db.query(ReligionModel).filter(ReligionModel.id==religion_id).first()
    if religion_exist:
        db.delete(religion_exist)
        db.commit()
        return Response(content=f' Religion id {religion_id} has been deleted successfully',status_code=200) 
    raise HTTPException(detail=f'religion id {religion_id} does not exist',status_code=400)
   
#---------create_cast--------------
@router.post('/create_cast',response_model=CasteGet,tags=['Master_Cast'])
async def create_cast(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                      cast:CastBase,db:Session=Depends(getdb)):
    cast_exit=db.query(CastModel).filter(CastModel.Cast==cast.Cast).first()
    if cast_exit:
        raise HTTPException(detail=f'{cast.Cast} already exist',status_code=400)
    cast_item=CastModel(**cast.model_dump())
    db.add(cast_item)
    db.commit()
    db.refresh(cast_item)   
    return cast_item 
@router.get('/get_cast',response_model=list[CasteGet],tags=['Master_Cast'])
async def get_cast(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                   db:Session=Depends(getdb)):
    all_cast=db.query(CastModel).order_by(CastModel.id.desc()).all()
    return all_cast
@router.put('/update_cast/{cast_id}',response_model=CasteGet,tags=['Master_Cast'])
async def update_cast(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                      cast_id:int,cast:CastBase,db:Session=Depends(getdb)):
    duplicate_cast=db.query(CastModel).filter(CastModel.Cast==cast.Cast,CastModel.id!=cast_id).first()
    if duplicate_cast:
        raise HTTPException(detail=f'{cast.Cast} already exist',status_code=400)
    cast_exist=db.query(CastModel).filter(CastModel.id==cast_id).first()
    if cast_exist:
        cast_exist.Cast=cast.Cast
        cast_exist.Religion_id=cast.Religion_id
        db.commit()
        db.refresh(cast_exist)
        return cast_exist
    raise HTTPException(detail=f'id {cast_id} does not exist',status_code=400)
@router.delete('/cast_del/{cast_id}',tags=['Master_Cast'])
async def del_cast(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                   cast_id:int,db:Session=Depends(getdb)):
    cast_exist=db.query(CastModel).filter(CastModel.id==cast_id).first()
    if cast_exist:
        db.delete(cast_exist)
        db.commit()
        return Response(content=f"id-{cast_id} has been deleted successfully",status_code=200)
    raise HTTPException(detail=f'id-{cast_id} does not exist',status_code=400)

#-----subcast-----------
@router.post('/create_subcast',response_model=SubcastGet,tags=['Master_Subcast'])
async def create_subcast(current_user: Annotated[UserBase, Depends(get_current_active_user)],
                        subcast:SubcastBase,db:Session=Depends(getdb)):
    subcast_exit=db.query(SubcastModel).filter(SubcastModel.Subcast==subcast.Subcast).first()
    if subcast_exit:
        raise HTTPException(detail=f'{subcast.Subcast} already exist',status_code=400)
    subcast_item=SubcastModel(**subcast.model_dump())
    db.add(subcast_item)
    db.commit()
    db.refresh(subcast_item)
    return subcast_item
@router.get('/get_subcast',response_model=list[SubcastGet],tags=['Master_Subcast'])
async def get_subcast(current_user: Annotated[UserBase, Depends(get_current_active_user)],
                      db:Session=Depends(getdb)):
    all_subcast=db.query(SubcastModel).order_by(SubcastModel.id.desc()).all()
    return(all_subcast)
@router.put('/update_subcast/{subcast_item}',response_model=SubcastGet,tags=['Master_Subcast'])
async def update_subcast(current_user: Annotated[UserBase, Depends(get_current_active_user)],
                         subcast_item:int,subcast:SubcastBase,db:Session=Depends(getdb)):
    subcast_duplicate=db.query(SubcastModel).filter(SubcastModel.Subcast==subcast.Subcast,SubcastModel.id!=subcast_item).first()
    if subcast_duplicate:
       raise HTTPException(detail=f'{subcast.Subcast} already exit',status_code=400)
    subcast_exit=db.query(SubcastModel).filter(SubcastModel.id==subcast_item).first()
    if subcast_exit:
        subcast_exit.Subcast=subcast.Subcast
        subcast_exit.Religion_id=subcast.Religion_id
        subcast_exit.Cast_id=subcast.Cast_id
        db.commit()
        db.refresh(subcast_exit)
        return subcast_exit
    raise HTTPException(detail='id-{subcast_item} does not exist',status_code=400)
@router.delete('/delete_subcast/{subcast_item}',tags=['Master_Subcast'])
async def del_subcast( current_user: Annotated[UserBase, Depends(get_current_active_user)],
                       subcast_item:int,db:Session=Depends(getdb)):
    subcast_exit=db.query(SubcastModel).filter(SubcastModel.id==subcast_item).first()
    if subcast_exit:
        db.delete(subcast_exit)
        db.commit()
        return Response(content=f'id-{subcast_item} has been deleted successfully',status_code=200)
    raise HTTPException(detail=f'id-{subcast_item} does not exist',status_code=400)
@router.get('/religion_cast/{religion_id}',response_model=list[ReligionCast],tags=['Master_Subcast'])
async def religion_cast(current_user:Annotated[UserBase,Depends(get_current_active_user)],religion_id:int,
                        db:Session=Depends(getdb)):
    list_cast=db.query(CastModel).filter(CastModel.Religion_id==religion_id).all()
    return list_cast
#--------langues----------
@router.post('/create_langues',response_model=LanguesGet,tags=['Master_Langues'])
async def create_langues(current_user: Annotated[UserBase, Depends(get_current_active_user)],
                        langues:LanguesBase,db:Session=Depends(getdb)):
    langues_exit=db.query(LanguesModel).filter(LanguesModel.Langues==langues.Langues).first()
    if langues_exit:
        raise HTTPException(detail=f'{langues.Langues} already exist',status_code=400)
    langues_item=LanguesModel(**langues.model_dump())
    db.add(langues_item)
    db.commit()
    db.refresh(langues_item)
    return langues_item
@router.get('/get_langues',response_model=list[LanguesGet],tags=['Master_Langues'])
async def get_langues(current_user: Annotated[UserBase, Depends(get_current_active_user)],
                      db:Session=Depends(getdb)):
    all_langues=db.query(LanguesModel).order_by(LanguesModel.id.desc()).all()
    return all_langues
@router.put('/update_langues/{langues_id}',response_model=LanguesGet,tags=['Master_Langues'])
async def update_langues( current_user: Annotated[UserBase, Depends(get_current_active_user)],
                          langues_id:int,langues:LanguesBase,db:Session=Depends(getdb)):
    langues_duplicate=db.query(LanguesModel).filter(LanguesModel.Langues==langues.Langues).first()
    if langues_duplicate:
        raise HTTPException(detail=f'{langues.Langues} already exist',status_code=400)
    langues_exit=db.query(LanguesModel).filter(LanguesModel.id==langues_id).first()
    if langues_exit:
        langues_exit.Langues=langues.Langues
        db.commit()
        db.refresh(langues_exit)
        return langues_exit
@router.delete('/del_langues/{langues_id}',tags=['Master_Langues'])
async def dlt_langues(current_user: Annotated[UserBase, Depends(get_current_active_user)],
                      langues_id:int,db:Session=Depends(getdb)):
    langues_exit=db.query(LanguesModel).filter(LanguesModel.id==langues_id).first()
    if langues_exit:
        db.delete(langues_exit)
        db.commit()
        return Response(content=f'id-{langues_id} has been  deleted successfully',status_code=200)  
    raise HTTPException(detail=f'id-{langues_id} does not exist',status_code=400) 
#_____occupation_________
@router.post('/create_occupation',response_model=OccupationGet,tags=['Master_Occupation'])
async def create_occupation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            occupation:OccupationBase,db:Session=Depends(getdb)):
    occupation_exist=db.query(OccupationModel).filter(OccupationModel.Occupation==occupation.Occupation).first()
    if occupation_exist:
        raise HTTPException(detail=f'{occupation.Occupation} already exist',status_code=400)
    occupation_item=OccupationModel(**occupation.model_dump())
    db.add(occupation_item)
    db.commit()
    db.refresh(occupation_item)
    return occupation_item
@router.get('/get_occupation',response_model=list[OccupationGet],tags=['Master_Occupation'])
async def get_occupation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         db:Session=Depends(getdb)):
    all_occupation=db.query(OccupationModel).order_by(OccupationModel.id.desc()).all() 
    return all_occupation
@router.put('/update_occupation/{occupation_id}',response_model=OccupationGet,tags=['Master_Occupation'])
async def update_occupation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             occupation:OccupationBase,occupation_id:int,db:Session=Depends(getdb)):
    occupation_duplicate=db.query(OccupationModel).filter(OccupationModel.Occupation==occupation.Occupation).first()
    if occupation_duplicate:
        raise HTTPException(detail=f"{occupation.Occupation} already exist",status_code=400)
    occupation_exist=db.query(OccupationModel).filter(OccupationModel.id==occupation_id).first()
    if occupation_exist:
        occupation_exist.Occupation=occupation.Occupation
        db.commit()
        db.refresh(occupation_exist)
        return occupation_exist
@router.delete('/dlt_occupation/{occupation_item}',tags=['Master_Occupation'])
async def dlt_occupation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         occupation_id:int,db:Session=Depends(getdb)):
    occupation_exist=db.query(OccupationModel).filter(OccupationModel.id==occupation_id).first() 
    if occupation_exist:
        db.delete(occupation_exist)
        db.commit()
        return Response(content=f'id-{occupation_id} has been deleted successfully',status_code=200) 
    raise HTTPException(detail=f"id-{occupation_id} does not exist",status_code=400) 
#______outhperson________
@router.post('/create_outhperson',response_model=OuthPersonGet,tags=['Master_Outhperson'])
async def create_outhperson(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            outhperson:OuthPersonBase,db:Session=Depends(getdb)):
    outhperson_exist=db.query(OuthPersonModel).filter(OuthPersonModel.OuthPerson==outhperson.OuthPerson).first()
    if outhperson_exist:
        raise HTTPException(detail=f'{outhperson.OuthPerson} already exist',status_code=400)
    outhperson_item=OuthPersonModel(**outhperson.model_dump())
    db.add(outhperson_item)
    db.commit()
    db.refresh(outhperson_item)
    return outhperson_item
@router.get('/get_outhperson',response_model=list[OuthPersonGet],tags=['Master_Outhperson'])
async def get_outhperson(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         db:Session=Depends(getdb)):
    all_outhperson=db.query(OuthPersonModel).order_by(OuthPersonModel.id.desc()).all()
    return all_outhperson
@router.put('/update_outhperson/{outhperson_id}',response_model=OuthPersonGet,tags=['Master_Outhperson'])
async def update_outhperson(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            outhperson_id:int,outhperson:OuthPersonBase,db:Session=Depends(getdb)):
    outhperson_duplicate=db.query(OuthPersonModel).filter(OuthPersonModel.OuthPerson==outhperson.OuthPerson).first() 
    if outhperson_duplicate:
        raise HTTPException(detail=f'{outhperson.OuthPerson} already exist',status_code=400)
    outhperson_exist=db.query(OuthPersonModel).filter(OuthPersonModel.id==outhperson_id).first()
    if outhperson_exist:
        outhperson_exist.OuthPerson=outhperson.OuthPerson
        db.commit()
        db.refresh(outhperson_exist)
        return outhperson_exist 
    raise HTTPException(detail=f'id-{outhperson_id} does not exist',status_code=400)
@router.delete('/dlt_outhperson/{outhperson_item}',tags=['Master_Outhperson'])
async def dlt_outhperson(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         outhperson_item:int,db:Session=Depends(getdb)):
    outhperson_exit=db.query(OuthPersonModel).filter(OuthPersonModel.id==outhperson_item).first()
    if outhperson_exit:
        db.delete(outhperson_exit)
        db.commit()
        return Response(content=f"id-{outhperson_item} has been deleted successfully",status_code=200)
    raise HTTPException(detail=f' id-{outhperson_item} does not exist',status_code=400)
#---------crime method-----------
@router.post('/create_kalam',response_model=CrimeKalamGet,tags=['Master_Kalam'])
async def create_kalam(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       kalam:CrimeKalamBase,db:Session=Depends(getdb)):
    kalam_exit=db.query(CrimeKalamModel).filter(CrimeKalamModel==kalam.Kalam).first()
    if kalam_exit:
        raise HTTPException(detail=f'{kalam.Kalam} alrady exist',status_code=400)
    kalam_item=CrimeKalamModel(**kalam.model_dump())
    db.add(kalam_item)
    db.commit()
    db.refresh(kalam_item)
    return kalam_item
@router.get('/get_kalam',response_model=list[CrimeKalamGet],tags=['Master_Kalam'])
async def get_kalam(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                    db:Session=Depends(getdb)):
    list_kalam=db.query(CrimeKalamModel).order_by(CrimeKalamModel.id.desc()).all()
    return list_kalam
@router.put('/update_kalam/kalam_id',response_model=CrimeKalamGet,tags=['Master_Kalam'])
async def update_kalam(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       kalam_id:int,kalam:CrimeKalamBase,db:Session=Depends(getdb)):
    kalm_duplicate=db.query(CrimeKalamModel).filter(CrimeKalamModel.Kalam==kalam.Kalam).first()
    if kalm_duplicate:
        raise HTTPException(detail=f'{kalam.Kalam} already exist',status_code=400)
    kalam_exist=db.query(CrimeKalamModel).filter(CrimeKalamModel.id==kalam_id).first()
    if kalam_exist:
        kalam_exist.Kalam=kalam.Kalam
        db.add(kalam_exist)
        db.commit()
        db.refresh(kalam_exist)
        return kalam_exist
    raise HTTPException(detail=f'id-{kalam_id} does not exist',status_code=400)
@router.delete('/dlt_kalam/{kalam_id}',tags=['Master_Kalam'])
async def del_kalam(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                    kalam_id:int,db:Session=Depends(getdb)):
    kalam_exit=db.query(CrimeKalamModel).filter(CrimeKalamModel.id==kalam_id).first()
    if kalam_exit:
          db.delete(kalam_exit)
          db.commit()
          return Response(content=f'id-{kalam_id} has been deleted successfully',status_code=200)
    raise HTTPException(detail=f'id-{kalam_id} does not exist',status_code=400)
#_________designation_api_____________
@router.get('/get_designation',response_model=list[DesignationGet],tags=['Master_Designation'])
async def get_designation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          db:Session=Depends(getdb)):
    designation_list=db.query(DesignationModel).order_by(DesignationModel.id.desc()).all()
    return designation_list
@router.post('/designation_created',response_model=DesignationGet,tags=['Master_Designation'])
async def create_designation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             designation:DesignationBase,db:Session=Depends(getdb)):
    designation_exist=db.query(DesignationModel).filter(DesignationModel.Designation==designation.Designation).first()
    if designation_exist:
        raise HTTPException(detail=f"{designation.Designation} is already exist",status_code=status.HTTP_400_BAD_REQUEST)
    designation_item=DesignationModel(**designation.model_dump())
    db.add(designation_item)
    db.commit()
    db.refresh(designation_item)
    return designation_item
@router.put('/update_designation/{designation_id}',response_model=DesignationGet,tags=['Master_Designation'])
async def update_designation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             designation_id:int,designation:DesignationBase,db:Session=Depends(getdb)):
    designation_duplicate=db.query(DesignationModel).filter(DesignationModel.Designation==designation.Designation).first()
    if designation_duplicate:
        raise HTTPException(detail=f'{designation.Designation} is already exist',status_code=status.HTTP_400_BAD_REQUEST)
    designation_exist=db.query(DesignationModel).filter(DesignationModel.id==designation_id).first()
    if designation_exist:
        designation_exist.Designation=designation.Designation
        db.add(designation_exist)
        db.commit()
        db.refresh(designation_exist)
        return designation_exist
    raise HTTPException(detail=f'id-{designation_id} id does not exist',status_code=status.HTTP_404_NOT_FOUND)
@router.delete('/del_designation/designation_id',tags=['Master_Designation'])
async def del_designation(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          designation_id:int,db:Session=Depends(getdb)):
    designation_exist=db.query(DesignationModel).filter(DesignationModel.id==designation_id).first()
    print(f"Received request to delete designation with ID: {designation_id}")
    if designation_exist:
        print(f"Designation exist: {designation_exist}")
        db.delete(designation_exist)
        db.commit()
        return Response(content=f'id-{designation_id} has been deleted successfully',status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f'id {designation_id} deos not exist',status_code=status.HTTP_404_NOT_FOUND)
#_________create_policestation_logine________
@router.post('/policestation_login',response_model=PoliceLoginGet,tags=["Policestation_Logine"])
async def policestation_logine(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                               police_logine:PoliceLogineBase,db:Session=Depends(getdb)):
    email_exist=db.query(PoliceStationLogineModel).filter(PoliceStationLogineModel.Email==police_logine.Email).first()
    if email_exist:
        raise HTTPException(detail=f"{police_logine.Email} email already exist",status_code=status.HTTP_400_BAD_REQUEST)
    station_exist=db.query(PoliceStationLogineModel).filter(PoliceStationLogineModel.PoliceStation_id==police_logine.PoliceStation_id).first()
    if station_exist:
        raise HTTPException(detail='Police Station already exist',status_code=status.HTTP_400_BAD_REQUEST)
    pwd = get_password_hash(police_logine.Password)
    logine_item=PoliceStationLogineModel(
                                        PoliceStation_id=police_logine.PoliceStation_id,
                                        User_Name=police_logine.User_Name,
                                        Mob_Number=police_logine.Mob_Number,
                                        Email=police_logine.Email,
                                        Designation_id=police_logine.Designation_id,
                                        Password=pwd
                                        )
    db.add(logine_item)
    db.commit()
    db.refresh(logine_item)
    return logine_item
@router.get('/get_station_login',response_model=list[PoliceLoginGet],tags=['Policestation_Logine'])
async def get_station_login(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            db:Session=Depends(getdb)):
    list_policelogin=db.query(PoliceStationLogineModel).order_by(PoliceStationLogineModel.id.desc()).all()
    return list_policelogin
@router.patch('/update_policelogine/{login_id}',response_model=PoliceLoginGet,tags=['Policestation_Logine'])
async def update_policelogin(current_user:Annotated[UserBase,Depends(get_current_user)],
                             login_id:int,
                             police_logine:PoliceLogine_01,db:Session=Depends(getdb)):
    email_exist=db.query(PoliceStationLogineModel).filter(PoliceStationLogineModel.Email==police_logine.Email,PoliceStationLogineModel.id!=login_id).first()
    if email_exist:
        raise HTTPException(detail=f'{police_logine.Email} email already exist',status_code=status.HTTP_400_BAD_REQUEST)
    policestation_exist=db.query(PoliceStationLogineModel).filter(PoliceStationLogineModel.PoliceStation_id==police_logine.PoliceStation_id,PoliceStationLogineModel.id!=login_id).first()
    if policestation_exist:
        raise HTTPException(detail=f'{police_logine.PoliceStation_id} policestation already exist',status_code=status.HTTP_400_BAD_REQUEST)
    user_exist=db.query(PoliceStationLogineModel).filter(PoliceStationLogineModel.id==login_id).first()  
    if user_exist:
        for field, value in police_logine.model_dump(exclude={"Password"},exclude_unset=True).items():
          setattr(user_exist, field, value)
        db.commit()
        db.refresh(user_exist)
        return user_exist 
    raise HTTPException(detail=f'id-{login_id} does not exist',status_code=status.HTTP_404_NOT_FOUND)
@router.delete("/del_stationlog/{station_id}",tags=['Policestation_Logine'])
async def del_stationlog(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         station_id:int,db:Session=Depends(getdb)):
    station_exist=db.query(PoliceStationLogineModel).filter(PoliceStationLogineModel.id==station_id).first()
    if station_exist:
        db.delete(station_exist)
        db.commit()
        return Response(content=f'id-{station_id} station logine  has been deleted successfully',status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f'id-{station_id} does not exist',status_code=status.HTTP_404_NOT_FOUND)
#--------complaint_api---------------------------
     
    
    



        










