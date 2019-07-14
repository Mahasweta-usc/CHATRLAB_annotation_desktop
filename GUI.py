import os, sys
import io
from tkinter import *
import json
import urllib.request as urllib2
import PIL
from PIL import Image, ImageTk
from google.cloud import storage
import certifi

print("All imports worked")
count = 0

User=""

# screen = os.popen("xrandr -q -d :0").readlines()[0]
# print(screen)

def on_closing():
		upload_blob("temp2.json","record.json","project_vaxx")
		window.destroy()
		exit()

def on_closing_entry():
        Query.destroy()
        exit()

class shabnam():

	def bsdk(self):
		global User
		User = self.e.get()
		if not User:
			pass
		else:
			self.frame.destroy()

	#install pip, virtual env, start virtualenv install deps

	def __init__(self,frame):
		self.frame = frame
		self.frame.title("User Log")
		Instr = Label(self.frame,text="User", font=('arial,10'),borderwidth=10,width=40)
		Instr.grid(row=0,column=0, padx=15, pady=10,sticky=E+W)
		self.e = Entry(self.frame)
		self.e.grid(row=2,column=0, padx=15, pady=10,sticky=E+W)

		enter = Button(self.frame, text="Enter", command=self.bsdk)
		enter.grid(row=4,column=0, padx=10, pady=10,sticky=E+W,columnspan=4)
		
		# self.frame.destroy()


Query = Tk()
p = shabnam(Query)
Query.protocol("WM_DELETE_WINDOW", on_closing_entry)	
Query.mainloop()

MisInf, Polarity, tag =  1,1,0
Ans1, Ans2, Ans3 = False, False, False

storage_client = storage.Client.create_anonymous_client()
bucket = storage_client.bucket(bucket_name="project_vaxx",user_project=None)

blobs = bucket.list_blobs(prefix="201", delimiter=None)
blobs = iter(blobs)
cwd = os.getcwd()

temp_file = os.path.join(cwd,"temp.json")

def upload_blob(source, destination_blob_name, bucket_name = "labeled_vaxx"):
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

class API():

	def clicked_true(self):
		self.true.config(state=DISABLED)
		self.false.config(state="normal")
		global MisInf, Ans1
		MisInf = 1
		Ans1 = True


	def clicked_false(self):
		self.false.config(state=DISABLED)
		self.true.config(state="normal")
		global MisInf, Ans1
		MisInf = 0
		Ans1 = True

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

	def tag(self):
		global tag, Ans3
		tag = 1
		Ans3 = True
		self.notag.config(state="normal")
		self.tag.config(state=DISABLED)

	def notag(self):
		global tag, Ans3
		tag = 0
		Ans3 = True
		self.notag.config(state=DISABLED)
		self.tag.config(state="normal")

	def count(self):

		
		self.true.config(state="normal")
		self.false.config(state="normal")
		self.pro.config(state="normal")
		self.anti.config(state="normal")
		self.neutral.config(state="normal")
		self.tag.config(state="normal")
		self.notag.config(state="normal")
		# download_blob("record.json","temp2.json")
		with open("temp2.json",'r') as input:
			data = json.load(input)
		count1 = data["Misinformation"]
		count2 = data["Others"]
		self.Label3.configure(text="  " + str(count1) + "  ")
		self.Label3.text = str(count1)
		self.Label4.configure(text="  " + str(count2)+ "  " )
		self.Label4.text=str(count2)

	def submit(self):
		global blobs, MisInf, Polarity, Ans1
		with open(temp_file,'r+') as json_file:  
			data = json.load(json_file)
			
		if Ans1 and Ans2 and Ans3:
			data["User"] = User
			data["Label"] = MisInf
			data["Polarity"] = Polarity
			data['Compound'] = tag
			with open(temp_file,'w+') as write: 
				json.dump(data,write,indent=4)
			upload_blob(temp_file,self.blob.name)
			file_delete = self.blob.name
			delete_blob(file_delete)
			
			with open("temp2.json",'r+') as input:
				data2 = json.load(input)
			if MisInf == 1:
				data2["Misinformation"] = data2["Misinformation"] + 1
			else:
				data2["Others"] = data2["Others"] + 1
			with open("temp2.json",'w+') as output: 
				json.dump(data2,output)
			# print(data2)
			# upload_blob("temp2.json","record.json","project_vaxx")
			self.true.config(state="normal")
			self.false.config(state="normal")
			self.pro.config(state="normal")
			self.anti.config(state="normal")
			self.neutral.config(state="normal")
			self.tag.config(state="normal")
			self.notag.config(state="normal")
			self.count()
			upload_blob("temp2.json","record.json","project_vaxx")
			self.Update()


		else:
			pass
	  

	def clicked_next(self):
		global blobs
		self.true.config(state="normal")
		self.false.config(state="normal")
		self.pro.config(state="normal")
		self.anti.config(state="normal")
		self.neutral.config(state="normal")
		self.tag.config(state="normal")
		self.notag.config(state="normal")
		self.Update()

	def clicked_skip(self):
		global blobs
		self.true.config(state="normal")
		self.false.config(state="normal")
		self.pro.config(state="normal")
		self.anti.config(state="normal")
		self.neutral.config(state="normal")
		self.tag.config(state="normal")
		self.notag.config(state="normal")

		file_skip = self.blob.name

		skip_blob(file_skip)
		self.Update()

	def clicked_delete(self):
		global blobs
		self.true.config(state="normal")
		self.false.config(state="normal")
		self.pro.config(state="normal")
		self.anti.config(state="normal")
		self.neutral.config(state="normal")
		self.tag.config(state="normal")
		self.notag.config(state="normal")

		file_delete = self.blob.name

		delete_blob(file_delete)
		self.Update()

	def next(self):
		URL = next(self.URL)
		raw_data = urllib2.urlopen(URL).read()
		im = Image.open(io.BytesIO(raw_data))
		width,height=im.size
		width,height = int(width*new_w),int(height*new_h)
		# print(width,height)
		im = im.resize((width,height))
		print("Yes\n")
		photo= ImageTk.PhotoImage(im)
		self.panel.configure(image=photo)
		self.panel.image = photo

	def Update(self):
		global blobs, Ans1, Ans2, Ans3, count
		Ans1 = False
		Ans2 = False
		Ans3 = False

		try:
			self.blob = next(blobs)
			print(self.blob)
		except:
			self.frame.destroy()

		# self.count()

		download_blob(self.blob.name,temp_file)
		with open(temp_file,"r") as input:
			data = json.load(input)
		# print(data)
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

		text = "***Caption***: {} \n\n ***Image Text***: {} \n\n ***Image Tags***: {}".format(caption,image_text,image_tags)
		url = data["node"]["display_url"]
		

		try:
			URL = url
			# print(URL)
			try:
				
				raw_data = urllib2.urlopen(URL, timeout=60, verify=False).read()
			except:
				raw_data = urllib2.urlopen(URL, timeout=60, cafile=certifi.where()).read()
			im = Image.open(io.BytesIO(raw_data))
			print("tik-tok")
			width,height=im.size
			width,height = int(500*new_w),int(500*new_h)
			im = im.resize((width,height))
			photo= ImageTk.PhotoImage(im)

			self.panel.configure(image=photo)
			self.panel.image = photo
			self.text2.config(state=NORMAL)

			self.text2.delete('1.0', END)
			# self.text2.insert(END,'\n')
			self.text2.insert(END,text)
			self.text2.config(state=DISABLED)

		except:
			self.Update()


	def __init__(self, Frame):
		self.frame = Frame
		self.frame.title("Data Viewer")
		self.frame.resizable(width=False, height=False)
		photo= ImageTk.PhotoImage(file="startup.png")
		self.panel = Label(self.frame,image=photo, borderwidth=-5,bg = "black",anchor=CENTER)
		# # self.panel.pack(side=LEFT, fill="both", expand="True")
		
		self.panel.grid(row=0, column = 0,columnspan=4,rowspan=4,sticky=N+S+E+W,padx=(int(35*new_w),int(0*new_w)),pady=(int(20*new_h),int(0*new_h)))

		self.text2 = Text(self.frame, borderwidth= 5,font=("arial", 12), wrap=WORD,height=5,highlightbackground='white')
		scroll = Scrollbar(self.frame, orient='vertical',command=self.text2.yview)
		self.text2.configure(yscrollcommand=scroll.set)
		self.text2.config(state=DISABLED)
		self.text2.grid(row=4, column = 0,rowspan=1,columnspan = 4, sticky=E+W, padx=(int(30*new_w),int(0*new_w)))
		self.text2.grid_propagate(True)
		self.panel.grid_propagate(True)
		scroll.grid(row=4, column = 3, sticky='nse')

		# self.frame.grid_columnconfigure(0, weight=1)
		# self.frame.grid_columnconfigure(1, weight=4)
		# self.frame.grid_columnconfigure(2, weight=4)
		# self.frame.grid_columnconfigure(3, weight=0)
		self.frame.grid_columnconfigure(4, weight=1,uniform="tukai")

		self.frame.grid_columnconfigure(5, weight=1,uniform="tukai")
		self.frame.grid_columnconfigure(6, weight=1,uniform="tukai")

		# self.frame.grid_rowconfigure(0, weight=5)
		# self.frame.grid_rowconfigure(1, weight=5)
		# self.frame.grid_rowconfigure(2, weight=5)
		# self.frame.grid_rowconfigure(3, weight=5)
		# self.frame.grid_rowconfigure(4, weight=1)
		# self.frame.grid_rowconfigure(5, weight=2)
		# self.frame.grid_rowconfigure(6, weight=4)
		# self.frame.grid_rowconfigure(7, weight=4)
		heading1 = Label(self.frame,text="Misinformation",anchor=CENTER,font=("arial", 10))
		heading1.grid(row=0, column = 5,columnspan=1,sticky=E+W)
		heading2 = Label(self.frame,text="Vaccination Bias",anchor=CENTER,font=("arial",10))
		heading2.grid(row=1, column = 5,columnspan=1,sticky=E+W)

		self.true = Button(self.frame, text="True", command=self.clicked_true, highlightbackground='red',highlightcolor='white',anchor=CENTER)

		self.true.grid(row=0,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.false = Button(self.frame, text="False", command=self.clicked_false, highlightbackground='green',highlightcolor='white',anchor=CENTER)

		self.false.grid(row=0,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.anti = Button(self.frame, text="Anti", command=self.antivaxx, highlightbackground='red',anchor=CENTER,highlightcolor='white')

		self.anti.grid(row=1,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.neutral = Button(self.frame, text="Neutral", command=self.neutral, highlightbackground='blue',anchor=CENTER,highlightcolor='white')

		self.neutral.grid(row=1,column=5, padx=(int(5*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.pro = Button(self.frame, text="Pro", command=self.provaxx, highlightbackground='green',anchor=CENTER,highlightcolor='white')

		self.pro.grid(row=1,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.tag = Button(self.frame, text="Sarcasm/Irony/Humor", command=self.tag, highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.tag.grid(row=2,column=4, padx=(int(20*new_w),int(5*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.notag = Button(self.frame, text="None", command=self.notag, highlightbackground='#3E4149',anchor=CENTER,highlightcolor='white')

		self.notag.grid(row=2,column=6, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1,sticky=S+E+W)

		self.Label1 = Label(self.frame,text= "Misinformation",relief="ridge",borderwidth=2,anchor=W)
		self.Label1.grid(row=3,column=4, padx=(int(15*new_w),int(0*new_w)), pady=(int(0*new_h),int(0*new_h)))


		self.Label2 = Label(self.frame,text= " Other posts ",relief="ridge",borderwidth=2,anchor=W)
		self.Label2.grid(row=4,column=4, padx= (int(15*new_w),int(0*new_w)), pady=(int(0*new_h),int(0*new_h)))


		self.Label3 = Label(self.frame,text= "0",relief="ridge",borderwidth=2,anchor=E)
		self.Label3.grid(row=3,column=6, padx=(int(15*new_w),int(20*new_w)), pady=(int(0*new_h),int(0*new_h)))


		self.Label4 = Label(self.frame,text= "0",relief="ridge",borderwidth=2,anchor=E)
		self.Label4.grid(row=4,column=6, padx=(int(15*new_w),int(20*new_w)), pady=(int(0*new_h),int(0*new_h)))

		submit = Button(self.frame, text=" Submit ", command=self.submit, highlightbackground='#3E4149',anchor=CENTER)
		submit.grid(row=5,column=5, columnspan = 1, padx=(int(20*new_w),int(20*new_w)),pady=(int(20*new_h),int(20*new_h)))

		forward = Button(self.frame, text=" Next ", command=self.clicked_next, highlightbackground='#3E4149',anchor=CENTER)
		forward.grid(row=6,column=5, columnspan = 1, padx=(int(20*new_w),int(20*new_w)),pady=(int(20*new_h),int(20*new_h)))
		

		skip = Button(self.frame, text=" Skip ", command=self.clicked_skip, highlightbackground='#3E4149',anchor=W)

		skip.grid(row=6,column=1, padx=(int(5*new_w),int(5*new_w)), pady=(int(20*new_h),int(20*new_h)))

		delete = Button(self.frame, text="Delete", command=self.clicked_delete, highlightbackground='#3E4149',anchor=E)
		delete.grid(row=6,column=2, padx=(int(25*new_w),int(0*new_w)),pady=(int(20*new_h),int(20*new_h)))

		# self.next = Button(self.frame, text="         >>        ", command=self.next,font=('arial',10))

		# self.next.grid(row=5,column=1, padx=(int(5*new_w),int(30*new_w)), pady=(int(5*new_h),int(5*new_h)),columnspan=1)
		# self.next.config(state=DISABLED)
		global blobs

		download_blob("record.json","temp2.json")
		self.count()

		self.Update()

		print("running")



window = Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
print(screen_width,screen_height)

new_h = screen_height/1080
new_w = screen_width/1920

print([new_h,new_w])

obj = API(window)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()