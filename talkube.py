import lib.talkube
import os

def main():
	print """
 _______       _      _  __     _          
|__   __|/\   | |    | |/ /    | |         
   | |  /  \  | |    | ' /_   _| |__   ___ 
   | | / /\ \ | |    |  <| | | | '_ \ / _ \\
   | |/ ____ \| |____| . \ |_| | |_) |  __/
   |_/_/    \_\______|_|\_\__,_|_.__/ \___|
         Takealot Kubernetes CLI Tools
         """

	tkube = lib.talkube.talkube()
	tkube.list_pods()


if __name__ == "__main__":
	main()
