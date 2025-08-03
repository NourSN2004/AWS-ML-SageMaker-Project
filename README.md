# AWS-ML-SageMaker-Project
ML Project on Sagemaker 
# Scones Unlimited Image Classification Workflow

This project implements a serverless, end-to-end image classification pipeline using AWS services for the Scones Unlimited delivery routing system. It demonstrates modern ML operations (MLOps) practices by:

* **Extracting** and **preprocessing** CIFAR-100 images from S3 via an AWS Lambda function
* **Training** a SageMaker built-in Image Classification model
* **Deploying** the model to a real-time SageMaker endpoint
* **Orchestrating** inference using AWS Step Functions and Lambda
* **Capturing** and **visualizing** inference data with SageMaker Model Monitor

---

## 🏗 Architecture Overview

```text
CIFAR data (bicycle & motorcycle)
      ↓
S3 Bucket (train/, test/)
      ↓
SageMaker Training Job → SageMaker Endpoint
      ↓
Step Functions Workflow:
  1) serializeImageData Lambda
  2) classifyImage Lambda
  3) filterInferences Lambda → Succeed/Fail
      ↓
Model Monitor captures inputs & outputs → S3
      ↓
Notebook for Testing & Visualization
```

![Step Functions Workflow](screenshots/step_function_success.png)

---

## ⚙️ Components

### 1. Lambda Functions (in `lambda.py`)

* **`serializeImageData`**: Downloads an image from S3, base64-encodes it
* **`classifyImage`**: Invokes the SageMaker endpoint via `boto3` (`sagemaker-runtime`)
* **`filterInferences`**: Checks that the model’s confidence exceeds a threshold (0.93)

### 2. Step Functions (`step_function.json`)

A Standard state machine chains the three Lambdas. The final step is configured to fail loudly on low confidence (no Catch).

### 3. SageMaker Model

* **Training**: Used the built-in `image-classification` algorithm for 30 epochs on 2 classes (bicycle vs. motorcycle)
* **Deployment**: Deployed on `ml.m5.xlarge` with data-capture enabled (100% sampling)

---

## 🚀 Setup & Deployment

1. **Data Preparation**: Run the ETL notebook to extract CIFAR-100, filter classes 8 & 48, save images to S3.
2. **Training**: In the same notebook, configure and run the SageMaker Estimator.
3. **Deployment**: Deploy the trained model; note the endpoint name printed for later use.
4. **Lambda & Step Functions**:  Create three Lambdas with Python 3.9, attach necessary IAM policies, paste handler code, and deploy. Author the Step Function in the visual editor.
5. **Testing & Evaluation**: Use the provided `generate_test_case()` helper to trigger multiple executions. Download Model Monitor logs, parse JSONLines, and visualize.

---

## 🔍 Testing & Evaluation

* **Step Function Executions**: Ran 5 randomized tests – see console logs for mixed Succeeded/Failed runs.
* **Model Monitor Visualization**:

  * **Scatter Plot** of inference confidence over time
  * **Histogram** of confidence distribution

![Inference Confidence Over Time](screenshots/confidence_time_series.png)

---

## 🎯 Stretch Goals

* **Automated Alerts**: Configured CloudWatch Alarms on low-confidence errors
* **Batch Inference**: Extended workflow to process S3 folders of images via AWS Batch + Lambda
* **Custom Threshold Tuning**: Developed a small GUI to adjust threshold and redeploy Step Function

---

## 🧹 Cleanup

To avoid costs, remove all resources:

1. **Delete** the SageMaker endpoint, endpoint config, model
2. **Stop/Delete** notebook instances
3. **Delete** the Step Functions state machine
4. **Delete** all three Lambda functions
5. **Empty/Delete** the S3 bucket (train/, test/, data\_capture/)

---

## 📄 Files

* **`lambda.py`** – All three Lambda handlers
* **`step_function.json`** – Exported state machine definition
* **`screenshots/`** – Visuals of workflow and plots

---

*By Nour Shammaa*

