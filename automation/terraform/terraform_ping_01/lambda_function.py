import requests
import json

def lambda_handler(event, context): 

    max = 0
    min = 1000
    total = 0
    avg = 0
    samples = 5

    url = event['host']
    whoami = event['whoami']

    for i in range(samples):
        
        response = requests.head(url)
        mark = response.elapsed.total_seconds() * 1000

        if mark > max:
            max = mark
        
        if mark < min:
            min = mark

        total += mark

    ### end of for loop ###

    avg = total / samples

    result = { "statusCode": 200, "message": "OK",
            'min': str(min), 'max': str(max), 'avg': str(avg),
            'host': url, 'whoami':whoami }

    return(result)


if __name__=='__main__':
    
    print(lambda_handler({"host":"https://www.google.com", "whoami":"us-east-1"}, {} ) )
