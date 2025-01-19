from flask import Flask , render_template ,jsonify,request,send_file
from src.exception import customexception
from src.logger import logging
import os,sys

from src.pipelines.train_pipeline import TrainedPipeline
from src.pipelines.predict_pipeline import PredictionPipeline

app = Flask(__name__)


@app.route("/")
def home():
    return "welcome to my application"

@app.route("/train")
def train_route():
    try:

        train_pipeline = TrainedPipeline()
        train_pipeline.run_pipeline()

        return "training completed"
    except Exception as e:
        raise customexception(e,sys)
    
@app.route("/predict",methods =['POST','GET'])
def upload():
    try:

        if request.method == 'POST':
            #object of prediction pipeline 
            prediction_pipeline = PredictionPipeline(request)

            #run the pipeline using object 
            prediction_file_details = prediction_pipeline.run_pipeline()

            logging.info("prediction completed downloading prediction file")

            return send_file(prediction_file_details.prediction_file_path,
                             download_name=prediction_file_details.prediction_file_name,
                             as_attachment=True)
        

        else:
            return render_template('upload_file.html')
            
    except Exception as e:
        raise customexception(e,sys)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)