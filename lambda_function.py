import boto3
import os
import datetime

textract = boto3.client('textract')
sns = boto3.client('sns')
s3client = boto3.client('s3')

badimagesns=os.environ['bad_image_sns']
circuitname=os.environ['circuit_name']
#s3SourceBucketName=os.environ['s3_source_bucket']
s3resultbucket=os.environ['s3_result_bucket']

def lambda_handler(event, context):
    print(event)
    for item in event['Records']:
        s3SourceBucketName=item['s3']['bucket']['name']
        documentName=item['s3']['object']['key']
    
    #documentName = "Screen Shot 2019-08-30 at 10.58.37 AM.png"
    #documentName = "deepracer_bad_photo.jpg"

    # Call Amazon Textract

    response = textract.detect_document_text(
        Document={
        'S3Object': {
        'Bucket': s3SourceBucketName,
        'Name': documentName
        }
        })

    # Initial search for team name, as this is not detected as a key/value pair
    ###########################################################################

    print(response)
    
    teamstr=""
    laptimestr=""
    subtimestr=""
    deepracercircuit=""
    
    
    for x in range(2,len(response["Blocks"])):
        #print(response["Blocks"][x])
        #print('*******************')
        if 'Racer name' in response["Blocks"][x]['Text']:
            teamstr=response["Blocks"][x]['Text']
            print(teamstr)
        if 'Your best average lap time' in response["Blocks"][x]['Text']:
            laptimestr=response["Blocks"][x+1]['Text']
            print(laptimestr)
        if 'Submission time' in response["Blocks"][x]['Text']:
            subtimestr=response["Blocks"][x+1]['Text']
            print(subtimestr)
        if circuitname in response["Blocks"][x]['Text']:
            deepracercircuit=response["Blocks"][x]['Text']
            print(deepracercircuit)    
   
    # if assumed fields not found in the image then send email/sms via sns
    if (teamstr=="") or (laptimestr=="") or (subtimestr=="") or (deepracercircuit==""):
        print("Required fields not found in Image")
        badimagemessage="DeepRacer Submission Error - Required fields not found in "+ documentName
        snsresponse=sns.publish(TopicArn=badimagesns,
                                Message=badimagemessage,
                                Subject="Invalid Deepracer image submitted")
        return 'Bad Image'                            
    
    teamname = teamstr[12:]
    subtimestr = subtimestr.replace(","," ")
    print(teamname)
    print(subtimestr)
    print(laptimestr)
    print(deepracercircuit)
    
    #put the result into s3 bucket
    current_time=datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%f")
    item=teamname+','+subtimestr+','+laptimestr
    s3key= teamname +"_"+ current_time+".csv"
    s3response = s3client.put_object(Bucket=s3resultbucket,
                            Body=item,Key=s3key)
    
    return 'Image Processed'