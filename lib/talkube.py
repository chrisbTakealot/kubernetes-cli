from kubernetes import client, config
import os

class talkube():
	v1 = None

	def __init__(self):
		# load config
		config.load_kube_config()	
		self.v1 = client.CoreV1Api()

	def list_pods(self):
		"""
		List all pods

		"""
		print "Listing pods with their IPs:"
		print "----------------------------"
		ret = self.v1.list_pod_for_all_namespaces(watch=False)
		for i in ret.items:
		    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))