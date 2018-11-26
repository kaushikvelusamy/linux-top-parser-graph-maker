import re
import pandas as pd
from collections import defaultdict
import datetime
import argparse
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=True)
parser.add_argument("--processID", "-p", type=str, required=True)
parser.add_argument("--processName", "-n", type=str, required=True)

args = parser.parse_args()
filename = args.file
pid = args.processID
pname = args.processName

log_text = open(filename)
content_dict = defaultdict(list)

for line in log_text:
	if line.startswith('top'):
		linecontent = map(lambda x: x.strip(),line.split("top - ")[1].split(","))
		linecontent = list(linecontent)
		linecontent[0] = linecontent[0].split("up")[0].strip()
		content_dict['top'].append(linecontent)
	if line.startswith('Tasks:'):
		linecontent = map(lambda x: x.strip(),line.split("Tasks:   ")[1].split(","))
		content_dict['Tasks'].append(linecontent)
	if line.startswith('%Cpu(s):'):
		linecontent = map(lambda x: x.strip(),line.split("%Cpu(s):")[1].split(","))
		content_dict['Cpu'].append(linecontent)
	if line.startswith('KiB Mem'):
		linecontent = map(lambda x: x.strip(),line.split("KiB Mem : ")[1].split(","))
		content_dict['Memory in KiB'].append(linecontent)
	if line.startswith('KiB Swap:'):
		linecontent = map(lambda x: x.strip(),line.split("KiB Swap: ")[1].split(","))
		content_dict['Swap Memory'].append(linecontent)
	if pid in line and "root" in line:
		#print(line)
		subline = {}
		#print line
		linecontent = list(filter(lambda x: x!='',line.split(' ')))
		#print(linecontent)
		subline['PR']=float(linecontent[2])
		subline['NI']=float(linecontent[3])
		subline['VIRT']=float(linecontent[4]) if 't' not in linecontent[4] else float(linecontent[4].split("t")[0])
		subline['RES']=float(linecontent[5].split("g")[0]) if 't' not in linecontent[5] else float(linecontent[5].split("t")[0])
		subline['SHR']=float(linecontent[6])
		subline['percent_CPU']=float(linecontent[8])
		subline['percent_MEM']=float(linecontent[9])
		
		content_dict['Rest'].append(subline)
		if pname not in line:
			break

top_line = content_dict['top']
top_line_header_5 = ['complete_time', 'users', 'load_average_1', 'load_average_2', 'load_average_3']
top_line_header_6 = ['complete_time','hour_min', 'users', 'load_average_1', 'load_average_2', 'load_average_3']
processed_top_line_header = ['idx','complete_time', 'users', 'load_average_1', 'load_average_2', 'load_average_3']
processed_top_rows = []


for idx,row in enumerate(top_line):
	row = list(row)
	if len(row)==5:
		curr_entry = dict(zip(top_line_header_5,row))
	else:
		curr_entry = dict(zip(top_line_header_6,row))
	#print(curr_entry)
	#print(curr_entry['users']) 
	#print(curr_entry['users'].strip("load average:"))
	processed_row = [idx, datetime.datetime.strptime(curr_entry['complete_time'].split(" up ")[0],"%H:%M:%S").time(), float(curr_entry['users'].strip(" users")), float(curr_entry['load_average_1'].strip("load average:")), float(curr_entry['load_average_2']), float(curr_entry['load_average_3'])]
	processed_top_rows.append(processed_row)

df = pd.DataFrame(processed_top_rows,columns = processed_top_line_header)

line1=df.plot.line(x='complete_time', y='users')
plt.title('Total Time The TOP Logs Were Monitored');
plt.savefig('line1')
line2=df.plot.line(x='complete_time', y='load_average_1')
plt.title('Average Load On The System To The Last 1 Minute');
plt.savefig('line2')
line3=df.plot.line(x='complete_time', y='load_average_2')
plt.title('Average Load On The System To The Last 5 Minute');
plt.savefig('line3')
line4=df.plot.line(x='complete_time', y='load_average_3')
plt.title('Average Load On The System To The Last 15 Minute');
plt.savefig('line4')

tasks = content_dict['Tasks']
tasks_header = ['total', 'running', 'sleeping', 'stopped', 'zombie']
processed_task_header = ['idx', 'total', 'running', 'sleeping', 'stopped', 'zombie']
task_rows = []

for idx,row in enumerate(tasks):
	zip_entry = list(zip(tasks_header,row))
	#print(zip_entry)
	#processed_row = [idx]+ list(map(lambda x: print(x),zip_entry))
	processed_row = [idx]+ list(map(lambda x: int(x[1].strip(" "+x[0])),zip_entry))
	task_rows.append(processed_row)

task_df = pd.DataFrame(task_rows,columns = processed_task_header)

df = pd.merge(df, task_df, on='idx')
line5=df.plot.line(x='complete_time', y='total')
plt.title('Total Time The Current Process Was Running');
plt.savefig('line5')
line6=df.plot.line(x='complete_time', y='running')
plt.title('Time The Current Process Was In Running State');
plt.savefig('line6')
line7=df.plot.line(x='complete_time', y='sleeping')
plt.title('Time The Current Process Was In Sleeping State');
plt.savefig('line7')
line8=df.plot.line(x='complete_time', y='stopped')
plt.title('Time The Current Process Was In Stopped State');
plt.savefig('line8')
line9=df.plot.line(x='complete_time', y='zombie')
plt.title('Time The Current Process Was In Zombie State');
plt.savefig('line9')
tasks = content_dict['Cpu']
tasks_header = ['us', 'sy', 'ni', 'id', 'wa', 'hi', 'si', 'st']
processed_task_header = ['idx', 'us', 'sy', 'ni', 'id', 'wa', 'hi', 'si', 'st']
task_rows = []

for idx,row in enumerate(tasks):
	zip_entry = zip(tasks_header,row)
	processed_row = [idx]+ list(map(lambda x: float(x[1].strip(" "+x[0])),zip_entry))
	task_rows.append(processed_row)

task_df = pd.DataFrame(task_rows,columns = processed_task_header)

df = pd.merge(df, task_df, on='idx')
line10=df.plot.line(x='complete_time', y='us')
plt.title('Percentage Of The CPU For User Processes --US');
plt.savefig('line10')
line11=df.plot.line(x='complete_time', y='sy')
plt.title('Percentage Of The CPU For System Processes --SY');
plt.savefig('line11')
line12=df.plot.line(x='complete_time', y='ni')
plt.title('Percentage Of The CPU Processes With Priority Upgrade- nice --NI');
plt.savefig('line12')
line13=df.plot.line(x='complete_time', y='id')
plt.title('Percentage Of The CPU Not Used --ID');
plt.savefig('line13')
line14=df.plot.line(x='complete_time', y='wa')
plt.title('Percentage Of The CPU Processes Waiting For I/O Operations --WA');
plt.savefig('line14')
line15=df.plot.line(x='complete_time', y='hi')
plt.title('Percentage Of The CPU Serving Hardware Interrupts --HI');
plt.savefig('line15')
line16=df.plot.line(x='complete_time', y='si')
plt.title('Percentage Of The CPU Serving Software Interrupts --SI');
plt.savefig('line16')
line17=df.plot.line(x='complete_time', y='st')
plt.title('The Amount Of CPU Stolen From This Virtual Machine By The Hypervisor For Other Tasks --ST');
plt.savefig('line17')
tasks = content_dict['Memory in KiB']
tasks_header = ['+total', ' free', '+used', '+buff/cache']
processed_task_header = ['idx', 'total_memory', 'free', 'used', 'buffer/cache']
task_rows = []

for idx,row in enumerate(tasks):
	row = list(row)
	if '+free' in row[1]:
		tasks_header[1]='+free'
	zip_entry = list(zip(tasks_header,row))
	processed_row = [idx]+ list(map(lambda x: float(x[1].strip(x[0])),zip_entry))
	task_rows.append(processed_row)

task_df = pd.DataFrame(task_rows,columns = processed_task_header)

df = pd.merge(df, task_df, on='idx')
line18=df.plot.line(x='complete_time', y='total_memory')
plt.title('Total Physical Memory RAM Value+ As Seen From Top Logs');
plt.savefig('line18')
line19=df.plot.line(x='complete_time', y='free')
plt.title('Physical Memory RAM FREE Value+ As Seen From Top Logs');
plt.savefig('line19')
line20=df.plot.line(x='complete_time', y='used')
plt.title('Physical Memory RAM USED Value+ As Seen From Top Logs');
plt.savefig('line20')
line21=df.plot.line(x='complete_time', y='buffer/cache')
plt.title('Physical Memory Consumed By The Buffer/Cache');
plt.savefig('line21')
tasks = content_dict['Swap Memory']
tasks_header = ['+total', '+free', ' used', '+rest']
processed_task_header = ['idx', 'total_swap_memory', 'swap_free', 'swap_used', 'swap_avail_mem']
task_rows = []

for idx,row in enumerate(tasks):
	zip_entry = list(zip(tasks_header,row))
	#print(zip_entry)
	processed_row = [idx]+ list(map(lambda x: x[1].strip(" "+x[0]),zip_entry[:-1]))
	#print(processed_row)
	processed_row = [idx]+ list(map(lambda x: float(x[1].strip(" "+x[0])),zip_entry[:-1]))
	rest = zip_entry[-1][1]
	#print(rest)
	if " used. " in rest:
		used, swap_mem = rest.split(" used. ")
	else:
		used, swap_mem = rest.split("+used.")
	used = float(used)
	#print(used,'***',swap_mem)
	if "+avail Mem" in swap_mem:
		swap_mem = float(swap_mem.split("+avail Mem")[0])
	else:
		swap_mem = float(swap_mem.split(" avail Mem")[0])
	processed_row += [used, swap_mem]
	task_rows.append(processed_row)

task_df = pd.DataFrame(task_rows,columns = processed_task_header)
#print(task_df)
#print(df)
df = pd.merge(df, task_df, on='idx')
#print(df)
line22=df.plot.line(x='complete_time', y='total_swap_memory')
plt.title('Total SWAP Memory Value+ As Seen From Top Logs');
plt.savefig('line22')
line23=df.plot.line(x='complete_time', y='swap_free')
plt.title('SWAP Memory FREE Value+ As Seen From Top Logs');
plt.savefig('line23')
line24=df.plot.line(x='complete_time', y='swap_used')
plt.title('SWAP Memory USED Value+ As Seen From Top Logs');
plt.savefig('line24')
line25=df.plot.line(x='complete_time', y='swap_avail_mem')
plt.title('SWAP Memory AVAILABLE Value+ As Seen From Top Logs');
plt.savefig('line25')

tasks = content_dict['Rest']
#print("*"*250)
#print(tasks)
tasks_header = ['PR', 'NI', 'VIRT', 'RES', 'SHR', 'percent_CPU', 'percent_MEM']
processed_task_header = ['idx', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'percent_CPU', 'percent_MEM']
task_rows = []

for idx,row in enumerate(tasks):
	row1 = [idx]+[row[x] for x in tasks_header]
	task_rows.append(row1)

task_df = pd.DataFrame(task_rows,columns = processed_task_header)

df = pd.merge(df, task_df, on='idx')

#print(df)
line26=df.plot.line(x='complete_time', y='PR')
plt.title('Priority Of The Process --PR');
plt.savefig('line26')
line27=df.plot.line(x='complete_time', y='NI')
plt.title('The NICE Value Of The Process --NI');
plt.savefig('line27')
line28=df.plot.line(x='complete_time', y='VIRT')
plt.title('Virtual Memory Used By The Process --VIRT');
plt.savefig('line28')
line29=df.plot.line(x='complete_time', y='RES')
plt.title('Physical Memory Used From The Process --RES');
plt.savefig('line29')
line30=df.plot.line(x='complete_time', y='SHR')
plt.title('Shared Memory Of The Process --SHR');
plt.savefig('line30')
line31=df.plot.line(x='complete_time', y='percent_CPU')
plt.title('The Percentage Of CPU Used By This Process --%CPU');
plt.savefig('line31')
line32=df.plot.line(x='complete_time', y='percent_MEM')
plt.title('This Is The Percentage Of RAM Used By The Process --%MEM');
plt.savefig('line32')

