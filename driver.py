from tkinter import *
import os
import io
import json
import urllib.request as urllib2
from google.cloud import storage
import PIL
from PIL import Image, ImageTk
# from google.cloud import storage
storage_client = storage.Client()
bucket = storage_client.get_bucket("project_vaxx")

blobs = bucket.list_blobs()

blobs = iter(blobs)
blob = blobs.__next__()
cwd = os.getcwd()

temp_file = os.path.join(cwd,"temp.json")
User = ""
# data["test"] = {}
# with open(temp_file,'w') as write:
# 	json.dump(data,write)

def upload_blob(source, destination_blob_name, bucket_name = "labeled_vaxx"):
	"""Uploads a file to the bucket."""
    # storage_client = storage.Client()
	bucket_t = storage_client.get_bucket(bucket_name)
	temp = bucket_t.blob(destination_blob_name)

	temp.upload_from_filename(source)

def download_blob(source_blob_name, destination_file_name, bucket_name = "project_vaxx"):
	bucket_t = storage_client.get_bucket(bucket_name)
	temp = bucket_t.blob(source_blob_name)

	temp.download_to_filename(destination_file_name)



def delete_blob(blob_name,bucket_name = "project_vaxx"):
	bucket_t = storage_client.get_bucket(bucket_name)
	temp = bucket_t.blob(blob_name)
	temp.delete()


# def copy_blob(bucket_name, blob_name, new_bucket_name, new_blob_name):
#     """Copies a blob from one bucket to another with a new name."""
#     storage_client = storage.Client()
#     source_bucket = storage_client.get_bucket(bucket_name)
#     source_blob = source_bucket.blob(blob_name)
#     destination_bucket = storage_client.get_bucket(new_bucket_name)

#     new_blob = source_bucket.copy_blob(
#         source_blob, destination_bucket, new_blob_name)


def clicked_true():
	with open(temp_file,'r') as json_file:  
		data = json.load(json_file)
		data["Label"]=1
		data["User"] = User
	with open(temp_file, 'w') as write:
		json.dump(data,write)
	global blob, blobs
	upload_blob(temp_file,blob.name)
	file_delete = blob.name
	# blob = blobs.__next__()
	delete_blob(file_delete)
	Update()




def clicked_false():
	with open(temp_file,'r') as json_file:  
		data = json.load(json_file)

		data["Label"] = 0
		data["User"] = User
	with open(temp_file,'w') as write:
		json.dump(data,write)
	global blob, blobs
	upload_blob(temp_file,blob.name)
	temp = blob.name
	file_delete = blob.name
	# blob = blobs.__next__()
	delete_blob(file_delete)
	Update()
    


def clicked_skip():
	global blob, blobs
	# blob = blobs.__next__()
	Update()

def clicked_delete():
	global blob, blobs
	file_delete = blob.name
	# blob = blobs.__next__()
	delete_blob(file_delete)
	Update()

def Update():
	global blob, blobs
	try:
		blob = blobs.__next__()
	except:
		window.destroy()
	download_blob(blob.name,temp_file)
	with open(temp_file,"r") as input:
		data = json.load(input)
	caption = data["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
	# print("Number of elements",len(blobs))
	URL = data["node"]["display_url"]
	raw_data = urllib2.urlopen(URL).read()
	im = Image.open(io.BytesIO(raw_data))
	photo= ImageTk.PhotoImage(im)
	# text1.image_create(END,image=photo)
	panel.configure(image=photo)
	panel.image = photo
	text2.config(state=NORMAL)

	text2.delete('1.0', END)
	text2.insert(END,'\n')
	text2.insert(END,caption)
	text2.config(state=DISABLED)

def Minimize():
	window.wm_attributes("-fullscreen",False)

def Maximize():
	window.wm_attributes("-fullscreen",True)

def get_info():
	global User
	User = e.get()
	if not User:
		pass
	else:
		Query.destroy()

Query = Tk()
Query.title("User Log")
Query.geometry('500x200')
Instr = Label(Query,text="Username entry")
Instr.pack(fill="none",expand="True")
e = Entry(Query)
e.pack(fill="none", expand=True)
enter = Button(Query, text="Enter", command= get_info)
enter.pack(fill="none", expand=True,side=BOTTOM)
Query.mainloop()


window = Tk()
window.wm_attributes("-fullscreen", True)
window.title("Data Viewer")

window.geometry('1000x800')


# frame = Frame(window, highlightbackground="green", highlightcolor="green", highlightthickness=1, width=100, height=100, bd= 0)
# frame.pack()
# frame.pack_propagate(False)
# frame = Frame(window)
# frame.pack(side=LEFT)

# frame = Frame(window)
# frame.pack(side=RIGHT)

# frame = Frame(window)
# frame.pack(side=BOTTOM)

true = Button(window, text="Misinformation", command=clicked_true)

true.pack(side=BOTTOM)

false = Button(window, text="Acceptable", command=clicked_false)

false.pack(side=BOTTOM)

skip = Button(window, text="Skip", command=clicked_skip)

skip.pack(side=BOTTOM)

delete = Button(window, text="Delete", command=clicked_delete)

delete.pack(side=BOTTOM)

delete = Button(window, text="Minimize", command=Minimize)

delete.pack(side=BOTTOM, anchor="se")

delete = Button(window, text="Maximize", command=Maximize)

delete.pack(side=BOTTOM, anchor="sw")






download_blob(blob.name,temp_file)


with open(temp_file,"r") as input:
	data = json.load(input)
caption = data["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
# caption = "Hello"
URL = data["node"]["display_url"]

raw_data = urllib2.urlopen(URL).read()
im = Image.open(io.BytesIO(raw_data))
# text1 = Text(window, height=500, width=400)
photo= ImageTk.PhotoImage(im)
# text1.insert(END,'\n')
# text1.image_create(END, image=photo)
panel = Label(window, image=photo, borderwidth=40, relief="solid")
panel.pack(side=LEFT, fill="both", expand="True")

text2 = Text(window,borderwidth=4,font=("Times New Roman", 18))
scroll = Scrollbar(window, command=text2.yview)
text2.configure(yscrollcommand=scroll.set)
text2.insert(END,'\n')
text2.insert(END, caption)
text2.config(state=DISABLED)
text2.pack(side=RIGHT,anchor="ne",fill="both",expand="True")

scroll.pack(side=RIGHT, fill=Y)

# labelframe = LabelFrame(text2)
# labelframe.pack(fill="both", expand="yes")
window.mainloop()