from kubernetes import client, config
import os
import argparse


class bcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class talkube():
	v1 = None

	
	def __init__(self):
		# load config
		config.load_kube_config()	
		self.v1 = client.CoreV1Api()


	def print_header(self, header_name):
		print bcolours.HEADER + header_name + bcolours.ENDC
		print bcolours.HEADER + "-" * len(header_name)  + bcolours.ENDC

	
	def list_pods(self,namespace=None):
		"""
		List all pods

		"""
		self.print_header("Listing pods with their IPs:")
		ret = self.v1.list_pod_for_all_namespaces(watch=False)
		for i in ret.items:
			if (namespace is None or namespace == i.metadata.namespace):
			    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
		print


	def pod_find(self, podname, namespace=None):
		"""
		Find a pod by namespace (Default all) and partial podname

		"""
		pod_found=None
		self.print_header("Looking for pod with name: %s in namespace: %s" % (podname, namespace if namespace else "All"))
		ret = self.v1.list_pod_for_all_namespaces(watch=False)
		for i in ret.items:
			if(podname in i.metadata.name) and (namespace is None or namespace == i.metadata.namespace):
				pod_found=i.metadata.name
				continue
		print ("Matched %s" % pod_found) if pod_found else ("* No match found *")
		print
		return pod_found


	def pod_bash(self, podname):
		"""
		Connect to pod 	    	
		$ kubectl exec -it  $_PODNAME_$ -- /bin/bash
    	"""
		
		self.print_header("Connecting to bash for pod: %s" % podname)
		os.system("kubectl exec -it %s -- /bin/bash" % podname)



if __name__ == "__main__":
	try:
		print bcolours.OKBLUE + """
 _______       _      _  __     _          
|__   __|/\   | |    | |/ /    | |         
   | |  /  \  | |    | ' /_   _| |__   ___ 
   | | / /\ \ | |    |  <| | | | '_ \ / _ \\
   | |/ ____ \| |____| . \ |_| | |_) |  __/
   |_/_/    \_\______|_|\_\__,_|_.__/ \___|
         Takealot Kubernetes CLI Tools
	         """ + bcolours.ENDC

		tkube = talkube()
		parser = argparse.ArgumentParser(description="A CLI tool for kubernetes") 
		parser.add_argument('podname', nargs='?', help='podname to use (partial match)')
		parser.add_argument('-l', '--list', help='List all running pods', required=False, action='store_true')
		parser.add_argument('-n', '--namespace', help='Namespace to filter on', required=False)
		parser.add_argument('-b', '--bash', help='Connect to pod bash', required=False, action='store_true')
		args = parser.parse_args()

		# list active pods using namespace filter
		if args.list:
			tkube.list_pods(namespace=args.namespace)

		# if no valid action has been performed, show help.
		if args.podname is None:
			if not args.list:
				parser.print_help()
				exit(1)
			else:
				exit(0)

		# find podname (partial match) using namespace filter (if set)
		podname = tkube.pod_find(podname=args.podname, namespace=args.namespace)
		if podname is None:
			raise Exception("Podname %s not found" % podname)

		# do we run bash
		if args.bash:
			tkube.pod_bash(podname=podname)

	except Exception as e:
		print
		print bcolours.ERROR + "!!! Error: %s !!!" % e.message + bcolours.ENDC
		print
