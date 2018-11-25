# linux-top-parser-graph-maker

This program generate graphs from the linux TOP command log file. 

 # Requirements 
 
This program is written in python 3. 

This program requires Pandas and MatplotLib packages 


 # To Generate the TOP log files
If you want to collect the TOP logs for a particular processID 

```
 top -p 140432 -b -d 60 > toplogs_sample.log
```
 
 -p processID -d timeinterval ( collect every 60 seconds here ) -b batch mode
 
 You should have only one processID in your log file.
 
 Your log file will look like this 

```
top - 21:35:21 up 50 days,  4:00, 11 users,  load average: 11.32, 5.13, 2.93
Tasks:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.5 us,  0.4 sy,  0.0 ni, 98.9 id,  0.2 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem : 10715027+total, 17605536+free,  9269312 used, 88617804+buff/cache
KiB Swap:  3000256 total,  2461376 free,   538880 used. 10568942+avail Mem 

   PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
 61447 root      20   0 2472704 1.338g   3712 R  1880  0.1  12:34.14 kv_fileload

top - 21:35:51 up 50 days,  4:00, 11 users,  load average: 14.61, 6.53, 3.47
Tasks:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
%Cpu(s): 10.1 us,  1.3 sy,  0.0 ni, 88.3 id,  0.3 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem : 10715027+total, 17559014+free,  9734336 used, 88617824+buff/cache
KiB Swap:  3000256 total,  2461376 free,   538880 used. 10564290+avail Mem 

   PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
 61447 root      20   0 2491904 1.781g   3712 R  1624  0.2  20:41.87 kv_fileload
 
 .
 .
 .
 
 ```
 
 # To Run the Program
 
 Copy the program and the log file to a new Folder and Run 
 
 ```
  python3 read_logs.py -f toplogs_sample.log -p 61447 -n kv_fileload
 ```
 # The Output Files Look Like Below 
 
 ![Alt text](https://github.com/kaushikvelusamy/linux-top-parser-graph-maker/blob/master/output.png)

 # Quick Reference for understanding the TOP ouput

 1. https://www.booleanworld.com/guide-linux-top-command/
 2. https://linuxaria.com/howto/understanding-the-top-command-on-linux

 
 
