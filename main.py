import json
import numpy as np
import boto3
import os

class SimpleLogisticModel:
    def __init__(self):
        self.weights = None
        self.bias = None

    def predict(self, X):
        model = np.dot(X, self.weights) + self.bias
        predictions = self._sigmoid(model)
        return [1 if i > 0.5 else 0 for i in predictions]

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

def load_model():
    s3 = boto3.client('s3')
    bucket_name = os.environ['MODEL_BUCKET']
    model_key = 'cat_dog_model_params.json'
    s3.download_file(bucket_name, model_key, '/tmp/cat_dog_model_params.json')
    
    # Load parameters from JSON
    with open('/tmp/cat_dog_model_params.json', 'r') as f:
        model_params = json.load(f)
    
    # Initialize the model with loaded parameters
    model = SimpleLogisticModel()
    model.weights = np.array(model_params['weights'])
    model.bias = model_params['bias']
    return model

def predict(model, features):
    features = np.array(features, dtype=np.float32).reshape(1, -1)
    prediction = model.predict(features)[0]
    return prediction

# Lambda handler function
def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        features = data['features']
        model = load_model()
        prediction = predict(model, features)

        # Fun response message
        if prediction == 1:
            result = "Dog Lover: You might be the type who’d dress your pet in a cute sweater and bring it on all your outdoor adventures!"
        else:
            result = "Cat Lover: You're probably more into Netflix marathons with a cat on your lap, judging you for binge-watching that third season!"

        return {
            'statusCode': 200,
            'body': json.dumps({'prediction': result})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
