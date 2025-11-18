# AI-Driven Image Analysis Pipeline

This project implements an automated image-processing workflow on AWS. Images placed in an S3 bucket trigger a Lambda function. The function runs Amazon Rekognition to extract labels, text, and face attributes. The processed results are written to DynamoDB, and a summary is delivered by email through SNS.

## Architecture Summary
S3 → Lambda → Rekognition → DynamoDB → SNS Email

## End-to-End Flow
1. An image is uploaded into an S3 bucket.  
2. S3 emits an event for newly created objects.  
3. The event activates a Lambda function.  
4. Lambda calls Rekognition to analyze the file for objects, optical text, and face characteristics.  
5. Rekognition outputs floating-point values; these are normalized into Decimal to match DynamoDB’s numeric constraints.  
6. Structured results are stored in DynamoDB using the image filename as the key.  
7. Lambda publishes a brief analysis report to an SNS topic.  
8. SNS sends the report to the confirmed email subscriber.

## AWS Components Used
- Amazon S3 for object storage  
- AWS Lambda for event-driven execution  
- Amazon Rekognition for visual analysis  
- Amazon DynamoDB for result persistence  
- Amazon SNS for email dispatch  
- IAM for scoped permissions  

## Prerequisites
Python 3.x runtime in Lambda.  
IAM role that permits:  
- Rekognition calls  
- S3 GetObject  
- DynamoDB PutItem and UpdateItem  
- SNS Publish  

## Deployment Outline
1. Create an S3 bucket for incoming images.  
2. Create a DynamoDB table named `ImageAnalysisResults` with `filename` as the partition key.  
3. Create an SNS topic and confirm your email subscription.  
4. Deploy the Lambda function and attach the required policies.  
5. Add the S3 ObjectCreated trigger to the Lambda function.  
6. Upload an image to validate the entire chain.

## Data Stored in DynamoDB
Each entry contains:  
- filename  
- detected labels  
- extracted text  
- face attributes  
- timestamp  

## Notification Output
SNS email contains a concise breakdown of detected labels, text, face count, and timestamp.

## Potential Extensions
Optional improvements:  
- Add moderation analysis for unsafe content  
- Include a pre-signed image link in outbound email  
- Add alarms for Lambda failures  
- Expose results via API Gateway
