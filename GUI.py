import os, sys
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

from process_url import *

print("All imports worked")
count = 0

User=""

# screen = os.popen("xrandr -q -d :0").readlines()[0]
# print(screen)



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
Ans1, Ans2, Ans3 = False, False, False

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
		global tag, Ans3

		if val:
			tag.append(val)
			Ans3 = True

			for key,value in self.category.items():
				if key in tag:
					value.config(state=DISABLED)
				else:
					value.config(state="normal")
		else:
			Ans3 = False
			tag = []
			for key,value in self.category.items():
				value.config(state="normal")
		

	def count(self):

		for key,value in self.label.items():
			value.config(state="normal")

		self.neutral.config(state="normal")
		self.pro.config(state="normal")
		self.anti.config(state="normal")

		for key,value in self.category.items():
			value.config(state="normal")

		download_blob("record.json","temp2.json")

		with open("temp2.json",'r') as ip:
			data = json.load(ip)


		if User not in data.keys():
			data[User] = 0

		self.completed = data[User]
		self.Label4.configure(text="  " + str(data[User])+ "  " )
		self.Label4.text=str(data[User])

		with open("temp2.json",'w+') as output: 
			json.dump(data,output)

		upload_blob("temp2.json","record.json","project_vaxx")



	def submit(self):
		global blobs, MisInf, tag, Polarity, Ans1, Ans2, Ans3, marked
		
			
		if Ans1 and Ans2 and Ans3:
			with open(temp_file,'r+') as json_file:  
				data = json.load(json_file)
			data["Annotations"][User] = {"Label":MisInf,"Polarity":Polarity,"Category":tag}

			with open(temp_file,'w+') as write: 
				json.dump(data,write,indent=4)
			upload_blob(temp_file,self.blob.name)
			
			download_blob("record.json","temp2.json")

			with open("temp2.json",'r+') as ip:
				data2 = json.load(ip)


			if User not in data2.keys():
				data2[User] = 0
				
			data2[User] += 1
			with open("temp2.json",'w+') as output: 
				json.dump(data2,output)
			upload_blob("temp2.json","record.json","project_vaxx")

			self.completed = data2[User]

			self.count()
			self.marked.append(self.blob.name)
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

		# print(blobs)
		skipped = blobs.pop(blobs.index(self.blob))
		blobs.append(skipped)
		# self.marked.append(self.blob.name)
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
		Ans3 = False
		tag = []
		download_blob('log.json','log.json')
		with open('log.json','r') as ip:
			data = json.load(ip)
		active = [data[key] for key in data.keys()]

		# print(blobs)
		# print(len(self.marked))
		self.blobs = self.skip_matching(blobs, self.marked)

		while(1):
			try:
				self.blob = next(self.blobs)
			except:
				if self.completed == len(blobs):
					sys.stdout.write("All Annotations complete")
				else:
					sys.stdout.write("Files busy. Try Again Later")
				on_closing()

			try:
				download_blob(self.blob.name,temp_file)
			except:
				continue
			
			with open(temp_file,'r') as ip:
				data2 = json.load(ip)

			#If already annotated

			if "Annotations" in data2:
				if User in data2["Annotations"].keys():
					continue
			else:
				data2["Annotations"] = {}

			with open(temp_file,'w+') as write: 
				json.dump(data2,write,indent=4)
			upload_blob(temp_file,self.blob.name)

			#File not open with another user

			if self.blob.name not in active:
				try:
					data[User] = self.blob.name
					with open('log.json','w') as op:
						json.dump(data,op, indent=2)
					upload_blob('log.json','log.json','project_vaxx')
					break
				except:
					continue
		
		self.count()
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

		text = caption + " " + image_text


		url_info = URL_rep(text)

		# text = text

		meta = ""

		for key,value in url_info.items():
			meta += "{} \n : {} \n".format(key,value)
		
		meta = meta.encode(encoding='UTF-8',errors='ignore')

		# text += meta 

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
			self.text2.insert(END,"\n\n***URL extracts***:\n","bold")
			self.text2.insert(END,meta)
			self.text2.config(state=DISABLED)

		except Exception as e:
			# print(e)
			self.Update()


	def __init__(self, Frame):
		self.frame = Frame
		self.frame.title("Data Viewer")
		self.frame.resizable(width=False, height=False)
		self.panel = Label(self.frame, borderwidth=-5,bg = "black",anchor=CENTER)
		self.marked = []

		self.panel.grid(row=0, column = 0,columnspan=4,rowspan=4,sticky=N+S+E+W,padx=(int(35*new_w),int(0*new_w)),pady=(int(20*new_h),int(0*new_h)))

		self.text2 = Text(self.frame, borderwidth= 5,font=("Helvetica", 12), wrap=WORD ,height=15,highlightbackground='white')
		self.text2.tag_configure("bold", font="Helvetica 15 bold")
		scroll = Scrollbar(self.frame, orient='vertical',command=self.text2.yview)
		self.text2.configure(yscrollcommand=scroll.set)
		self.text2.config(state=DISABLED)
		self.text2.grid(row=4, column = 0,rowspan=1,columnspan = 4, sticky=E+W, padx=(int(30*new_w),int(0*new_w)))
		self.text2.grid_propagate(True)
		self.panel.grid_propagate(True)
		scroll.grid(row=4, column = 3, sticky='nse')
		self.frame.grid_columnconfigure(4, weight=1,uniform="tukai")

		self.frame.grid_columnconfigure(5, weight=1,uniform="tukai")
		self.frame.grid_columnconfigure(6, weight=1,uniform="tukai")
		heading1 = Label(self.frame,text="Content Label",anchor=CENTER,font=("Helvetica", 15, "bold"))
		heading1.grid(row=0, column = 5,columnspan=1,sticky=E+W)
		heading2 = Label(self.frame,text="Vaccination Bias",anchor=CENTER,font=("Helvetica",15, "bold"))
		heading2.grid(row=1, column = 5,columnspan=1,sticky=E+W)
		heading3 = Label(self.frame,text="Post Category",anchor=CENTER,font=("Helvetica",15, "bold"))
		heading3.grid(row=2, column = 5,columnspan=1,sticky=E+W)

		self.cat1 = Button(self.frame, text="Misinformation", command=lambda: self.clicked_true(1), highlightbackground='red',highlightcolor='white',anchor=CENTER)

		self.cat1.grid(row=0,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.cat2 = Button(self.frame, text="Controversial", command=lambda: self.clicked_true(2), highlightbackground='blue',anchor=CENTER,highlightcolor='white')

		self.cat2.grid(row=0,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.cat3 = Button(self.frame, text="Clean", command=lambda: self.clicked_true(3), highlightbackground='green',highlightcolor='white',anchor=CENTER)

		self.cat3.grid(row=0,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)



		self.anti = Button(self.frame, text="Anti", command=self.antivaxx, highlightbackground='red',anchor=CENTER,highlightcolor='white')

		self.anti.grid(row=1,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.neutral = Button(self.frame, text="Neutral", command=self.neutral, highlightbackground='blue',anchor=CENTER,highlightcolor='white')

		self.neutral.grid(row=1,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.pro = Button(self.frame, text="Pro", command=self.provaxx, highlightbackground='green',anchor=CENTER,highlightcolor='white')

		self.pro.grid(row=1,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)



		self.tag1 = Button(self.frame, text="Sarcasm/Irony/Humor", command=lambda: self.tag(1), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag1.grid(row=2,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag2 = Button(self.frame, text="Opinion:Argumentative/Advocacy", command=lambda: self.tag(2), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag2.grid(row=2,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)


		self.tag3 = Button(self.frame, text="Opinion:Personal Experience/Inference", command=lambda: self.tag(3), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag3.grid(row=2,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		# self.Label1 = Label(self.frame,text= "Misinformation",relief="ridge",borderwidth=2,anchor=W)
		# self.Label1.grid(row=3,column=4, padx=(int(15*new_w),int(0*new_w)), pady=(int(0*new_h),int(0*new_h)))
		self.tag4 = Button(self.frame, text="Informative/Reporting", command=lambda: self.tag(4), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag4.grid(row=3,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag5 = Button(self.frame, text="Promotional/Commercial", command=lambda: self.tag(5), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag5.grid(row=3,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)


		self.tag6 = Button(self.frame, text="Campaign(Apolitical)", command=lambda: self.tag(6), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag6.grid(row=3,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag8 = Button(self.frame, text="Political/Legal/Social", command=lambda: self.tag(8), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag8.grid(row=4,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=E+W)

		self.tag7 = Button(self.frame, text="Conspiracy", command=lambda: self.tag(7), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag7.grid(row=4,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=E+W)

		self.tag9 = Button(self.frame, text="Others", command=lambda: self.tag(9), highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag9.grid(row=4,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=E+W)

		self.tag0 = Button(self.frame, text="Reset Category", command=lambda: self.tag(0), highlightbackground='black',anchor=CENTER,highlightcolor='white')

		self.tag0.grid(row=4,column=5, padx=(int(50*new_w),int(50*new_w)), pady=(int(0*new_h),int(50*new_h)),columnspan=1,sticky=S+E+W)



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
		0:self.tag0
		}

		self.Label2 = Label(self.frame,text= " Total Posts Labeled by {}:".format(User),relief="ridge",borderwidth=2,anchor=W,font=("Helvetica", 15, "bold"))
		self.Label2.grid(row=5,column=4, padx= (int(15*new_w),int(0*new_w)), pady=(int(0*new_h),int(0*new_h)),sticky=S+E+W)


		# self.Label3 = Label(self.frame,text= "0",relief="ridge",borderwidth=2,anchor=E)
		# self.Label3.grid(row=3,column=6, padx=(int(15*new_w),int(20*new_w)), pady=(int(0*new_h),int(0*new_h)))


		self.Label4 = Label(self.frame,text= "0",relief="ridge",borderwidth=2,anchor=E,font=("Helvetica", 15, "bold"))
		self.Label4.grid(row=5,column=6, padx=(int(15*new_w),int(20*new_w)), pady=(int(0*new_h),int(0*new_h)))

		submit = Button(self.frame, text=" Submit ", command=self.submit, highlightbackground='#3E4149',anchor=CENTER)
		# submit.grid(row=5,column=5, columnspan = 1, padx=(int(20*new_w),int(20*new_w)),pady=(int(20*new_h),int(20*new_h)))
		submit.grid(row=6,column=5, columnspan = 1, padx=(int(20*new_w),int(20*new_w)),pady=(int(20*new_h),int(50*new_h)),sticky=S+E+W)

		# forward = Button(self.frame, text=" Next ", command=self.clicked_next, highlightbackground='#3E4149',anchor=CENTER)
		
		

		skip = Button(self.frame, text=" Next ", command=self.clicked_skip, highlightbackground='#3E4149',anchor=CENTER)

		skip.grid(row=6,column=1, padx=(int(5*new_w),int(5*new_w)), pady=(int(20*new_h),int(50*new_h)),sticky=S+E+W)

		delete = Button(self.frame, text="Delete", command=self.clicked_delete, highlightbackground='#3E4149',anchor=CENTER)
		delete.grid(row=6,column=2, padx=(int(25*new_w),int(0*new_w)),pady=(int(20*new_h),int(50*new_h)),sticky=S+E+W)

		# self.next = Button(self.frame, text="         >>        ", command=self.next,font=('Helvetica',10))

		# self.next.grid(row=5,column=1, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1)
		# self.next.config(state=DISABLED)
		global blobs

		# download_blob("record.json","temp2.json")
		self.completed = 0

		self.count()

		# print(self.completed)
		self.Update()

		print("running")



window = Tk()

def on_closing():
	download_blob("log.json","log.json")

	with open("log.json",'r') as ip:
		data = json.load(ip)
	# for key,value in data.items():
	data[User] = ""
	with open("log.json",'w+') as output: 
		json.dump(data,output)

	upload_blob("log.json","log.json","project_vaxx")
	os.remove("image.png")
	os.remove("temp.json")
	os.remove("temp2.json")
	os.remove("log.json")
	window.destroy()
	exit()


screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
# print(screen_width,screen_height)

new_h = screen_height/1080
new_w = screen_width/1920

# print([new_h,new_w])

obj = API(window)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
