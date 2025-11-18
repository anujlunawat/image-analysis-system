import json
import boto3
from datetime import datetime
from decimal import Decimal

rekognition = boto3.client("rekognition")
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

table = dynamodb.Table("ImageAnalysisResults")
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:YOUR_ACCOUNT_ID:ImageAnalysisTopic"

def convert_to_decimal(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    if isinstance(obj, list):
        return [convert_to_decimal(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_to_decimal(v) for k, v in obj.items()}
    return obj

def lambda_handler(event, context):

    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        filename = record["s3"]["object"]["key"]

        label_response = rekognition.detect_labels(
            Image={"S3Object": {"Bucket": bucket, "Name": filename}},
            MaxLabels=10,
            MinConfidence=70
        )
        labels = convert_to_decimal(label_response["Labels"])

        text_response = rekognition.detect_text(
            Image={"S3Object": {"Bucket": bucket, "Name": filename}}
        )
        text_items = [
            item["DetectedText"]
            for item in text_response["TextDetections"]
            if item.get("Type") == "LINE"
        ]

        face_response = rekognition.detect_faces(
            Image={"S3Object": {"Bucket": bucket, "Name": filename}},
            Attributes=["ALL"]
        )

        # rekognition returns float values in confidence scores and face attributes. 
        # but, dynamodb doesn't accept floating-point numbers.
        # hence, every numberical/float value must be converted to decimal.
        faces = convert_to_decimal(face_response.get("FaceDetails", []))

        table.put_item(
            Item={
                "filename": filename,
                "labels": labels,
                "text": text_items,
                "faces": faces,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

        email_message = (
            f"Image Analyzed: {filename}\n\n"
            f"Objects: {[l['Name'] for l in labels]}\n"
            f"Text: {text_items}\n"
            f"Faces Detected: {len(faces)}\n"
            f"Timestamp: {datetime.utcnow().isoformat()}"
        )

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="New Image Analysis Result",
            Message=email_message
        )

    return {"status": "done"}
