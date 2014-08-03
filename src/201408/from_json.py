'''
Created on Aug 3, 2014

@author: fcmeng
'''
import json
from boto import ec2
class JsonLoader:
    def __init__(self):
        file_to_read = open('aws.json', 'r')
        json_file=file_to_read.read()
        file_to_read.close()  
        self.payload=json.loads(json_file)  

if __name__ == '__main__':
    l=JsonLoader()  
    env=l.payload['aws_credentials']['gandalf'] 
    conn = ec2.connect_to_region(env['region'],
                                 aws_access_key_id=env['aws_access_key_id'],
                                 aws_secret_access_key=env['aws_secret_access_key'])
    
    filters={'instance-state-name' : ['running'],'tag:Name':'communication-platform/jobs'}
    instances = []
    reservations = conn.get_all_instances(filters=filters)
  
    for r in reservations:
        instances += r.instances
    for i in instances: 
        print(i,i.id,i.image_id,i.states)
    
    
    