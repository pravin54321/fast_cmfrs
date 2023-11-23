from ..dependencies import *
from fastapi import UploadFile, File


StoreImage = "C:/Cluematrix/FaceRecogniationNewProject/Static/Images/"


class imgprocess:
    '''image_processing storing/facedetection/normalisation'''
    file_path = None
    unique_filename=None
    db = db
       
    @classmethod
    async def store_img(cls,images,subdir):
        os.makedirs(StoreImage, exist_ok=True)
        cls.unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{images.filename}"
        cls.file_path = os.path.join(
            f"{StoreImage}{subdir}", cls.unique_filename)
        async with aiofiles.open(cls.file_path, "wb") as f:
            while chunk := await images.read(1024):
                try:
                    await f.write(chunk)
                except Exception as e:
                    print(f"Error while writing the file: {e}")
    @classmethod
    async def facedetection(cls,subdir):
        if cls.file_path is not None:
            time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
            face_image_directory = os.path.join(StoreImage,subdir)
            faces = RetinaFace.extract_faces(img_path=cls.file_path)
            if faces is not None:
                for idx, face in enumerate(faces):
                    resize_face = cv2.resize(face, (300, 400))
                    unique_filename2 = f"{time_stamp}_{idx}.png"
                    cls.file_path = os.path.join(
                        face_image_directory, unique_filename2)
                    face = cv2.cvtColor(resize_face, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(cls.file_path, face)
            else:
                print("face is not detected")
        else:
            print("file_path is none:no image found for face detection")
    @classmethod
    async def facelandmark(cls,subdir):
        if cls.file_path is not None:
            time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
            face_image_directory = os.path.join(StoreImage,subdir)
            try:
                img = cv2.imread(cls.file_path)
                mp_face_mesh = mediapipe.solutions.face_mesh
                face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
                results = face_mesh.process(
                    cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                landmarks = results.multi_face_landmarks[0]
                face_oval = mp_face_mesh.FACEMESH_FACE_OVAL
               
                df = pd.DataFrame(list(face_oval), columns=["p1", "p2"])
                routes_idx = []
                p1 = df.iloc[0]["p1"]
                p2 = df.iloc[0]["p2"]
                for i in range(0, df.shape[0]):
                    obj = df[df["p1"] == p2]
                    p1 = obj["p1"].values[0]
                    p2 = obj["p2"].values[0]
                    route_idx = []
                    route_idx.append(p1)
                    route_idx.append(p2)
                    routes_idx.append(route_idx)
                # for route_idx in routes_idx:
                #      print(f"Draw a line between {route_idx[0]}th landmark point to {route_idx[1]}th landmark point")
                #      pass
                routes = []
                for source_idx, target_idx in routes_idx:
                    source = landmarks.landmark[source_idx]
                    target = landmarks.landmark[target_idx]
                    relative_source = (
                        int(img.shape[1] * source.x), int(img.shape[0] * source.y))
                    relative_target = (
                        int(img.shape[1] * target.x), int(img.shape[0] * target.y))
                    routes.append(relative_source)
                    routes.append(relative_target)
                import numpy as np
                mask = np.zeros((img.shape[0], img.shape[1]))
                mask = cv2.fillConvexPoly(mask, np.array(routes), 1)
                mask = mask.astype(bool)
                out = np.zeros_like(img)
                out[mask] = img[mask]
                unique_filename3 = f"{time_stamp}.png"
                cls.file_path = os.path.join(face_image_directory, unique_filename3)
                cv2.imwrite(cls.file_path, out)
            except Exception as e:
                print(f"Error occurred while processing face : {str(e)}")
        else:
            pass
    @classmethod
    async def embedding(cls,id:str,db):
        if cls.file_path is not None:
           embbeding = DeepFace.represent(img_path=cls.file_path,enforce_detection=False,model_name='Facenet')[0]["embedding"]
           json_embeding = json.dumps(embbeding)
           encoding_data = PersonImgModel(file_path=cls.unique_filename,face_encoding=json_embeding,Person_id=id)
           if id and db is not None:
                db.add(encoding_data)
                db.commit()
                db.refresh(encoding_data)
           else:
               return embbeding     
        else:
            return "face not detected"   
        
class SearchImage:
    '''serach image '''
    def __init__(self,targetemb,db):
        self.targetemb = targetemb
      
        self.db = db
    def findEuclideanDistance(self,source_representation,test_representation):
        euclidean_distance = source_representation - test_representation
        euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
        euclidean_distance = np.sqrt(euclidean_distance)
        return euclidean_distance  
    def findEuclideanDistance_01(self,row):
        source = np.array(row['embedding'])
        target = np.array(row['target'])
        distance = (source - target)
        return np.sqrt(np.sum(np.multiply(distance, distance)))      
  
    async def SingaleImageSearch_01(self):
        '''singale image found in result'''
        jsonDec = json.decoder.JSONDecoder()
        source_data = self.db.query(PersonImgModel).all()
        instances =[]
        target_representation = np.array(self.targetemb)
        for data in source_data:
                source_representetion = jsonDec.decode(data.face_encoding)
                source_representetion = np.array(source_representetion)
                # print(data.face_encoding.dtype)
                distance = self.findEuclideanDistance(source_representetion,target_representation)
                instances.append((distance,data.id))
        result = [min(instances, key=lambda x: x[0])]
        instance = pd.DataFrame(result,columns=['distance','img_id'])
        return instance
          
    async def SingaleImageSearch_02(self):
        jsonDec = json.decoder.JSONDecoder()
        target_representation = np.array(self.targetemb)  
        instances = [(data.Person_id,data.id, jsonDec.decode(data.face_encoding)) for data in self.db.query(PersonImgModel).all()]
        retrive_df = pd.DataFrame(instances,columns=['Pson_Id','img_id','embedding'])
        target_duplicate = np.array([target_representation]*retrive_df.shape[0])
        retrive_df['target'] = target_duplicate.tolist()
        retrive_df['distance'] = retrive_df.apply(self.findEuclideanDistance_01,axis=1)
        retrive_df = retrive_df[retrive_df["distance"]<30]
        retrive_df = retrive_df.sort_values(by=['distance']).reset_index(drop=True)
        retrive_df = retrive_df[['Pson_Id',"img_id",'distance']]
        return retrive_df
    async def FinalResult(self,result):
        data = []
        for index ,instance in result.iterrows():
          
            person = self.db.query(PersonImgModel).filter(PersonImgModel.id==int(instance.img_id)).first()
            if person:
                image_distance = imagedata(
                Person_id = person.Person.id, 
                id=person.id,
                file_path=person.file_path,
                distance=instance.distance,  # Adjust this based on your requirement
                Person={
                    "id":person.Person.id,
                    "Name":person.Person.Name,
                    "Age":person.Person.Age,
                    "Address":person.Person.Address,
                    "Gender":person.Person.Gender,
                    "Mobile_Number":person.Person.Mobile_Number,
                    "Status":person.Person.Status,
                    "Email":person.Person.Email,
                }
            )
                data.append(image_distance)
        return data
    #-----------------------------store_group_face_img--------------------------
       
async def store_groupimg(img_path):
    group_img = db.GroupImageModel(ImgPath=img_path)
    db.add(group_img)
    db.commit()
    db.refresh(group_img)


                     
             


        
                  