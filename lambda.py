# --- serializeImageData ---
import json, boto3, base64
s3 = boto3.client('s3')
def lambda_handler(event, context):
    payload = event.get("body") or event
    if isinstance(payload, str):
        payload = json.loads(payload)
    key, bucket = payload["s3_key"], payload["s3_bucket"]
    s3.download_file(bucket, key, "/tmp/image.png")
    with open("/tmp/image.png","rb") as f:
        img64 = base64.b64encode(f.read()).decode()
    return {"statusCode":200, "body": { "image_data": img64, "s3_bucket": bucket, "s3_key": key, "inferences": [] }}

# --- classifyImage ---
import json, base64, boto3
ENDPOINT = "image-classification-2025-08-02-19-21-34-805"
runtime  = boto3.client("sagemaker-runtime")
def lambda_handler(event, context):
    payload = event.get("body") or event
    if isinstance(payload, str):
        payload = json.loads(payload)
    img = base64.b64decode(payload["image_data"])
    resp = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType="image/png", Body=img)
    payload["inferences"] = resp["Body"].read().decode()
    return {"statusCode":200, "body": payload}

# --- filterInferences ---
import json
THRESHOLD = 0.93
def lambda_handler(event, context):
    payload = event.get("body") or event
    if isinstance(payload, str):
        payload = json.loads(payload)
    inferences = json.loads(payload["inferences"])
    if not any(float(x) > THRESHOLD for x in inferences):
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")
    return {"statusCode":200, "body": payload}
