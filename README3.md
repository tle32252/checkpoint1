This file does not support the resume function for thread. However, it is able to download the file one at a time as thread. Moreover, the no. of connections default is 5.(I already tried to make it handle to receive the no. of connections you want but there is some error so I set the default is 5 to avoid this error).

To run this file please do chmod +x in the terminal 


To do the normal download, in the main function, else part, use self.downloadAll() instead of self.downloadThread() or you can run srget2final.py instead

ex: ./srgetcp3.py -o filename.txt url

