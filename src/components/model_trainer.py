import sys
import os
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV,train_test_split
from src.constants import *
from src.logger import logging
from src.exception import customexception
from src.utils.main_utils import MainUtils


from dataclasses import dataclass

@dataclass
class ModelTrainingConfig:
    artifact_folder = os.path.join(artifact_folder)
    trained_model_path = os.path.join(artifact_folder,"model.pkl")
    expected_accuracy = 0.45
    model_config_file_path = os.path.join('config',"model.yaml")

class ModelTrainer:
    def __init__(self):
        
        self.model_trainer_config = ModelTrainingConfig()

        self.utils = MainUtils()

        self.models = {
                        'XGBClassifier' : XGBClassifier(),
                        'GradientBoostingClassifier':GradientBoostingClassifier(),
                        'RandomForestClassifier':RandomForestClassifier(),
                        'SVC':SVC()

        }
    def evaluate_model(self,x,y,models):
        
        try:
            X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size=0.2,random_state=42)

            report = {}

            for i in range(len(list(models))):
                model = list(models.values())[i]
                model.fit(X_train,Y_train)

                Y_train_pred = model.predict(X_train)

                Y_test_pred = model.predict(X_test)

                train_model_score = accuracy_score(Y_train,Y_train_pred)


                test_model_score = accuracy_score(Y_test,Y_test_pred)

                report[list(models.keys())[i]] = test_model_score
        
            return report
        except Exception as e:
            raise customexception(e,sys) from e
        
    def get_best_model(self,
                       x_train:np.array,
                       x_test:np.array,
                       y_train:np.array,
                       y_test:np.array):
        try:

            model_report :dict = self.evaluate_model(x_train = x_train,
                                                     x_test= x_test,
                                                     y_train = y_test,
                                                     y_test = y_test,
                                                     models=self.models)
            print(model_report)

            best_model_score = max(sorted(model_report.values()))

            #to get best model name from dict

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model_object = self.models[best_model_name]

            return best_model_name,best_model_object,best_model_score
        
        except Exception as e :
            raise customexception(e,sys) from e
        
    def finetune_best_model(self,
                            best_model_object,
                            best_model_name,
                            x_train,
                            y_train) ->object :
        try :

            model_param_grid  = self.utils.read_yaml_file(self.model_trainer_config.model_config_file_path)["model_selection"]["model"][best_model_name]["search_param_grid"]


            grid_search = GridSearchCV(best_model_name,param_grid=model_param_grid,cv=5,verbose=1,n_jobs=-1)

            grid_search.fit(x_train,y_train)

            best_params = grid_search.best_params_

            print("the best params are ",best_params)

            finetuned_model = best_model_object.set_params(**best_params)

            return finetuned_model
        except Exception as e:
            raise customexception(e,sys) from e
    

    def initiate_model_trainer(self,train_array,test_array):

        try:

            logging.info(f"splitting training and testng input and target features")

            x_train,x_test,y_train,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],  
            )

            logging.info(f"extracting model config file path")


            model_report : dict = self.evaluate_model(x=x_train,y = y_train,models=self.models)

            #to get the best model score from dict
            
            best_model_score = max(sorted(model_report.values()))

            #to get the best model name from dict
            
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]


            best_model = self.models[best_model_name]

            best_model = self.finetune_best_model(
                best_model_name=best_model_name,
                best_model_object=best_model,
                x_train=x_train,
                y_train=y_train
            )

            best_model.fit(x_train,y_train)
            y_pred = best_model.predict(x_test)
            best_model_score = accuracy_score(y_test,y_pred)

            print(f"the best model name is {best_model_name} and score {best_model_score}")

            if best_model_score < 0.5 :
                raise Exception("no model is found with an accuracy greater than 0.5 threshold")
            
            logging.info(f"best found model for training and testing dataset")


            logging.info(f"saving model at path {self.model_trainer_config.trained_model_path}")

            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_path),exist_ok=True)

            self.utils.save_object(
                file_path=self.model_trainer_config.trained_model_path,
                obj = best_model
            )

            return self.model_trainer_config.trained_model_path
        

        except Exception as e:
            raise customexception(e,sys) from e