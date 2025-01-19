import sys
import os
 
from src.components.data_ingestion import dataIngestion
from src.components.data_transformation import DataTransformatin
from src.components.model_trainer import ModelTrainer

from src.exception import customexception

class TrainedPipeline :

    def start_data_ingestion(self):

        try:
            data_ingestion = dataIngestion()
            feature_stored_file_path = data_ingestion.initiate_data_ingestion()
            return feature_stored_file_path
        except Exception as e:
            raise customexception(e,sys)





    def start_data_transformation(self,feature_stored_file_path):

        try:
            data_transformation = DataTransformatin(feature_stored_file_path)
            train_arr,test_arr,preprocessor_path = data_transformation.initiate_data_transformation()
            return train_arr,test_arr,preprocessor_path
        except Exception as e:
            raise customexception(e,sys)



    def start_model_training(self,train_arr,test_arr):
        try:
            model_trainer = ModelTrainer()
            accuraccy_score = model_trainer.initiate_model_trainer(train_arr,test_arr)
            return accuraccy_score
        except Exception as e:
            raise customexception(e,sys)
        
    def run_pipeline(self):
        try:
            feature_stored_file_path = self.start_data_ingestion()
            train_arr,test_arr,preprocessor_path = self.start_data_transformation(feature_stored_file_path)
            accuraccy_score = self.start_model_training(train_arr,test_arr)

            print("training completed with an accuracy of",accuraccy_score)
        except Exception as e:
            raise customexception(e,sys)

    
