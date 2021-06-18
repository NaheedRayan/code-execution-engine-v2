import sys
import subprocess
import re
import gc

from  datetime import datetime
import json
# import resource 

# "python3 run.py "+ json_msg.filename +" "+extensions[json_msg.lang]+" "+json_msg.timeout 
filename = str(sys.argv[1])
extension = str(sys.argv[2])
timeout = str(sys.argv[3])


java_file_class_name = str()
error_message = str()


# for java
def changing_class_name():

    grep_syntax = """'(?<=\\n|\A|\\t)\s?(public\s+)*(class|interface)\s+\K([^\\n\s{]+)'"""

    fl = subprocess.run(f"cd temp/ && grep -P -m 1  -o {grep_syntax} {filename}.java"  ,shell=True , stdout=subprocess.PIPE,stderr=subprocess.STDOUT  , timeout=60)


    global java_file_class_name
    java_file_class_name = fl.stdout.decode().strip()

    # for renaming the file
    subprocess.run(f"cd temp/ && mv {filename}.java {java_file_class_name}.java"  ,shell=True , stdout=subprocess.PIPE,stderr=subprocess.STDOUT  , timeout=60)



# mem_start = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
# mem_end = 0
end_time = 0
begin_time = 0
status = True #for error checking

#########################################################
############  Reading the input file ####################
#########################################################
try:
    inputfile = subprocess.run(f"cd temp/ && cat input.txt"  ,shell=True , stdout=subprocess.PIPE,stderr=subprocess.STDOUT  , timeout=int("5"))
except Exception as e:
    result = 'Something went wrong while reading input file'
    status = False
    error_message = str(e)



#########################################################
##############  Compiling the file ######################
#########################################################
if(status):
    try:
        if(extension == "cpp" or extension == "c"):
            comp = subprocess.run(f"cd temp/ && g++ {filename}.{extension} -o {filename}"  ,shell=True , stdout=subprocess.PIPE,stderr=subprocess.STDOUT  , timeout=60)
            if(comp.stdout.decode()):
                result = comp.stdout.decode()
                error_message = result
                status = False

        if(extension == "java"):
            changing_class_name()
            comp = subprocess.run(f"cd temp/ && javac {java_file_class_name}.java"  ,shell=True , stdout=subprocess.PIPE,stderr=subprocess.STDOUT ,timeout=60 )
            if(comp.stdout.decode()):
                result = comp.stdout.decode()
                error_message = result
                status = False
        
    except Exception as e:
        result = "Something went wrong while compiling the file\n"+str(e)
        status = False
        error_message = str(e)


#########################################################
################  Running the file ######################
#########################################################
if(status):
    try:
        

        if(extension == "py"):
            begin_time = datetime.today().timestamp() # getting initial
            output = subprocess.run(f"cd temp/ && timeout -s KILL 5 python3 {filename}.{extension}"  ,shell=True , stdout=subprocess.PIPE, stderr=subprocess.PIPE ,  input=(inputfile.stdout.decode()).encode() , timeout=int(timeout))
            result = output.stdout.decode()

        elif(extension=="cpp" or extension == "c"):
            begin_time = datetime.today().timestamp() # getting initial
            output = subprocess.run(f"cd temp/ && timeout -s KILL 5 ./{filename}"  ,shell=True , stdout=subprocess.PIPE,stderr=subprocess.PIPE , input=(inputfile.stdout.decode()).encode() , timeout=int(timeout))
            result = output.stdout.decode()

        elif(extension == "java"):
            begin_time = datetime.today().timestamp() # getting initial
            output = subprocess.run(f"cd temp/ && timeout -s KILL 5 java {java_file_class_name}"  ,shell=True , stdout=subprocess.PIPE,stderr=subprocess.PIPE , input=(inputfile.stdout.decode()).encode() , timeout=int(timeout))
            result = output.stdout.decode()

        # mem_end = getrusage(RUSAGE_CHILDREN).ru_maxrss-mem_start 
        end_time = datetime.today().timestamp() - begin_time

        # if there is any error we will also add the error
        if(output.stderr.decode() != ""):
            result += output.stderr.decode()
            status = False
            error_message = output.stderr.decode()

        

    except Exception as e:
        result  = "Time limit exceeded\n"
        status = False
        end_time = datetime.today().timestamp() - begin_time
        error_message = str(e)
        # mem_end = 0
        


# mem_end = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss-mem_start 
end_time = datetime.today().timestamp() - begin_time




#########################################################
################  Checking output size ##################
#########################################################
a = sys.getsizeof(result)
a = a/1048567 #converting bytes to mb

if(a > 5): #if the data is greater than 5mb then the data will not be written in output.txt
    result = "Out of memory"
    status = False   
    error_message = "Output data more than 5mb"


# getting the result and writting it on output.txt
file = open("./temp/output.txt" , "w")
file.write(result)
file.close()

del result
gc.collect()#garbage collector


#########################################################
############### Transfering data as json ################
#########################################################
if(status == True):
    status_data = {
    	"status" : "Successful" ,
    	"time" : format(end_time, ".4f") ,
        "error_message" : error_message
    }
    j = json.dumps(status_data)
    print(j ,end="")
else:
    status_data = {
    	"status" : "Failed" ,
    	"time" : format(end_time, ".4f"),
        "error_message" : error_message
    }
    j = json.dumps(status_data)
    print(j,end="")