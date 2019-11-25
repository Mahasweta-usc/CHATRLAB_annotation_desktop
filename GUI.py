import os, sys

def DevNull():
	pass

sys.stderr = DevNull()
import io
from tkinter import *
import json
import urllib.request as urllib2
import PIL
from PIL import Image, ImageTk
from google.cloud import storage
import certifi
import random
import urllib.request
from urllib.parse import urljoin
from itertools import cycle
import unidecode 
import emoji
#commit

# from process_url import *

print("All imports worked")
count = 0

User=""




def on_closing_entry():
        Query.destroy()
        exit()

class shabnam():

	def bsdk(self):
		global User
		User = self.e.get() # "'{}'".format(self.e.get().replace("'",'"'))
		if not User:
			pass
		else:
			self.frame.destroy()

	#install pip, virtual env, start virtualenv install deps

	def __init__(self,frame):
		self.frame = frame
		self.frame.title("User Log")
		Instr = Label(self.frame,text="User", font=('Helvetica',15,"bold"),borderwidth=10,width=40)
		Instr.grid(row=0,column=0, padx=15, pady=10,sticky=E+W)
		self.e = Entry(self.frame)
		self.e.grid(row=2,column=0, padx=30, pady=10,sticky=E+W)

		enter = Button(self.frame, text="Enter", command=self.bsdk)
		enter.grid(row=4,column=0, padx=200, pady=10,sticky=E+W,columnspan=4)
		
		# self.frame.destroy()


Query = Tk()
p = shabnam(Query)
Query.protocol("WM_DELETE_WINDOW", on_closing_entry)	
Query.mainloop()

MisInf, Polarity, tag =  1,1,[]
Ans1, Ans2, Ans3 = False, False, True

storage_client = storage.Client.create_anonymous_client()
bucket = storage_client.bucket(bucket_name="project_vaxx",user_project=None)

org = bucket.list_blobs(prefix="201", delimiter=None)
# blobs = iter(org)
blobs = []
for i in org:
    try:
        # get the next item
        blobs.append(i) #org._get_next_page_response()
        # do something with element
    except StopIteration:
        # if StopIteration is raised, break from loop
        break

org_len = len(blobs)
cwd = os.getcwd()

temp_file = os.path.join(cwd,"temp.json")



def upload_blob(source, destination_blob_name, bucket_name = "project_vaxx"):
	bucket_t = storage_client.bucket(bucket_name, user_project=None)
	temp = storage.Blob(destination_blob_name, bucket_t)

	temp.upload_from_filename(source)

def download_blob(source_blob_name, destination_file_name, bucket_name = "project_vaxx"):
	bucket_t = storage_client.bucket(bucket_name, user_project=None)
	temp = storage.Blob(source_blob_name, bucket_t)

	temp.download_to_filename(destination_file_name)

def delete_blob(blob_name, bucket_name = "project_vaxx"):
	bucket_t = storage_client.bucket(bucket_name, user_project=None)
	temp = storage.Blob(blob_name, bucket_t)
	# # print('Blob {} deleted.'.format(temp))
	blob = bucket.blob(blob_name)
	name = "xxx-" + blob_name
	blob = bucket_t.rename_blob(blob, name)

def skip_blob(blob_name, bucket_name = "project_vaxx"):
	bucket_t = storage_client.bucket(bucket_name, user_project=None)
	temp = storage.Blob(blob_name, bucket_t)
	# # print('Blob {} deleted.'.format(temp))
	blob = bucket.blob(blob_name)
	name = "yyy-" + blob_name
	blob = bucket_t.rename_blob(blob, name)

        # print(url,response.status_code)

    

class API():


	def clicked_true(self, val):
		global MisInf, Ans1
		MisInf = val
		Ans1 = True

		for key,value in self.label.items():
			if key == val:
				value.config(state=DISABLED)
			else:
				value.config(state="normal")


	def provaxx(self):
		global Polarity, Ans2
		Polarity = 1
		Ans2 = True
		self.pro.config(state=DISABLED)
		self.anti.config(state="normal")
		self.neutral.config(state="normal")

	def antivaxx(self):
		global Polarity, Ans2
		Polarity = -1
		Ans2 = True
		self.pro.config(state="normal")
		self.anti.config(state=DISABLED)
		self.neutral.config(state="normal")

	def neutral(self):
		global Polarity, Ans2
		Polarity = 0
		Ans2 = True
		self.pro.config(state="normal")
		self.neutral.config(state=DISABLED)
		self.anti.config(state="normal")

	
	def tag(self,val):
		global tag

		if val:
			tag.append(val)

			for key,value in self.category.items():
				if key in tag:
					value.config(state=DISABLED)
				else:
					value.config(state="normal")
		else:
			tag = []
			for key,value in self.category.items():
				value.config(state="normal")
		

	def count(self,val):

		# pass
		for key,value in self.label.items():
			value.config(state="normal")

		self.neutral.config(state="normal")
		self.pro.config(state="normal")
		self.anti.config(state="normal")

		for key,value in self.category.items():
			value.config(state="normal")

		self.Label4.configure(text="  Total Posts annotated by {}: {}  ".format(User,self.completed) )


	def submit(self):
		global blobs, MisInf, tag, Polarity, Ans1, Ans2, Ans3
		
			
		if Ans1 and Ans2 and Ans3:
			with open(temp_file,'r+') as json_file:  
				data = json.load(json_file)

			try:
				test = data["Annotations"]
			except:
				data["Annotations"] = {}

			data["Annotations"][User] = {"Label":MisInf,"Polarity":Polarity,"Category":tag}

			with open(temp_file,'w+') as write: 
				json.dump(data,write,indent=4)

			upload_blob(temp_file,self.blob.name)
			# print(data["Annotations"][User])

			self.completed += 1
			# self.marked.append(self.blob.name)
			blobs.pop(blobs.index(self.blob))
			self.count(1)
			self.Update()


		else:
			pass
	  

	def clicked_skip(self):
		global blobs
		for key,value in self.label.items():
			value.config(state="normal")

		self.neutral.config(state="normal")
		self.pro.config(state="normal")
		self.anti.config(state="normal")

		for key,value in self.category.items():
			value.config(state="normal")

		skipped = blobs.pop(blobs.index(self.blob))
		blobs.append(skipped)
		self.count(0)
		self.Update()

	def clicked_delete(self):
		global blobs

		for key,value in self.label.items():
			value.config(state="normal")

		self.neutral.config(state="normal")
		self.pro.config(state="normal")
		self.anti.config(state="normal")

		for key,value in self.category.items():
			value.config(state="normal")

		file_delete = self.blob.name

		delete_blob(file_delete)
		# self.completed += 1
		# self.marked.append(self.blob.name)
		blobs.pop(blobs.index(self.blob))
		self.count(1)
		self.Update()


	def skip_matching(self, gen, value):
	    for v in gen:
	        if v == value:
	            continue
	        yield v

	def Update(self):
		global blobs, Ans1, Ans2, Ans3, count,tag
		Ans1 = False
		Ans2 = False
		Ans3 = True
		tag = []

		self.blobs = iter(blobs)

		if blobs:
			self.blob = next(self.blobs)

		else:
			sys.stdout.write("All Annotations complete\n")
			on_closing()

		try:
			download_blob(self.blob.name,temp_file)
		except:
			self.Update()
	
		with open(temp_file,'r') as ip:
			data2 = json.load(ip)

		try:
			test = data2["Annotations"][User]
			self.completed += 1
			blobs.pop(blobs.index(self.blob))
			self.Update()
		except:
			pass
				
		
		self.count(0)
		with open(temp_file,"r") as ip:
			data = json.load(ip)
		try:
			caption = data["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
		except:
			caption = ""
		try:
			image_text = data['embed_text']
		except:
			image_text = " "
		try:
			image_tags = ", ".join(data['tags'])
		except:
			image_tags = " "

		try:

			try:
				download_blob((self.blob.name).replace(".json",".png"),"image.png","procvaxx")
			except Exception as e:
				# print(e)
				self.Update()

			im = Image.open("image.png") 
			# print("succeeded")
			# print("tik-tok")
			width,height=im.size
			width,height = int(500*new_w),int(500*new_h)
			im = im.resize((width,height))
			photo= ImageTk.PhotoImage(im)

			self.panel.configure(image=photo)
			self.panel.image = photo
			self.text2.config(state=NORMAL)

			self.text2.delete('1.0', END)
			self.text2.insert(END,"***Caption***: ","bold")
			self.text2.insert(END,"{} \n\n".format(caption).encode(encoding='UTF-8',errors='ignore'))
			self.text2.insert(END,"***Image text***: ","bold")
			self.text2.insert(END,"{} \n\n".format(image_text).encode(encoding='UTF-8',errors='ignore'))
			# self.text2.insert(END,"\n\n***URL extracts***:\n","bold")
			# self.text2.insert(END,meta)
			self.text2.config(state=DISABLED)
			# print(data)

		except Exception as e:
			# print(e)
			self.Update()


	def __init__(self, item):
		self.frame = Frame(item,bd=20)
		self.frame.grid(row=0,column=0,sticky=N+S+E+W)
		self.panel = Label(self.frame, borderwidth=-5,bg = "black",anchor=CENTER)
		# self.marked = []

		self.panel.grid(row=0, column = 0,columnspan=4,rowspan=2,sticky=N+S+E+W,padx=(int(35*new_w),int(0*new_w)),pady=(int(20*new_h),int(0*new_h)))

		self.text2 = Text(self.frame, borderwidth= 5,font=("Helvetica", 15), wrap=WORD ,height=15,highlightbackground='white')
		self.text2.tag_configure("bold", font="Helvetica 15 bold")
		scroll = Scrollbar(self.frame, orient='vertical',command=self.text2.yview)
		self.text2.configure(yscrollcommand=scroll.set)
		self.text2.config(state=DISABLED)
		self.text2.grid(row=2, column = 0,rowspan=12,columnspan = 4, sticky=N+S+E+W, padx=(int(30*new_w),int(0*new_w)))
		self.text2.grid_propagate(True)
		self.panel.grid_propagate(True)
		scroll.grid(row=2, column = 3, rowspan=12,columnspan=1,sticky='nse')
		self.frame.grid_columnconfigure(4, weight=1,uniform="tukai")

		self.frame.grid_columnconfigure(5, weight=1,uniform="tukai")
		self.frame.grid_columnconfigure(6, weight=1,uniform="tukai")
		heading1 = Label(self.frame,text="Content Label",anchor=CENTER,font=("Helvetica", 15, "bold"))
		heading1.grid(row=0, column = 5,columnspan=1,pady=(int(35*new_h),int(5*new_h)),sticky=N+E+W)
		heading2 = Label(self.frame,text="Vaccination Bias",anchor=CENTER,font=("Helvetica",15, "bold"))
		heading2.grid(row=0, column = 5,columnspan=1,sticky=S+E+W)

		heading4 = Label(self.frame,text="   Content Type   ",anchor=CENTER,fg="#000066",font=("Helvetica",13, "bold"))
		heading4.grid(row=1, column = 4,columnspan=1, sticky=S+E+W,padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)))
		heading5 = Label(self.frame,text="   Content Style   ",anchor=CENTER,fg="#660066",font=("Helvetica",13, "bold"))
		heading5.grid(row=1, column = 6,columnspan=1,sticky=S+E+W,padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h))) #,padx=(int(5*new_w),int(20*new_w))
		heading3 = Label(self.frame,text="Discussion Topic",anchor=CENTER,font=("Helvetica",13, "bold"),fg="#993333")
		heading3.grid(row=1, column = 5,columnspan=1,sticky=S+E+W, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)))

		self.cat1 = Button(self.frame, text="Misinformation", command=lambda: self.clicked_true(1), highlightbackground='red',highlightcolor='white',anchor=CENTER)

		self.cat1.grid(row=0,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=E+W)

		self.cat2 = Button(self.frame, text="Controversial", command=lambda: self.clicked_true(2), highlightbackground='blue',anchor=CENTER,highlightcolor='white')

		self.cat2.grid(row=0,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=E+W)

		self.cat3 = Button(self.frame, text="Clean", command=lambda: self.clicked_true(3), highlightbackground='green',highlightcolor='white',anchor=CENTER)

		self.cat3.grid(row=0,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=E+W)

		self.tag0 = Button(self.frame, text="Reset Category", command=lambda: self.tag(0), highlightbackground='black',anchor=CENTER,highlightcolor='white')

		self.tag0.grid(row=9,column=5, columnspan=2, padx= (int(60*new_w),int(70*new_w)), pady=(int(5*new_h),int(5*new_h)),sticky=E+W)



		self.anti = Button(self.frame, text="Anti", command=self.antivaxx, highlightbackground='red',anchor=CENTER,highlightcolor='white')

		self.anti.grid(row=1,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(60*new_h),int(5*new_h)),columnspan=1,sticky=N+E+W)

		self.neutral = Button(self.frame, text="Neutral", command=self.neutral, highlightbackground='blue',anchor=CENTER,highlightcolor='white')

		self.neutral.grid(row=1,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(60*new_h),int(5*new_h)),columnspan=1,sticky=N+E+W)

		self.pro = Button(self.frame, text="Pro", command=self.provaxx, highlightbackground='green',anchor=CENTER,highlightcolor='white')

		self.pro.grid(row=1,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(60*new_h),int(5*new_h)),columnspan=1,sticky=N+E+W)

		#Types

		

		self.tag1 = Button(self.frame, text="Ingredients", command=lambda: self.tag(1), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag1.grid(row=2,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag2 = Button(self.frame, text="Efficacy", command=lambda: self.tag(2), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag2.grid(row=3,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag3 = Button(self.frame, text="Autism", command=lambda: self.tag(3), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag3.grid(row=4,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag4 = Button(self.frame, text="SBS/Infant Death", command=lambda: self.tag(4), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag4.grid(row=5,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag5 = Button(self.frame, text="Conspiracy", command=lambda: self.tag(5), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag5.grid(row=6,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag6 = Button(self.frame, text="Vaccination Schedule", command=lambda: self.tag(6), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag6.grid(row=7,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag7 = Button(self.frame, text="Vaccination Rate", command=lambda: self.tag(7), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag7.grid(row=8,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=N+E+W)

		self.tag8 = Button(self.frame, text="Research/Evidence", command=lambda: self.tag(8), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag8.grid(row=9,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=N+E+W)

		self.tag9 = Button(self.frame, text="Herd Immunity", command=lambda: self.tag(9), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag9.grid(row=10,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=N+E+W)

		self.tag10 = Button(self.frame, text="Vaccine Necessity", command=lambda: self.tag(10), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag10.grid(row=11,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=N+E+W)

		self.tag11 = Button(self.frame, text="Vaccine Safety", command=lambda: self.tag(11), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag11.grid(row=12,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=N+E+W)

		

		self.tag12 = Button(self.frame, text="Campaign", command=lambda: self.tag(21), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag12.grid(row=2,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag13 = Button(self.frame, text="Political/Legal", command=lambda: self.tag(22), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag13.grid(row=3,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag14 = Button(self.frame, text="Promotional/Commercial", command=lambda: self.tag(23), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag14.grid(row=4,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag15 = Button(self.frame, text="Faith", command=lambda: self.tag(24), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag15.grid(row=5,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag16 = Button(self.frame, text="Lawsuits", command=lambda: self.tag(25), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag16.grid(row=6,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		#Style

		

		self.tag17 = Button(self.frame, text="Claim", command=lambda: self.tag(31), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag17.grid(row=2,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag18 = Button(self.frame, text="Sarcasm/Irony/Humour", command=lambda: self.tag(32), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag18.grid(row=3,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag19 = Button(self.frame, text="Informative/Reporting", command=lambda: self.tag(33), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag19.grid(row=4,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag20 = Button(self.frame, text="Personal Experience", command=lambda: self.tag(34), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag20.grid(row=5,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)




		self.label = {1:self.cat1,
		2:self.cat2,
		3:self.cat3
		}

		self.category = {1:self.tag1,
		2:self.tag2,
		3:self.tag3,
		4:self.tag4,
		5:self.tag5,
		6:self.tag6,
		7:self.tag7,
		8:self.tag8,
		9:self.tag9,
		10:self.tag10,
		11:self.tag11,
		21:self.tag12,
		22:self.tag13,
		23:self.tag14,
		24:self.tag15,
		25:self.tag16,
		31:self.tag17,
		32:self.tag18,
		33:self.tag19,
		34:self.tag20,
		0:self.tag0
		}


		self.Label4 = Label(self.frame,text= " Total Posts Labeled by {}: 0".format(User),relief="ridge",borderwidth=2,anchor=CENTER,font=("Helvetica", 10, "bold"))
		self.Label4.grid(row=1,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(25*new_h),int(5*new_h)),columnspan=1,sticky=E+W)

		submit = Button(self.frame, text=" Submit ", command=self.submit, highlightbackground='green2',anchor=CENTER)
		# submit.grid(row=5,column=5, columnspan = 1, padx=(int(20*new_w),int(20*new_w)),pady=(int(20*new_h),int(20*new_h)))
		submit.grid(row=11,column=5, columnspan = 2, rowspan=2, padx=(int(25*new_w),int(25*new_w)),pady=(int(5*new_h),int(5*new_h)),sticky=N+S+E+W)

		# forward = Button(self.frame, text=" Next ", command=self.clicked_next, highlightbackground='#3E4149',anchor=CENTER)
		
		

		skip = Button(self.frame, text=" Next ", command=self.clicked_skip, highlightbackground='navy',anchor=CENTER)

		skip.grid(row=10,column=5, padx=(int(60*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),sticky=N+E+W)

		delete = Button(self.frame, text="Delete", command=self.clicked_delete, highlightbackground='red2',anchor=CENTER)
		delete.grid(row=10,column=6, padx=(int(5*new_w),int(70*new_w)),pady=(int(5*new_h),int(5*new_h)),sticky= N+E+W)

		global blobs

		self.completed = 0


		self.count(0)

		# print(self.completed)
		self.Update()

		print("running")



window = Tk()

def on_closing():
	try:
		os.remove("image.png")
		os.remove("temp.json")
		# os.remove("log.json")
	except:
		pass
		
	window.destroy()
	exit()

def signal_handler(signum,frame):
	on_closing()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

new_h = screen_height/1080
new_w = screen_width/1920

try:
	import signal
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)
	signal.signal(signal.SIGHUP, signal_handler)
except:
	pass

window.title("Data Viewer")
window.resizable(width=False, height=False)
obj = API(window)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
