# Infrastructure Specification

## S3
Bucket used for all inbound image uploads:
- image-analysis-bucket-anuj

## DynamoDB
Table: ImageAnalysisResults  
Partition key: filename (String)

## SNS
Topic for outbound email alerts:
- ImageAnalysisTopic  
Email subscription must be confirmed.

## IAM Access
The Lambda execution role must include:
- Full Rekognition access  
- S3:GetObject on the image bucket  
- DynamoDB write permissions on the analysis table  
- SNS:Publish for the notification topic  

## Trigger Configuration
S3 ObjectCreated events must be connected to the Lambda function.
