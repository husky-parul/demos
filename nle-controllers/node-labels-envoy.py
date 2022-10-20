#read metrics from prometheus for the two nodes
# compute CIM reading = log(last hr) / log(last 24 hrs)
# forcasted CIM for the next 2 hrs
# assign label: 
    # green =  min(node1, node2)
    # red = max(node1, node2)


import os
import requests,sys
import math



class NodeLabelEnvoyController():
    def __init__(self):
        self.url = os.getenv("PROMETHEUS_URL","http://localhost:9090")
        print("self.url", self.url)


    
    def computeNodeLabels(self):

        params_list = [
            {'query': 'sum(sum_over_time(carbon_intensity{zone="GB"}[2h]))'},
            {'query': 'sum(sum_over_time(carbon_intensity{zone="GB"}[1d]))'},
            {'query': 'sum(sum_over_time(carbon_intensity{zone="DK"}[2h]))'},
            {'query': 'sum(sum_over_time(carbon_intensity{zone="DK"}[1d]))'}
        ]
        n1_ci_lh = n1_ci_ld = n2_ci_lh = n2_ci_ld = 0.0
        
        # n1_ci_lh GB
        response = requests.get('http://localhost:9090/api/v1/query',params=params_list[0])
        results = response.json()['data']['result']
        n1_ci_lh = int(results[0]['value'][1])
        log_n1_ci_lh = math.log(n1_ci_lh)

        # n1_ci_ld GB
        response = requests.get('http://localhost:9090/api/v1/query',params=params_list[1])
        results = response.json()['data']['result']
        n1_ci_ld = int(results[0]['value'][1])
        log_n1_ci_ld = math.log(n1_ci_ld)

        node1_ci =  log_n1_ci_lh / log_n1_ci_ld

        print("Node 1 CI",node1_ci)


        # n2_ci_lh DK
        response = requests.get('http://localhost:9090/api/v1/query',params=params_list[2])
        results = response.json()['data']['result']
        n2_ci_lh = int(results[0]['value'][1])
        log_n2_ci_lh = math.log(n2_ci_lh)

        # n2_ci_ld DK
        response = requests.get('http://localhost:9090/api/v1/query',params=params_list[3])
        results = response.json()['data']['result']
        n2_ci_ld = int(results[0]['value'][1])
        log_n2_ci_ld = math.log(n2_ci_ld)

        node2_ci =  log_n2_ci_lh / log_n2_ci_ld

        print("Node 2 CI",node2_ci)

        min_ci = min(node1_ci,node2_ci)

        if min_ci == node1_ci:
            return {"Green":"GB"} #this should return node name
        else:
            return{"Green":"DK"}


if __name__ == "__main__":
    obj = NodeLabelEnvoyController()
    obj.computeNodeLabels()
    

