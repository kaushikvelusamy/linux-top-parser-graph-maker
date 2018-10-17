import re
import pandas as pd
from collections import defaultdict
import datetime
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=True)
parser.add_argument("--process", "-p", type=str, required=True)
args = parser.parse_args()
log_text = open(args.file)
content_dict = defaultdict(list)
for line in log_text:
	if line.startswith('top'):
		linecontent = map(lambda x: x.strip(),line.split("top - ")[1].split(","))
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
		linecontent = map(lambda x: x.strip(),line.split("KiB Swap:  ")[1].split(","))
		content_dict['Swap Memory'].append(linecontent)
	if args.process in line:
		subline = {}
		#print line
		linecontent = list(filter(lambda x: x!='',line.split(' ')))
		#print linecontent
		subline['PR']=float(linecontent[2])
		subline['NI']=float(linecontent[3])
		subline['VIRT']=float(linecontent[4]) if 't' not in linecontent[4] else float(linecontent[4].split("t")[0])
		subline['RES']=float(linecontent[5].split("g")[0]) if 't' not in linecontent[5] else float(linecontent[5].split("t")[0])
		subline['SHR']=float(linecontent[6])
		subline['percent_CPU']=float(linecontent[8])
		subline['percent_MEM']=float(linecontent[9])
		
		content_dict['Rest'].append(subline)
		if 'kv_fileload' not in line:
			break

top_line = content_dict['top']
top_line_header = ['complete_time', 'hour_min', 'users', 'load_average_1', 'load_average_2', 'load_average_3']
processed_top_line_header = ['idx','complete_time', 'users', 'load_average_1', 'load_average_2', 'load_average_3']
processed_top_rows = []
for idx,row in enumerate(top_line):
	curr_entry = dict(zip(top_line_header,row))
	processed_row = [idx, datetime.datetime.strptime(curr_entry['complete_time'].split(" up ")[0],"%H:%M:%S").time(), int(curr_entry['users'].strip(" users")), float(curr_entry['load_average_1'].strip("load average: ")), float(curr_entry['load_average_2']), float(curr_entry['load_average_3'])]
	processed_top_rows.append(processed_row)
df = pd.DataFrame(processed_top_rows,columns = processed_top_line_header)
line1=df.plot.line(x='complete_time', y='users')
plt.savefig('line1')
line2=df.plot.line(x='complete_time', y='load_average_1')
plt.savefig('line2')
line3=df.plot.line(x='complete_time', y='load_average_2')
plt.savefig('line3')
line4=df.plot.line(x='complete_time', y='load_average_3')
plt.savefig('line4')
tasks = content_dict['Tasks']
tasks_header = ['total', 'running', 'sleeping', 'stopped', 'zombie']
processed_task_header = ['idx', 'total', 'running', 'sleeping', 'stopped', 'zombie']
task_rows = []
for idx,row in enumerate(tasks):
	zip_entry = zip(tasks_header,row)
	processed_row = [idx]+ list(map(lambda x: int(x[1].strip(" "+x[0])),zip_entry))
	task_rows.append(processed_row)
task_df = pd.DataFrame(task_rows,columns = processed_task_header)

df = pd.merge(df, task_df, on='idx')

line5=df.plot.line(x='complete_time', y='total')
plt.savefig('line5')
line6=df.plot.line(x='complete_time', y='running')
plt.savefig('line6')
line7=df.plot.line(x='complete_time', y='sleeping')
plt.savefig('line7')
line8=df.plot.line(x='complete_time', y='stopped')
plt.savefig('line8')
line9=df.plot.line(x='complete_time', y='zombie')
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
plt.savefig('line10')
line11=df.plot.line(x='complete_time', y='sy')
plt.savefig('line11')
line12=df.plot.line(x='complete_time', y='ni')
plt.savefig('line12')
line13=df.plot.line(x='complete_time', y='id')
plt.savefig('line13')
line14=df.plot.line(x='complete_time', y='wa')
plt.savefig('line14')
line15=df.plot.line(x='complete_time', y='hi')
plt.savefig('line15')
line16=df.plot.line(x='complete_time', y='si')
plt.savefig('line16')
line17=df.plot.line(x='complete_time', y='st')
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
plt.savefig('line18')
line19=df.plot.line(x='complete_time', y='free')
plt.savefig('line19')
line20=df.plot.line(x='complete_time', y='used')
plt.savefig('line20')
line21=df.plot.line(x='complete_time', y='buffer/cache')
plt.savefig('line21')

tasks = content_dict['Swap Memory']
tasks_header = [' total', ' free', ' used', 'rest']
processed_task_header = ['idx', 'total_swap_memory', 'swap_free', 'swap_used', 'swap_avail_mem']
task_rows = []
for idx,row in enumerate(tasks):
	zip_entry = list(zip(tasks_header,row))
	processed_row = [idx]+ list(map(lambda x: float(x[1].strip(" "+x[0])),zip_entry[:-1]))
	rest = zip_entry[-1][1]
	used, swap_mem = rest.split(" used. ")
	used = float(used)
	swap_mem = float(swap_mem.split("+avail Mem")[0])
	processed_row += [used, swap_mem]
	task_rows.append(processed_row)
task_df = pd.DataFrame(task_rows,columns = processed_task_header)
# print task_df

df = pd.merge(df, task_df, on='idx')

line22=df.plot.line(x='complete_time', y='total_swap_memory')
plt.savefig('line22')
line23=df.plot.line(x='complete_time', y='swap_free')
plt.savefig('line23')
line24=df.plot.line(x='complete_time', y='swap_used')
plt.savefig('line24')
line25=df.plot.line(x='complete_time', y='swap_avail_mem')
plt.savefig('line25')

tasks = content_dict['Rest']
tasks_header = ['PR', 'NI', 'VIRT', 'RES', 'SHR', 'percent_CPU', 'percent_MEM']
processed_task_header = ['idx', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'percent_CPU', 'percent_MEM']
task_rows = []
for idx,row in enumerate(tasks):
	row1 = [idx]+[row[x] for x in tasks_header]
	task_rows.append(row1)
task_df = pd.DataFrame(task_rows,columns = processed_task_header)



df = pd.merge(df, task_df, on='idx')

print(df)
line26=df.plot.line(x='complete_time', y='PR')
plt.savefig('line26')
line27=df.plot.line(x='complete_time', y='NI')
plt.savefig('line27')
line28=df.plot.line(x='complete_time', y='VIRT')
plt.savefig('line28')
line29=df.plot.line(x='complete_time', y='RES')
plt.savefig('line29')
line30=df.plot.line(x='complete_time', y='SHR')
plt.savefig('line30')
line31=df.plot.line(x='complete_time', y='percent_CPU')
plt.savefig('line31')
line32=df.plot.line(x='complete_time', y='percent_MEM')
plt.savefig('line32')






	



