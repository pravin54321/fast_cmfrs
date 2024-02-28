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
#-------------------------info_mode-----------------------------
@router.post('/info_mode',response_model=infomode_BaseGet,tags=['Master_InfoMode'])
async def create_infomode(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          info_mode:Infomode_Base,db:Session=Depends(getdb)):
    infomode_exist=db.query(Infomode_Model).filter(Infomode_Model.Info_Mode==info_mode.Info_Mode).first()
    if infomode_exist:
        raise HTTPException(detail=f'{info_mode.Info_Mode} is already exist',status_code=status.HTTP_400_BAD_REQUEST)
    infomode_item=Infomode_Model(**info_mode.model_dump())
    db.add(infomode_item)
    db.commit()
    db.refresh(infomode_item)
    return infomode_item
@router.get('/get_infomode',response_model=list[infomode_BaseGet],tags=['Master_InfoMode'])
async def get_infomode(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       db:Session=Depends(getdb)):
    list_infomode=db.query(Infomode_Model).order_by(Infomode_Model.id.desc()).all()
    return list_infomode
@router.put('/update_infomode/{infomode_id}',response_model=infomode_BaseGet,tags=['Master_InfoMode'])
async def update_infomode(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          infomode_id:int,info_mode:Infomode_Base,db:Session=Depends(getdb)):
    infomode_duplicate=db.query(Infomode_Model).filter(Infomode_Model.Info_Mode==info_mode.Info_Mode,Infomode_Model.id!=infomode_id).first()
    if infomode_duplicate:
        raise HTTPException(detail=f"{info_mode.Info_Mode} already exist",status_code=status.HTTP_400_BAD_REQUEST)
    infomode_exist=db.query(Infomode_Model).filter(Infomode_Model.id==infomode_id).first()
    if infomode_exist:
        infomode_exist.Info_Mode=info_mode.Info_Mode
        db.commit()
        db.refresh(infomode_exist)
        return infomode_exist
    raise HTTPException(detail=f'{infomode_id} does not exist',status_code=status.HTTP_400_BAD_REQUEST)
@router.delete('/dlt_infomode/{info_id}',tags=['Master_InfoMode'])
async def dlt_infomode(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       info_id:int,db:Session=Depends(getdb)):
    infomode_exist=db.query(Infomode_Model).filter(Infomode_Model.id==info_id).first()
    print(infomode_exist)
    if infomode_exist:
        db.delete(infomode_exist)
        db.commit()
        return Response(content=f"infomode has been deleted successfully",status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f"{info_id} does not exist",status_code=status.HTTP_400_BAD_REQUEST)
#---------------crime_type__________________________
@router.get('/get_crimetype',response_model=list[CrimeType_Get],tags=['Master_CrimeType'])
async def get_crimetype(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                        db:Session=Depends(getdb)):
    list_crimetype=db.query(CrimeMethod_Model).order_by(CrimeMethod_Model.id.desc()).all()
    return list_crimetype
@router.post('/create_crimetype',response_model=CrimeType_Get,tags=['Master_CrimeType'])
async def create_crimetype(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                           crime_type:CrimeType_Base,db:Session=Depends(getdb)):
    crime_exist=db.query(CrimeMethod_Model).filter(CrimeMethod_Model.Crime_Type==crime_type.Crime_Type).first()
    if crime_exist:
        raise HTTPException(detail=f"{crime_type.Crime_Type} already exist",status_code=status.HTTP_400_BAD_REQUEST)
    crimetype_db=CrimeMethod_Model(**crime_type.model_dump())
    db.add(crimetype_db)
    db.commit()
    db.refresh(crimetype_db)
    return crimetype_db
@router.put('/update_crimetype/{crimetype_id}',response_model=CrimeType_Get,tags=['Master_CrimeType'])
async def  update_crimetype(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            crimetype_id:int,crime_type:CrimeType_Base,db:Session=Depends(getdb)):
    duplicate_item=db.query(CrimeMethod_Model).filter(CrimeMethod_Model.Crime_Type==crime_type.Crime_Type,CrimeMethod_Model.id!=crimetype_id).first()
    if duplicate_item:
        raise HTTPException(detail=f"{crime_type.Crime_Type} already exist",status_code=status.HTTP_400_BAD_REQUEST)
    crimetype_item=db.query(CrimeMethod_Model).filter(CrimeMethod_Model.id==crimetype_id).first()
    if crimetype_item is None:
        raise HTTPException(detail=f"id -{crimetype_id} item not fount",status_code=status.HTTP_400_BAD_REQUEST)
    for field,item in crime_type.model_dump(exclude_unset=True).items():
        setattr(crimetype_item,field,item)
    db.commit()
    db.refresh(crimetype_item)    
    return crimetype_item
@router.delete('/dlt_crimetype/{crimety_id}',tags=['Master_CrimeType'])
async def dlt_crimety(
                      crimety_id:int,db:Session=Depends(getdb)):
    db_item=db.query(CrimeMethod_Model).filter(CrimeMethod_Model.id==crimety_id).first()
    if db_item is None:
        raise HTTPException(detail=f"id-{crimety_id} item does not exist",status_code=status.HTTP_400_BAD_REQUEST)
    db.delete(db_item)
    db.commit()
    return Response(content=f"crime_type has been updated successfully",status_code=status.HTTP_200_OK)
    

#_________create_policestation_logine________
@router.post('/policestation_login',response_model=Pstation_loginBase,tags=["Policestation_Logine"])
async def policestation_logine(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                               police_logine:Pstation_loginBase,db:Session=Depends(getdb)):
    email_exist=db.query(UserModel).filter(UserModel.UserEmail==police_logine.UserEmail).first()
    if email_exist:
        raise HTTPException(detail=f"{police_logine.UserEmail} already exist",status_code=status.HTTP_400_BAD_REQUEST)
    hash_password_01= get_password_hash(police_logine.UserPassword)
    setattr(police_logine,'UserPassword',hash_password_01)
    plogine_item=UserModel(**police_logine.model_dump())
    db.add(plogine_item)
    db.commit()
    db.refresh(plogine_item)
    return plogine_item
@router.get('/get_station_login',response_model=list[Pstation_loginBaseGet],tags=['Policestation_Logine'])
async def get_station_login(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            db:Session=Depends(getdb)):
    list_policelogin=db.query(UserModel).filter(UserModel.Role==0).order_by(UserModel.id.desc()).all()
    return list_policelogin
@router.patch('/update_policelogine/{login_id}',response_model=Pstation_loginBase,tags=['Policestation_Logine'])
async def update_policelogin(current_user:Annotated[UserBase,Depends(get_current_user)],
                             login_id:int,
                             police_logine:Pstation_loginBase,db:Session=Depends(getdb)):
    email_exist=db.query(UserModel).filter(UserModel.UserEmail==police_logine.UserEmail,UserModel.id!=login_id).first()
    if email_exist:
        raise HTTPException(detail=f'{police_logine.UserEmail} email already exist',status_code=status.HTTP_400_BAD_REQUEST)
    policestation_exist=db.query(UserModel).filter(UserModel.Pstation_id==police_logine.Pstation_id,UserModel.id!=login_id).first()
    if policestation_exist:
        raise HTTPException(detail=f'{police_logine.Pstation_id} policestation already exist',status_code=status.HTTP_400_BAD_REQUEST)
    user_exist=db.query(UserModel).filter(UserModel.id==login_id).first()  
    if user_exist:
        for field, value in police_logine.model_dump(exclude={"UserPassword"},exclude_unset=True).items():
          setattr(user_exist, field, value)
        db.commit()
        db.refresh(user_exist)
        return user_exist 
    raise HTTPException(detail=f'id-{login_id} does not exist',status_code=status.HTTP_404_NOT_FOUND)
@router.delete("/del_stationlog/{station_id}",tags=['Policestation_Logine'])
async def del_stationlog(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         station_id:int,db:Session=Depends(getdb)):
    station_exist=db.query(UserModel).filter(UserModel.id==station_id).first()
    if station_exist:
        db.delete(station_exist)
        db.commit()
        return Response(content=f'id-{station_id} station logine  has been deleted successfully',status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f'id-{station_id} does not exist',status_code=status.HTTP_404_NOT_FOUND)
#--------complaint_api---------------------------
@router.post('/create_complaint',response_model=ComplaintGet,tags=["Complaint_Api"])
async def create_complaint(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                        complaint:ComplaintBase=Body(...),img_file:UploadFile=File(None),
                        db:Session=Depends(getdb)):
    if img_file:
        file_path=await imagestore(img_file,'complaint/complainant_img')
        setattr(complaint,'Complainant_Imgpath',f"Static/Images/complaint/complainant_img/{file_path}")
    user_id=[current_user.id if current_user.id else None]
    complaint.user_id=user_id[0]
    complaint_item=ComplaintModel(**complaint.model_dump())
    db.add(complaint_item)
    db.commit()
    return complaint_item
@router.get('/get_complaint',response_model=list[ComplaintGet],tags=['Complaint_Api'])
async def get_complaint(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                        db:Session=Depends(getdb)):
    if current_user.Role == 1 or current_user.Role==2:#0 for sp and 2 for admin
           list_complaint=db.query(ComplaintModel).all()
    elif current_user.Role==0:       
           list_complaint=db.query(ComplaintModel).filter(ComplaintModel.user_id==current_user.id).order_by(ComplaintModel.id.desc()).all()
    return list_complaint
@router.get('/get_single_complaint/{complaint_id}',response_model=ComplaintGet,tags=['Complaint_Api'])
async def get_single_complaint(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                               complaint_id:int,db:Session=Depends(getdb)):
    if current_user.Role==1 or current_user.Role==2:
        complaint_item=db.query(ComplaintModel).filter(ComplaintModel.id==complaint_id).first()
        return complaint_item
    elif current_user.Role==0:
        complaint_item=db.query(ComplaintModel).filter(ComplaintModel.id==complaint_id,ComplaintModel.user_id==current_user.id).first()
        return complaint_item

@router.patch('/update_complaint/{complaint_id}',response_model=ComplaintGet,tags=['Complaint_Api'])
async def update_complaint(current_user:Annotated[UserBase,Depends(getdb)],
                           complaint_id:int,
                           complaint:ComplaintBase,db:Session=Depends(getdb)):
    complaint_exist=db.query(ComplaintModel).filter(ComplaintModel.id==complaint_id).first()
    if complaint_exist:
        for field,value in complaint.model_dump(exclude={'Complaint_uid'},exclude_unset=True).items():
          setattr(complaint_exist,field,value)
        db.commit()
        db.refresh(complaint_exist)
        return complaint_exist
    raise HTTPException(detail=f'id-{complaint_id} does not exist',status_code=status.HTTP_404_NOT_FOUND)  
@router.delete('/del/{complaint_id}',tags=['Complaint_Api'])
async def del_complaint(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                        complaint_id:int,db:Session=Depends(getdb)):
    complaint_exist=db.query(ComplaintModel).filter(ComplaintModel.id==complaint_id).first()
    evidance_exist=db.query(ComEvidenceModel).filter(ComEvidenceModel.Complaint_id==complaint_id).all()
    accused_exist=db.query(ComAccused_Model).filter(ComAccused_Model.complaint_id==complaint_id).all()
    witness_exist=db.query(ComWitness_Model).filter(ComWitness_Model.complaint_id==complaint_id).all()
    victime_exist=db.query(ComVictime_Model).filter(ComVictime_Model.complaint_id==complaint_id).all()
    if complaint_exist:
        dlt_evidence=[await dlt_image(evidence.File_Path) for evidence in evidance_exist] if evidance_exist else None
        dlt_accused=[await dlt_image(accused.Accused_Imgpath) for accused in accused_exist] if accused_exist else None
        dlt_witness=[await dlt_image(witness.Witness_Imgpath) for witness in witness_exist] if witness_exist else None
        dlt_victime=[await dlt_image(victime.Victime_Imgpath) for victime in victime_exist] if victime_exist else None
        db.delete(complaint_exist)
        db.commit()
        return Response(content=f'id-{complaint_id} has been deleted successfully',status_code=status.HTTP_200_OK)  
    raise HTTPException(detail=f"id-{complaint_id} does not exist",status_code=status.HTTP_404_NOT_FOUND)  
#_________________________complaint_accused_______________________________
@router.get("/get_comaccused",response_model=list[ComAccused_BaseGet],tags=["Complaint_Accused"]) 
async def get_comaccused(current_user:Annotated[UserBase,Depends(get_current_active_user)],complaint_id:int,
                         db:Session=Depends(getdb)):
    list_comaccused=db.query(ComAccused_Model).filter(ComAccused_Model.complaint_id==complaint_id).order_by(ComAccused_Model.id.desc()).all()
    return(list_comaccused) 
@router.post('/create_comaccused',response_model=ComAccused_BaseGet,tags=['Complaint_Accused'])
async def  create_comaccused(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             com_accused:ComAccused_Base=Body(),image:UploadFile=File(None),db:Session=Depends(getdb)):
    com_accused_duplicate=db.query(ComAccused_Model).filter(ComAccused_Model.Accused_Name==com_accused.Accused_Name,
                                                            ComAccused_Model.complaint_id==com_accused.complaint_id).first()
    if com_accused_duplicate:
        raise HTTPException(detail=f"{com_accused.Accused_Name} alrady have been present this complaint",status_code=status.HTTP_400_BAD_REQUEST)
    if image:
        file_path=await imagestore(image,'complaint/Accused_img')
        setattr(com_accused,'Accused_Imgpath',f"Static/Images/complaint/Accused_img/{file_path}")
    com_accused=ComAccused_Model(**com_accused.model_dump())
    db.add(com_accused)
    db.commit()
    db.refresh(com_accused) 
    return com_accused 
@router.put('/update_comaccused/{comaccused_id}',response_model=ComAccused_BaseGet,tags=['Complaint_Accused']) 
async def update_cimaccused(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            comaccused_id:int,com_accused:ComAccused_Base,db:Session=Depends(getdb)):
    comaccused_item=db.query(ComAccused_Model).filter(ComAccused_Model.id==comaccused_id).first()
    if comaccused_item:
        com_accused_duplicate=db.query(ComAccused_Model).filter(ComAccused_Model.Accused_Name==com_accused.Accused_Name,
                                                                ComAccused_Model.complaint_id==comaccused_item.complaint_id,
                                                                ComAccused_Model.id!=comaccused_id).first()
        if com_accused_duplicate:
            raise HTTPException(detail=f'{com_accused.Accused_Name} already exist',status_code=status.HTTP_400_BAD_REQUEST)
        for field,item in com_accused.model_dump(exclude_unset=True).items():
            setattr(comaccused_item,field,item)
        db.commit()
        db.refresh(comaccused_item)   
        return comaccused_item 
    raise HTTPException(detail=f"{comaccused_id} does not exist",status_code=status.HTTP_400_BAD_REQUEST)
@router.delete('/dlt_com_accused/{com_accused_id}',tags=["Complaint_Accused"])
async def dlt_com_accused(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         com_accused_id:int,db:Session=Depends(getdb)):
    com_accused_item=db.query(ComAccused_Model).filter(ComAccused_Model.id==com_accused_id).first()
    if com_accused_item:
        db.delete(com_accused_item)
        db.commit()
        return Response(content=f"com_accused_item has been deleted successfully",status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f"{com_accused_id} does not exist",status_code=status.HTTP_200_OK)
#----------------complaint_witness----------------------------
@router.get('/get_com_witness',response_model=list[ComWitness_BaseGet],tags=["Complaint_Witness"])
async def get_com_witness(current_user:Annotated[UserBase,Depends(get_current_active_user)],complaint_id:int,
                          db:Session=Depends(getdb)):
    list_com_witness=db.query(ComWitness_Model).filter(ComWitness_Model.complaint_id==complaint_id).order_by(ComWitness_Model.id.desc()).all()
    return list_com_witness
@router.post('/create_com_witness',response_model=ComWitness_BaseGet,tags=["Complaint_Witness"])
async def create_com_witness(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            com_witness:ComWitness_Base=Body(...),image:UploadFile=File(None),
                            db:Session=Depends(getdb)):
    duplicate_witness=db.query(ComWitness_Model).filter(ComWitness_Model.Witness_Name==com_witness.Witness_Name,
                                                        ComWitness_Model.complaint_id==com_witness.complaint_id).first()
    if duplicate_witness:
        raise HTTPException(detail=f"{com_witness.Witness_Name} already present in this complaint",status_code=status.HTTP_400_BAD_REQUEST)
    if image:
        file_path=await imagestore(image,'complaint/Witness_img')
        setattr(com_witness ,'Witness_Imgpath',f"Static/Images/complaint/Witness_img/{file_path}")
    witness_db=ComWitness_Model(**com_witness.model_dump())
    db.add(witness_db)
    db.commit()
    db.refresh(witness_db)
    return witness_db
@router.put('/update_com_witness/{witness_id}',response_model=ComWitness_BaseGet,tags=["Complaint_Witness"])
async def update_com_witness(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                              witness_id:int,com_witness:ComWitness_Base,
                            db:Session=Depends(getdb)):
    dupllicate_witness=db.query(ComWitness_Model).filter(ComWitness_Model.Witness_Name==com_witness.Witness_Name,
                                                         ComWitness_Model.complaint_id==com_witness.complaint_id,
                                                         ComWitness_Model.id!=witness_id).first()
    if dupllicate_witness:
        raise HTTPException(detail=f"{com_witness} already present",status_code=status.HTTP_400_BAD_REQUEST)
    witness_exist=db.query(ComWitness_Model).filter(ComWitness_Model.id==witness_id).first()
    if witness_exist:
        for field,item in com_witness.dict(exclude_unset=True).items():
            setattr(witness_exist,field,item)
            print(f"{field}====>{item}")
        db.commit()
        db.refresh(witness_exist) 
        return witness_exist
    raise HTTPException(detail=f"{witness_id} does not found",status_code=status.HTTP_400_BAD_REQUEST)
@router.delete('/dlt_com_witness/{witness_id}',tags=["Complaint_Witness"])    
async def del_com_complaint(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                            witness_id:int,db:Session=Depends(getdb)):
    com_witness_exist=db.query(ComWitness_Model).filter(ComWitness_Model.id==witness_id).first()
    if com_witness_exist:
        db.delete(com_witness_exist)
        db.commit()
        return Response(content=f"com_witness has been deleted succesfully",status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f'{witness_id} does not exist',status_code=status.HTTP_400_BAD_REQUEST)   
#--------------------------complaint_Victime_--------------------------------------------------
@router.get('/get_victime',response_model=list[ComVictime_BaseGet],tags=['Complaint_Victime'])
async def get_com_victime(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          complaint_id:int,db:Session=Depends(getdb)):
    list_victime=db.query(ComVictime_Model).filter(ComVictime_Model.complaint_id==complaint_id).order_by(ComVictime_Model.id.desc()).all()
    return list_victime
@router.post('/create_com_victime',response_model=ComVictime_BaseGet,tags=['Complaint_Victime'])
async def create_com_victime(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             com_victime:ComVictime_Base,image:UploadFile=File(None),
                             db:Session=Depends(getdb)):
    duplicate_victime=db.query(ComVictime_Model).filter(ComVictime_Model.Victime_Name==com_victime.Victime_Name,
                                                        ComVictime_Model.Victime_Name==com_victime.Victime_Name).first()
    if duplicate_victime:
        raise HTTPException(detail=f"{com_victime.Victime_Name} already exist in this complaint",status_code=status.HTTP_400_BAD_REQUEST) 
    if image:
        img_path=await imagestore(image,'complaint/victime_img')
        setattr(com_victime,'Victime_Imgpath',f"Static/Images/complaint/victime_img/{img_path}")
    victime_db=ComVictime_Model(**com_victime.model_dump())
    db.add(victime_db)
    db.commit()     
    db.refresh(victime_db)
    return victime_db
@router.put('/updadte_com_victime/{victime_id}',response_model=ComVictime_BaseGet,tags=['Complaint_Victime'])
async def update_com_victime(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             victime_id:int,com_victime:ComVictime_Base,db:Session=Depends(getdb)):
    duplicate_victime=db.query(ComVictime_Model).filter(ComVictime_Model.Victime_Name==com_victime.Victime_Name,
                                                        ComVictime_Model.complaint_id==com_victime.complaint_id,
                                                        ComVictime_Model.id!=victime_id).first()
    if duplicate_victime:
        raise HTTPException(detail=f"{com_victime.Victime_Name} already present in this complaint",status_code=status.HTTP_400_BAD_REQUEST)
    victime_exist=db.query(ComVictime_Model).filter(ComVictime_Model.id==victime_id).first()
    if victime_exist:
                for field,item  in com_victime.model_dump(exclude_unset=True).items():
                    setattr(victime_exist,field,item)
                db.commit()
                db.refresh(victime_exist)
                return victime_exist
    raise HTTPException(detail=f"id-{victime_id} does not found",status_code=status.HTTP_400_BAD_REQUEST)  
@router.delete('/del_com_victime/{victime_id}',tags=['Complaint_Victime'])
async def del_com_victime(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          victime_id:int,db:Session=Depends(getdb)):
    victime_exist=db.query(ComVictime_Model).filter(ComVictime_Model.id==victime_id).first()
    if victime_exist:
        db.delete(victime_exist)
        db.commit()
        return Response(content=f"victime has been deleted successfully",status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f"id-{victime_id} does not found",status_code=status.HTTP_400_BAD_REQUEST)
    
#----------------------------evidence_api------------------------
@router.get('/get_evidence/{complaint_id}',response_model=list[ComEvidenceBase],tags=['Complaint_Evidence'])
async def get_evidence(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       complaint_id:int,db:Session=Depends(getdb)):
    list_evidence=db.query(ComEvidenceModel).filter(ComEvidenceModel.Complaint_id==complaint_id).order_by(ComEvidenceModel.id.desc()).all()
    return list_evidence 
@router.post("/evidence_create",response_model=ComplaintGet,tags=['Complaint_Evidence'])
async def evidence_cretae(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          complaint_id:int=Form(...),
                          evidence: list[UploadFile] = File(None),db:Session=Depends(getdb)):
    complaint_exist=db.query(ComplaintModel).filter(ComplaintModel.id==complaint_id).first()
    if complaint_exist: 
        if evidence:
            for image in evidence:
                file_type=image.content_type
                file_path=await imagestore(image,'complaint/evidence_img')
                evidence_db=ComEvidenceModel(File_Path=f'Static/Images/complaint/evidence_img/{file_path}',File_Type=file_type,Complaint_id=complaint_id)
                db.add(evidence_db)
            db.commit()
            db.refresh(evidence_db)
            return complaint_exist
    raise HTTPException(detail=f"complaint id {complaint_id} does not  exist",status_code=status.HTTP_400_BAD_REQUEST)
@router.put('/update_evidence/{evidence_id}',tags=['Complaint_Evidence'])
async def update_evidence(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          evidence_id:int,evidence:UploadFile=File(...),
                          db:Session=Depends(getdb)):
    evidence_exist=db.query(ComEvidenceModel).filter(ComEvidenceModel.id==evidence_id).first()
    if evidence_exist:
        delete_image=await dlt_image(evidence_exist.File_Path)
        file_path=await imagestore(evidence,'complaint/evidence_img')
        file_type=evidence.content_type
        evidence_exist.Complaint_id=evidence_exist.Complaint_id
        evidence_exist.File_Path=f'Static/Images/complaint/evidence_img/{file_path}'
        evidence_exist.File_Type=file_type
        db.commit()
        db.refresh(evidence_exist)
        return evidence_exist
    raise HTTPException(detail=f"id-{evidence_id} does not exist",status_code=status.HTTP_404_NOT_FOUND)
@router.delete('/dlt_evidence/{evidence_id}',tags=['Complaint_Evidence'])
async def del_evidence(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       evidence_id:int,db:Session=Depends(getdb)):
    evidence_exist=db.query(ComEvidenceModel).filter(ComEvidenceModel.id==evidence_id).first()
    if evidence_exist:
        delete_img=await dlt_image(evidence_exist.File_Path)
        db.delete(evidence_exist)
        db.commit()
        return Response(content=f'id-{evidence_id} has been delete successfully',status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f'id-{evidence_id} does not exist',status_code=status.HTTP_404_NOT_FOUND)
#--------------------------Ncr-------------------------------
@router.get('/get_ncr',response_model=list[NCRBaseGet],tags=['NCR_API'])
async def get_ncr(current_user:Annotated[UserBase,Depends(get_current_active_user)],db:Session=Depends(getdb)):
    list_ncr=db.query(NCRModel).filter(NCRModel.user_id==current_user.id).order_by(NCRModel.id.desc()).all()
    return list_ncr
@router.post('/create_ncr_from_complaint/{complaint_id}',response_model=NCRBaseGet,tags=['NCR_API'])
async def create_ncr_from_complaint(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                                    complaint_id:int,db:Session=Depends(getdb)):
    complaint_exist=db.query(ComplaintModel).filter(ComplaintModel.id==complaint_id).first()
    if complaint_exist:
        ncr_db=NCRModel(police_station_id=complaint_exist.Station_id,Complaint_id=complaint_exist.id,
                        info_recive=complaint_exist.Complaint_Date,Occurrence_Date_Time=complaint_exist.Occurance_date_time,
                        Place_Occurrence=complaint_exist.Place_Occurance,Name_Complainant=complaint_exist.Complainant_Name,
                        Complainant_Mob_Number=complaint_exist.Mob_Number,Complainant_Age=complaint_exist.Complainant_Age,
                        Complainant_imgpath=complaint_exist.Complainant_Imgpath,Complainant_Description=complaint_exist.Complaint_Desc,
                        complaint_or_Ncr=0,user_id=current_user.id)
        db.add(ncr_db)
        db.commit()
        db.refresh(complaint_exist)
        if ncr_db.id:
            ncr_address_db=Complainat_AddressModel(NCR_id=ncr_db.id,Address=complaint_exist.Address)
            db.add(ncr_address_db)
            db.commit()
            complaint_accused_exist=db.query(ComAccused_Model).filter(ComAccused_Model.complaint_id==complaint_id).all()
            if complaint_accused_exist:
                for accused in complaint_accused_exist:
                    ncr_accused_db=AccusedModel(NCR_id=ncr_db.id,Name=accused.Accused_Name
                                                ,Age=accused.Accused_Age,image_path=accused.Accused_Imgpath)
                    db.add(ncr_accused_db)
                    db.commit()
                    ncr_accused_address=Accused_AddressModel(Accused_id=ncr_accused_db.id,
                                                             Address=accused.Accused_Address)
                    db.add(ncr_accused_address)
                db.commit()
            return ncr_db   
            
@router.post('/create_ncr',response_model=NCRBaseGet,tags=['NCR_API'])
async def create_ncr(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                     ncr:NCRBase,address_schema:Com_address_Schema,image:UploadFile=File(),db:Session=Depends((getdb))):
    user_id=[current_user.id if current_user.id else None]
    ncr.user_id=user_id[0]
    file_path=await imagestore(image,'ncr/complainant_img')
    setattr(ncr,'Complainant_imgpath',f"Static/Images/ncr/complainant_img/{file_path}")
    ncr_item=NCRModel(**ncr.model_dump())
    db.add(ncr_item)
    db.commit()
    if ncr_item.id:
        address_data=[{
            "Address_Type": comp_address.Address_Type,
            "Address": comp_address.Address,
            "NCR_id": ncr_item.id
        } for comp_address in address_schema.com_address
        ]
        address_instance=[Complainat_AddressModel(**data) for data in address_data]
        print(address_instance)
        db.add_all(address_instance)
        db.commit()
        return ncr_item
    return Response(content=f"warning:{ncr.Name_Complainant} address does not add",status_code=status.HTTP_200_OK)
@router.put('/update_ncr/{ncr_id}',response_model=NCRBaseGet,tags=['NCR_API'])
def update_ncr(current_user:Annotated[UserBase,Depends(get_current_active_user)],
               ncr_id:int,ncr_item:NCRBase,comp_addresses:list[CompAddressBase],
               db:Session=Depends(getdb)):
    ncr_exist=db.query(NCRModel).filter(NCRModel.id==ncr_id).first()
    if ncr_exist:
            if ncr_exist:
                for field ,value in ncr_item.model_dump(exclude_unset=True).items():
                    setattr(ncr_exist,field,value)
                db.commit()
                comp_address_exist=db.query(Complainat_AddressModel).filter(Complainat_AddressModel.NCR_id==ncr_id).all()    
                if comp_address_exist:
                    [db.delete(dlt_address) for dlt_address in comp_address_exist]
                    db.commit()
                address_data=[{
                     "Address_Type": address.Address_Type,
                      "Address": address.Address,
                      "NCR_id":ncr_id
                } for address in comp_addresses]  
                address_instance=[Complainat_AddressModel(**data) for data in address_data]
                db.add_all(address_instance)
                db.commit()
                # db.refresh(ncr_exist)  
                return ncr_exist
    raise HTTPException(detail=f'{ncr_id} does not exist',status_code=status.HTTP_404_NOT_FOUND)
@router.delete('/del_ncr/{ncr_id}',tags=['NCR_API'])
async def del_ncr(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                  ncr_id:int,db:Session=Depends(getdb)):
    ncr_exist=db.query(NCRModel).filter(NCRModel.id==ncr_id).first()
    if ncr_exist:
        db.delete(ncr_exist)
        db.commit()
        return Response(content=f'id-{ncr_id} has been deleted successfully',status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f'id-{ncr_id} does not exist',status_code=status.HTTP_404_NOT_FOUND)
#_____________ncr_accuse_________________________________________
@router.get('/get_ncr_accused',response_model=list[AccusedBaseGet],tags=['NCR_Accused'])
async def get_ncr_accused(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          db:Session=Depends(getdb)):
    list_accused=db.query(AccusedModel).all()
    return list_accused
@router.post('/create_ncr_accused/',response_model=NCRBaseGet,tags=['NCR_Accused'])
async def create_ncr_accused(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             accused_shema:AccusedBase,image:UploadFile=File(None),
                             db:Session=Depends(getdb)):
    ncr_exist=db.query(NCRModel).filter(NCRModel.id==accused_shema.NCR_id).first()
    if ncr_exist:
            image_path=await imagestore(image,'ncr/accused_img')
            accused_data=AccusedModel(Name=accused_shema.Name,
                                      Father_Name=accused_shema.Father_Name,
                                      Aliase_Name=accused_shema.Aliase_Name,
                                      DOB=accused_shema.DOB,
                                      Mobile_Number=accused_shema.Mobile_Number,
                                      Accused_Description=accused_shema.Accused_Description,
                                      Age=accused_shema.Age,
                                      image_path=f"Static/Images/ncr/accused_img/{image_path}",
                                      NCR_id=accused_shema.NCR_id)
            db.add(accused_data)
            db.commit()
            if accused_data.id:
                accused_address=[{
                    "Address_Type":address.Address_Type,
                    "Address":address.Address,
                    "Accused_id":accused_data.id
                } for address in accused_shema.Addresses]
                address_instance=[Accused_AddressModel(**data) for data in accused_address]
                db.add_all(address_instance)
                db.commit()
                return ncr_exist
            return Response(content=f"warning:{accused_shema.Name} address not add",status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f"id-{accused_shema.NCR_id} ncr_item does not exist",status_code=status.HTTP_400_BAD_REQUEST)
@router.put('/update_ncr_accused/{accused_id}',response_model=AccusedBaseGet,tags=['NCR_Accused'])
async  def update_ncr_accused(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                              accused_id:int,accused_shema:AccusedBase,db:Session=Depends(getdb)):
    accused_exist=db.query(AccusedModel).filter(AccusedModel.id==accused_id).first()
    if accused_exist:
        accused_exist.NCR_id=accused_shema.NCR_id
        accused_exist.Name=accused_shema.Name
        accused_exist.Father_Name=accused_shema.Father_Name
        accused_exist.Age=accused_shema.Age
        db.commit()
        accused_address_exist=db.query(Accused_AddressModel).filter(Accused_AddressModel.Accused_id==accused_id).all()
        if accused_address_exist:
            [db.delete(del_address) for del_address in accused_address_exist]
            db.commit()  # Execute the deletion and commit the transaction
        accused_address=[{
                    "Address_Type":address.Address_Type,
                     "Address":address.Address,
                    "Accused_id":accused_id
                } for address in accused_shema.Addresses]
        address_instance=[Accused_AddressModel(**data) for data in accused_address]
        db.add_all(address_instance)
        db.commit()
        return accused_exist
    raise HTTPException(detail=f"id-{accused_id}:accused does not found",status_code=status.HTTP_400_BAD_REQUEST)

@router.delete('/dlt_ncr_accused/{accused_id}',tags=['NCR_Accused'])
async def dlt_ncr_accused(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          accused_id:int,db:Session=Depends(getdb)):
    accused_exist=db.query(AccusedModel).filter(AccusedModel.id==accused_id).first()
    if accused_exist:
        await dlt_image(accused_exist.image_path)
        db.delete(accused_exist)
        db.commit()
        return Response(content=f"accused has been deleted successfully",status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f"id-{accused_id} accuseed item does not exist",status_code=status.HTTP_400_BAD_REQUEST)
#-------------ncr_act_____
@router.post('/create_ncr_act/{accused_id}',response_model=AccusedBaseGet,tags=['NCR_Act'])
async def create_ncr_act(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         accused_id:int,act_item:list[NCR_ACTBase],db:Session=Depends(getdb)):
    ncr_exist=db.query(AccusedModel).filter(AccusedModel.id==accused_id).first()
    if ncr_exist:
        act_data=[{
            "accused_id":accused_id,
            "Act_id": actItem.Act_id,
            "Section": json.dumps(actItem.Section)} for actItem in act_item]
        actInstance=[NCR_ACTModel(**data) for data in act_data]
        db.add_all(actInstance)
        db.commit()
        return ncr_exist   
    raise HTTPException(detail=f"id-{accused_id} accused item does not eist",status_code=status.http400)
@router.put('/update_ncr_act/{ncr_act_id}',response_model=AccusedBaseGet,tags=['NCR_Act'])
async def update_ncr_act(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         ncr_act_id:int,actSchema:ncr_Actupdate,db:Session=Depends(getdb)):
    act_exist=db.query(NCR_ACTModel).filter(NCR_ACTModel.id==ncr_act_id).first()
    if act_exist:
        accused_exist=db.query(AccusedModel).filter(AccusedModel.id==actSchema.accused_id).first()
        if accused_exist:
            act_exist.Act_id=actSchema.Act_id
            act_exist.accused_id=actSchema.accused_id
            act_exist.Section=json.dumps(actSchema.Section)
            db.commit()
            db.refresh(accused_exist)
            return accused_exist
        raise HTTPException(detail=f"id-{actSchema.accused_id} accused does not found",status_code=status.HTTP_400_BAD_REQUEST)
    raise HTTPException(detail=f"id-{ncr_act_id} ncr_act not found",status_code=status.HTTP_400_BAD_REQUEST)
@router.delete('/delete_ncr_act/{act_id}',tags=['NCR_Act'])
async def delete_ncr_act(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         act_id:int,db:Session=Depends(getdb)):
    act_exist=db.query(NCR_ACTModel).filter(NCR_ACTModel.id==act_id).first()
    if act_exist:
        db.delete(act_exist)
        db.commit()
        return Response(content="act item has been deleted successfully",status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f"id-{act_id} act item does not exist",status_code=status.HTTP_400_BAD_REQUEST)
        
    

    

   
#-----------------------------fir_api-------------------------------------------------------------
@router.get('/get_fir',response_model=list[FirBaseGet],tags=['FIR_API'])
async def get_fir(current_user:Annotated[UserBase,Depends(get_current_active_user)],db:Session=Depends(getdb)):
    list_fir=db.query(FIRModel).filter(FIRModel.user_id==current_user.id).order_by(FIRModel.id.desc()).all()
    return list_fir
@router.post('/create_fir',response_model=FirBaseGet,tags=['FIR_API'])
async def create_fir(current_user:Annotated[UserBase,Depends(get_current_user)],
                     fir_item:FirBase,fir_acts:list[Fir_ActBase],db:Session=Depends(getdb)):
    user_id=[current_user.id if current_user.id else None]
    fir_item.user_id=user_id[0]
    fir_db=FIRModel(**fir_item.model_dump())
    db.add(fir_db)
    db.commit()
    if fir_db.id:
        for fir_act in fir_acts:
            act_db=FirSectionActModel(Fir_id=fir_db.id,Fir_Act=fir_act.Fir_Act,Fir_Section=fir_act.Fir_Section)
            db.add(act_db)
        db.commit()    
    db.refresh(fir_db)
    return fir_db
@router.patch('/update_fir/fir_id',response_model=FirBase,tags=['FIR_API'])
async def update_fir(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                     fir_id:int,fir_item:FirBase,fir_acts:list[Fir_ActBase],
                     db:Session=Depends(getdb)):
    fir_exist=db.query(FIRModel).filter(FIRModel.id==fir_id).first()  
    if fir_exist:
        for field,value in fir_item.model_dump(exclude={"Fir_No"},exclude_unset=True).items():
            setattr(fir_exist,field,value)
        db.commit()
        fir_act_exist=db.query(FirSectionActModel).filter(FirSectionActModel.Fir_id==fir_id).all()
        if fir_act_exist:
                for fir_act in fir_act_exist:
                    db.delete(fir_act)
                    db.commit()
        for  fir_act in fir_acts:    
              fir_act_db=FirSectionActModel(Fir_id=fir_id,Fir_Act=fir_act.Fir_Act,Fir_Section=fir_act.Fir_Section)
              db.add(fir_act_db)
        db.commit()
        return fir_exist 
    raise HTTPException(detail=f'id-{fir_id} does not exist',status_code=status.HTTP_400_BAD_REQUEST) 
@router.delete('/dlt_fir/{fir_id}',tags=['FIR_API'])
async def dlt_fir(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                  fir_id:int,db:Session=Depends(getdb)):
                 fir_exist=db.query(FIRModel).filter(FIRModel.id==fir_id).first()
                 if fir_exist:
                     db.delete(fir_exist)
                     db.commit()
                     return Response(content=f'id-{fir_id} has been deleted successfully',status_code=status.HTTP_200_OK) 
                 raise HTTPException(detail=f"id-{fir_id} does not exist",status_code=status.HTTP_400_BAD_REQUEST)            

#------------charge_sheet__form---------------------
@router.get('/get_chargesheet',response_model=list[ChargeSheetBaseGet],tags=['ChargeSheet_Api'])
async def get_chargesheet(current_user:Annotated[UserBase,Depends(get_current_active_user)],db:Session=Depends(getdb)):
    list_chargesheet=db.query(ChargeSheetModel).filter(ChargeSheetModel.user_id==current_user.id).order_by(ChargeSheetModel.id.desc())
    return list_chargesheet
@router.post('/create_chargesheet',response_model=ChargeSheetBaseGet,tags=['ChargeSheet_Api'])
async def create_chargesheet(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             charge_sheet:ChargeSheetBase,chargesheet_act:list[ChargeSheet_ActBase],db:Session=Depends(getdb)):
    user_id=[current_user.id if current_user.id else None]
    charge_sheet.user_id=user_id[0]
    chargesheet_item=ChargeSheetModel(**charge_sheet.model_dump())
    db.add(chargesheet_item)
    db.commit()
    if chargesheet_item.id:
        for sheet_act in  chargesheet_act:
            chargesheet_act_db=ChargeSheet_ActModel(ChargeSheet_id=chargesheet_item.id,ChargeSheet_Act=sheet_act.ChargeSheet_Act,
                                                    ChargeSheet_Section=sheet_act.ChargeSheet_Section)
            db.add(chargesheet_act_db)
        db.commit()     
    db.refresh(chargesheet_item) 
    return chargesheet_item     

@router.patch('/update_chargesheet/{charge_sheet_id}',response_model=ChargeSheetBase,tags=['ChargeSheet_Api'])
async def update_chargesheet(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                             charge_sheet_id:int,charge_sheet:ChargeSheetBase,chargesheet_act:list[ChargeSheet_ActBase],
                             db:Session=Depends(getdb)):
    charegsheet_exist=db.query(ChargeSheetModel).filter(ChargeSheetModel.id==charge_sheet_id).first()
    if charegsheet_exist:
        for field,value in charge_sheet.model_dump(exclude={"ChargeSheet_No"},exclude_unset=True).items():
            setattr(charegsheet_exist,field,value)
        db.commit()
        chargesheet_act_exist=db.query(ChargeSheet_ActModel).filter(ChargeSheet_ActModel.ChargeSheet_id==charge_sheet_id).all()
        if chargesheet_act_exist:
            for sheet_act in chargesheet_act_exist:
                db.delete(sheet_act)
            db.commit()
            for act in chargesheet_act:
                act_db=ChargeSheet_ActModel(ChargeSheet_id=charegsheet_exist.id,ChargeSheet_Act=act.ChargeSheet_Act,ChargeSheet_Section=act.ChargeSheet_Section)
                db.add(act_db)
            db.commit() 
        return charegsheet_exist     
@router.delete('/dlt_chargesheet/{sheet_id}',tags=['ChargeSheet_Api'])
async def dlt_chargesheet(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                          sheet_id:int,db:Session=Depends(getdb)):
         charge_sheet_exist=db.query(ChargeSheetModel).filter(ChargeSheetModel.id==sheet_id).first()
         if charge_sheet_exist:
             db.delete(charge_sheet_exist)
             db.commit()
             return Response(content=f'id-{sheet_id} has been deleted successfully',status_code=status.HTTP_200_OK) 
         raise HTTPException(detail=f'{sheet_id} does not exist',status_code=status.HTTP_400_BAD_REQUEST) 
#_____________________inquiry_form_____________________________
@router.get('/get_enqform',response_model=list[EnquiryNamunaBaseGet],tags=['Enquiry_Api'])
async def enqform(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                                         db:Session=Depends(getdb)):
    list_enqform=db.query(EnquiryFormModel).filter(EnquiryFormModel.user_id==current_user.id).order_by(EnquiryFormModel.id.desc()).all()
    return list_enqform
@router.post('/create_inquiry_namuna',response_model=EnquiryNamunaBaseGet,tags=['Enquiry_Api'])
async def create_inquiry_form(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                              file:UploadFile=File(None),
                              enquiry_form:EnquiryNamunaBase=Depends(),
                              db:Session=Depends(getdb)):
   
    file_path=await imagestore(file,'namuna_form')
    setattr(enquiry_form,'Image_Path',file_path)
    user_id=[current_user.id if current_user.id else None]
    EnquiryNamunaBase.user_id=user_id[0]
    Enquiry_form_item=EnquiryFormModel(**enquiry_form.model_dump())
    db.add(Enquiry_form_item) 
    db.commit()
    db.refresh(Enquiry_form_item)
    return Enquiry_form_item
@router.patch('/update_enqform/{enqform_id}',response_model=EnquiryNamunaBase,tags=['Enquiry_Api'])
async def update_enqform(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                         enqform_id:int,enq_form:EnquiryNamunaBaseGet,db:Session=Depends(getdb)):
    enqform_exist=db.query(EnquiryFormModel).filter(EnquiryFormModel.id==enqform_id).first()
    if enqform_exist:
        for field,value in enq_form.model_dump(exclude={'Image_Path'},exclude_unset=True).items():
             setattr(enqform_exist,field,value) 
        db.commit()
        db.refresh(enqform_exist)
        return enqform_exist
    raise HTTPException(detail=f'id-{enqform_id} does not exist',status_code=status.HTTP_400_BAD_REQUEST)
@router.delete('/dlt_enqform/{enqform_id}',tags=['Enquiry_Api']) 
async def del_enqform(curremt_user:Annotated[UserBase,Depends(get_current_active_user)],
                      enqform_id:int,db:Session=Depends(getdb)):
    enqform_exist=db.query(EnquiryFormModel).filter(EnquiryFormModel.id==enqform_id).first()
    if enqform_exist:
        db.delete(enqform_exist)
        db.commit()
        return Response(content=f"id-{enqform_id} has  been deleted successfully",status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f"id-{enqform_id} does not exist",status_code=status.HTTP_400_BAD_REQUEST) 
@router.put('/update_image/{enqform_id}',tags=['Enquiry_Api'])
async def update_img(current_user:Annotated[UserBase,Depends(get_current_active_user)],enqform_id:int,
                     file:UploadFile=File(...),
                     db:Session=Depends(getdb)):
    file_path=await imagestore(file,'namuna_form')
    enqform_exist=db.query(EnquiryFormModel).filter(EnquiryFormModel.id==enqform_id).update({'Image_Path':file_path})
    db.commit()
    if enqform_exist is 1:
      return Response(content="image has been change successfully",status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f"id-{enqform_id} does not exist",status_code=status.HTTP_400_BAD_REQUEST)
#_______________yellow_card____________________
@router.get('/get_ycard',response_model=list[Yellow_CardBaseGet],tags=['Yellow_Card_Api'])
async def get_ycard(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                    db:Session=Depends(getdb)):
    list_yellowcard=db.query(YellowCardModel).filter(YellowCardModel.user_id==current_user.id).order_by(YellowCardModel.id.desc()).all()
    return list_yellowcard
@router.post('/create_yellow_card',response_model=Yellow_CardBase,tags=['Yellow_Card_Api'])
async def create_yellowcard(current_user:Annotated[UserBase,Depends(get_current_user)],
                           yellow_card:Yellow_CardBase=Depends(),file:UploadFile=File(None),db:Session=Depends(getdb)):
    file_path=await imagestore(file,'yellow_card')
    setattr(yellow_card,'Accused_ImgPath',file_path)
    user_id=current_user.id
    yellow_card.user_id=user_id
    yellow_card_item=YellowCardModel(**yellow_card.model_dump())
    db.add(yellow_card_item)
    db.commit()
    db.refresh(yellow_card_item)
    return yellow_card_item
@router.patch('/update_yellow_card/{ycard_id}',response_model=Yellow_CardBase,tags=['Yellow_Card_Api'])
async def update_ycard(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                       ycard_id:int,yellow_card:Yellow_CardBase,db:Session=Depends(getdb)):
    yellow_card_exist=db.query(YellowCardModel).filter(YellowCardModel.id==ycard_id).first()
    if yellow_card_exist:
        for field,value in yellow_card.model_dump(exclude={'Accused_ImgPath'},exclude_unset=True).items():
            setattr(yellow_card_exist,field,value)
        db.commit()
        db.refresh(yellow_card_exist)
        return yellow_card_exist 
@router.delete('/del_ycard/{ycard_id}',tags=['Yellow_Card_Api']) 
async def del_ycard(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                    ycard_id:int,db:Session=Depends(getdb)):
      ycard_exist=db.query(YellowCardModel).filter(YellowCardModel.id==ycard_id).first()
      if ycard_exist:
          db.delete(ycard_exist)
          db.commit()
          return Response(content=f"id-{ycard_id} has been deleted successfully",status_code=status.HTTP_200_OK)
      raise HTTPException(detail=f"id-{ycard_id} does not exist",status_code=status.HTTP_400_BAD_REQUEST)   

@router.patch('/upd_ycard_img/{ycard_id}',response_model=Yellow_CardBase,tags=['Yellow_Card_Api'])
async def upd_ycard_img(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                        ycard_id:int,file:UploadFile=File(),db:Session=Depends(getdb)):
    file_path=await imagestore(file,'yellow_card')
    ycard_exist=db.query(YellowCardModel).filter(YellowCardModel.id==ycard_id).update({'Accused_ImgPath':file_path})
    if ycard_exist is 1:
        return Response(content='image has been update successfully',status_code=status.HTTP_200_OK)
    raise HTTPException(detail=f"id-{ycard_id} does not exist",status_code=status.HTTP_400_BAD_REQUEST)
@router.post('/test_form')
def submit(user_review:Rate=Body(), image:list[Any] = None):
        for i in user_review.id1:
            print(i.name)
            print(image)
        return {"JSON Payload ": user_review, "Image": image.filename}
   

    



        










