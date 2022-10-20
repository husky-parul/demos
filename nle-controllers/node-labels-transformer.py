import os
from kubernetes import client, config

class NodeLabelsUpdater():

    def updateNodeLabels(self):
        self.kubeconfig = os.getenv("KUBECONFIG","/home/.kube/config")
        node_map = [{"baremetal01.ibm.cloud":"green"}]

        #  provide list of nodes in the env vaiable
        config.load_kube_config(self.kubeconfig)
        client.configuration.debug = True

        api_instance = client.CoreV1Api()

        
        for i in node_map:
            for key, value in i:
                body = {
                    "metadata": {
                    "labels": {
                        "carbon_intensity": value
                        }
                   }
                }
                api_response = api_instance.patch_node(key, body)
                pprint(api_response)

if __name__ == '__main__':
    obj = NodeLabelsUpdater()
    obj.updateNodeLabels()

