import json
import boto3

def lambda_handler(event, context):
    flag = 0
    shaHash=event['path'][1:]
    s3 = boto3.client('s3')
    
    resp = s3.select_object_content(
        Bucket='shahash',
        Key='output.csv',
        ExpressionType='SQL',
        Expression=f"SELECT s.password FROM s3object s where s.shaHash = '{shaHash}'",
        InputSerialization = {'CSV': {"FileHeaderInfo": "Use"}, 'CompressionType': 'NONE'},
        OutputSerialization = {'CSV': {}},
    )
    print(resp)
    for event in resp['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            flag = 1
        elif 'Stats' in event:
            statsDetails = event['Stats']['Details']
            print("Stats details bytesScanned: ")
            print(statsDetails['BytesScanned'])
            print("Stats details bytesProcessed: ")
            print(statsDetails['BytesProcessed'])
            print("Stats details bytesReturned: ")
            print(statsDetails['BytesReturned'])
    
    
    if (flag == 1):  
        pwd = records.rstrip()
        return {
            'statusCode': 200,
            'body': json.dumps({shaHash:pwd})
        }
    else:
        return{
            'statusCode' :404,
            'body' : ""
        }