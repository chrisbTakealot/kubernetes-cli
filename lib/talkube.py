from kubernetes import client, config
import os

class talkube():
	v1 = None

	
	def __init__(self):
		# load config
		config.load_kube_config()	
		self.v1 = client.CoreV1Api()


	def print_header(self, header_name):
		print header_name
		print "-" * len(header_name)

	
	def list_pods(self):
		"""
		List all pods

		"""
		self.print_header("Listing pods with their IPs:")
		ret = self.v1.list_pod_for_all_namespaces(watch=False)
		for i in ret.items:
		    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


	def pod_find(self, podname, namespace=None):
		"""
		Find a pod by namespace (Default all) and partial podname

		"""
		self.print_header("Looking for pod with name: %s in namespace: %s" % (podname, namespace if namespace else "All"))
		ret = self.v1.list_pod_for_all_namespaces(watch=False)
		for i in ret.items:
			if(podname in i.metadata.name) and (namespace is None or namespace == i.metadata.namespace):
				print "Matched %s" % i.metadata.name
				return  i.metadata.name
		print "* No match found *"
		return None


	def pod_bash(self, podname):
		"""
		Connect to pod 	    	
		$ kubectl exec -it  $_PODNAME_$ -- /bin/bash
    	"""
		
		self.print_header("Connecting to bash for pod: %s" % podname)
		os.system("kubectl exec -it %s -- /bin/bash" % podname)
