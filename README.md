# TA8-BadDataBusters-ML-Model-Deployement - Dog vs. Cat Lover Predictor 🐶🐱

This repository contains a fun and lightweight machine learning project designed to predict whether a person is a Dog Lover or a Cat Lover based on simple personality features. The predictor is deployed on AWS Lambda for scalability and cost-efficiency, with model parameters stored in AWS S3.

**Medium Article Link:** https://medium.com/@akhilxox/deploying-the-ultimate-dog-vs-384bc7a920ed

## Project Overview 📋

This project leverages a logistic regression model trained on mock data to classify users as either Dog Lovers or Cat Lovers. The model uses simple features and deploys serverlessly with AWS Lambda, pulling model parameters from AWS S3.

---

## File Structure 📂

| File/Folder               | Description                                                                                          |
|---------------------------|------------------------------------------------------------------------------------------------------|
| `model/training.py`       | Contains code to train the logistic regression model and save its parameters.                        |
| `model/cat_dog_model_params.json` | JSON file with saved model parameters (weights and bias) for deployment.                 |
| `main.py`                 | Lambda function code that loads model parameters, makes predictions, and returns results.            |
| `requirements.txt`        | Lists dependencies needed for Lambda (minimal setup with numpy and boto3).                          |
| `serverless.yml`          | Configuration file for Serverless Framework to deploy on AWS Lambda and configure environment.       |

---

## Requirements 📝

To set up and deploy this project, you’ll need the following:

- **AWS CLI** - For AWS configuration
- **Python 3.8** - Lambda-compatible Python version
- **Serverless Framework** - For deploying Lambda functions

---

## Step-by-Step Guide 🛠️

### 1. AWS Setup: Installing and Configuring AWS CLI

Install the AWS CLI:

```bash
curl -s "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

Configure the AWS CLI with your credentials and region:

```bash
aws configure
```

Input your AWS Access Key ID, Secret Access Key, and Default Region (e.g., us-east-1). Set the region permanently:

```bash
echo 'export AWS_DEFAULT_REGION="us-east-1"' >> ~/.bashrc
source ~/.bashrc
```

### 2. Training the Model (in model/training.py)
In this step, we define a lightweight logistic regression model to classify users based on the following mock features:

| Feature                   | Description                                               |
|---------------------------|-----------------------------------------------------------|
| Coffee Cups per Day       | Assumes high caffeine = dog owner.                        |
| Netflix Hours per Week    | Assumes high binge time = more relaxed, like a cat.       |
| Favorite Vacation Type    | Adventurers prefer dogs; loungers prefer cats.            |
| Social Media Accounts     | High social presence suggests dog lover.                  |
| Willingness to Dress Pets | Cats resist, dogs tolerate.                               |

Run the code in training.py. This will create a .json file.

### 3. Saving Model Parameters to AWS S3
After training, save the model parameters to S3 so they can be accessed by Lambda during runtime.

Upload the JSON file to S3:

```bash
aws s3 cp model/cat_dog_model_params.json s3://your-bucket-name/
```

### 4. Configuring Serverless Framework

Install Serverless Framework
```bash
npm install -g serverless
```

Configure serverless.yml: 

This file sets up the Lambda function, specifying permissions and dependencies.

```bash
service: cat-dog-lover-predictor

provider:
  name: aws
  runtime: python3.8
  region: us-east-1
  environment:
    MODEL_BUCKET: your-bucket-name
  iamRoleStatements:
    - Effect: "Allow"
      Action:
        - "s3:GetObject"
      Resource:
        - "arn:aws:s3:::your-bucket-name/*"

functions:
  predictor:
    handler: main.lambda_handler
    events:
      - http:
          path: predict
          method: post

plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    dockerizePip: true
    slim: true
    strip: true
```

| Key Configuration       | Purpose                                              |
|-------------------------|------------------------------------------------------|
| Environment Variable    | Sets MODEL_BUCKET to the S3 bucket name.             |
| Permissions             | Grants Lambda permission to read from the S3 bucket. |
| Dockerized Pip          | Ensures compatible package installation for Lambda.  |

### 5. Writing the Lambda Function (main.py)

The Lambda function in main.py loads model parameters from S3, processes input features, and returns predictions.

| Function               | Purpose                                                                       |
|------------------------|-------------------------------------------------------------------------------|
| SimpleLogisticModel    | Defines model class to perform logistic regression.                          |
| load_model             | Loads model parameters from S3 into a SimpleLogisticModel instance.          |
| lambda_handler         | Main Lambda handler function that handles requests, loads model, predicts.   |

### 6. Adding Dependencies (requirements.txt)

Create a requirements.txt file with only the necessary dependencies:

```bash
boto3==1.20.0
numpy==1.18.5
```

These will be installed in the Lambda environment to keep the deployment package lightweight.

### 7. Deploying with Serverless

Run the following command to deploy your function on AWS Lambda:

```bash
serverless deploy
```

### 8. Testing the Deployed API

With your API deployed, you can test it using curl:

```bash
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/predict \
-H "Content-Type: application/json" \
-d '{"features": [28, 3, 8, 1, 5]}'
```

## Conclusion

We've successfully built, deployed, and tested a lightweight Dog vs. Cat Lover Predictor on AWS Lambda, using serverless architecture to create a scalable and efficient solution.



