import re
import os
import subprocess
import numpy as np
import concurrent.futures

##########################################################################################################################################################################################
# function to get the path of the current directory
##########################################################################################################################################################################################   
def getCurrentDirectoryPath(directoryName):
    base_dirc = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dirc, directoryName)
    return path


##########################################################################################################################################################################################
# function to create a directory
##########################################################################################################################################################################################
def createDirectory(directoryName):
    print(directoryName)
    try:
        path = getCurrentDirectoryPath(directoryName)
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print('Error: Creating directory. ', directoryName)


##########################################################################################################################################################################################
# runs the wget command and logs the information in log file
##########################################################################################################################################################################################
def run_wget_cmd(wget_cmd, verbose = False, *args, **kwargs):
    process = subprocess.Popen(
        wget_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )
    std_out, std_err = process.communicate()
    return std_err


##########################################################################################################################################################################################
# Downloading the files concucurrently using thread pool.
# @repetition -> Represents the repetition number
# @downloadSize -> size of the file to be downloaded
# @link -> url from where the files is being downloaded
# @logFileName -> to log the output of wget command
# @noOfConcurrentDownloads -> number of times the files is downloaded concurrently
##########################################################################################################################################################################################
def runConcurrentDownloads(repetition, downloadSize, link, logFileName, noOfConcurrentDownloads):
    directory_name = str(downloadSize) + "_concurrentdownload_" + str(noOfConcurrentDownloads)
    createDirectory(directory_name)
    path = getCurrentDirectoryPath(directory_name)

    wget = 'wget --limit-rate=10M --directory-prefix=' + path + ' ' + link
    with concurrent.futures.ThreadPoolExecutor(max_workers=noOfConcurrentDownloads) as threadExecutor:
        throughputs = []
        throughputValues = []
        futureToUrl = {threadExecutor.submit(run_wget_cmd, wget, verbose=False): degree for degree in range(noOfConcurrentDownloads)}
        for future in concurrent.futures.as_completed(futureToUrl):
            wgetLog = future.result()
            throughput = regex.search(wgetLog)
            if throughput is not None:
                splittedThroughput = throughput.group(0).split(" ")
                throughputValue = float(splittedThroughput[0])
                throughputMetric = splittedThroughput[1].strip()

                # if the throughput is in KB/s, convert into MB/s
                if throughputMetric == "KB/s":
                    throughputValue = round((throughputValue / 1024), 2)
                    throughputMetric = "MB/s"

                throughputs.append(str(throughputValue) + " " + throughputMetric)
                throughputValues.append(throughputValue)
                
            with open(logFileName, 'a') as logFile:
                print(wgetLog, file=logFile)
                print("############################################################################################################################", file=logFile)

    extraValuesNeeded = noOfConcurrentDownloads - len(throughputValues)
    initialAverage = round(np.mean(throughputValues), 2)
    for x in range(extraValuesNeeded):
        throughputValues.append(initialAverage)
        
    dataLogName = str(repetition) + "_downloadLimit_10M_" + str(downloadSize) + "File_" + str(noOfConcurrentDownloads) + ".txt"
    with open(dataLogName, 'w') as dataLog:
        print(throughputs, file=dataLog)
        print("Average Throughput: " + str(round(np.mean(throughputValues), 2)) + "MB/s", file=dataLog)
        


##########################################################################################################################################################################################
# Start point of the execution of the program
##########################################################################################################################################################################################
if __name__ == '__main__':
    noOfConcurrentDownloads = [10, 25, 50]
    sizes = ["100KB","1MB","100MB"]
    links = ["https://cloud.iitmandi.ac.in/f/36c1c10b5caf46948ee9/?dl=1",
             "https://cloud.iitmandi.ac.in/f/fef3ed77ad16482582f9/?dl=1",
             "https://cloud.iitmandi.ac.in/f/f760934703f647c49dbb/?dl=1",
             "https://cloud.iitmandi.ac.in/f/5d31e8769b954109be61/?dl=1",
             "https://cloud.iitmandi.ac.in/f/0e1dfdb780e845129513/?dl=1",
             "https://cloud.iitmandi.ac.in/f/07109a50545d4930a714/?dl=1",
             "https://cloud.iitmandi.ac.in/f/2984f340696b4ab8b301/?dl=1",
             "https://cloud.iitmandi.ac.in/f/c200476d3ce247e08c87/?dl=1",
             "https://cloud.iitmandi.ac.in/f/d276f3cbe766409db927/?dl=1"
            ]
    
    # regex to match the format (12.0 MB/s) to get the throughput from wget output
    regex = re.compile(r'(\d{1,4}\.?\d{0,4}\ [KM][Bb]/s)')
    
    for repetition in range(1, 4):
        logFileName = "Autolog-" + str(repetition) + "-7PM.txt"
        with open(logFileName, 'w') as logFile:
            print("Repetition No: " + str(repetition))

        i = 0
        for link in links:
            runConcurrentDownloads(repetition, sizes[i], link, logFileName, 25)
            i += 1
 
