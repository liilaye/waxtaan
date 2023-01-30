from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
import pymysql
import re
import hashlib
import socket
import time
import threading
import random
import smtplib
from email.mime.text import MIMEText
import struct
import pickle

class Login(tk.Tk):
	def __init__(self,window):
		self.root = window
		self.root.title("WaxxTan")
		self.root.geometry("1000x600")
		self.root.configure(bg = "#ffffff")
		self.root.resizable(False,False)
		self.loginform()

	def loginform(self):
		self.root.geometry("1000x600")
		self.canvas = Canvas(
		    self.root,
		    bg = "#FFFFFF",
		    height = 600,
		    width = 1000,
		    bd = 0,
		    highlightthickness = 0,
		    relief = "ridge")
		self.canvas.place(x = 0, y = 0)

		self.background_img = PhotoImage(file = f"img/background.png")
		background = self.canvas.create_image(
		    500.0, 300.0,
		    image=self.background_img)

		self.entry0_img = PhotoImage(file = f"img/img_textBox0.png")
		entry0_bg = self.canvas.create_image(
		    714.5, 260.0,
		    image = self.entry0_img)

		self.name = Entry(
		    bd = 0,
		    bg = "#ffffff",
		    highlightthickness = 0)

		self.name.place(
		    x = 531.0, y = 233,
		    width = 367.0,
		    height = 52)

		self.entry1_img = PhotoImage(file = f"img/img_textBox1.png")
		entry1_bg = self.canvas.create_image(
		    710.5, 360.0,
		    image = self.entry1_img)

		self.password = Entry(
		    bd = 0,
		    show=".",
		    bg = "#ffffff",
		    highlightthickness = 0)

		self.password.place(
		    x = 527.0, y = 333,
		    width = 367.0,
		    height = 52)

		self.img0 = PhotoImage(file = f"img/img0.png")
		b0 = Button(
		    image = self.img0,
		    borderwidth = 0,
		    highlightthickness = 0,
		    cursor="hand2",
		    command = self.Register,
		    relief = "flat")

		b0.place(
		    x = 722, y = 429,
		    width = 183,
		    height = 40)

		self.img1 = PhotoImage(file = f"img/img1.png")
		b1 = Button(
		    image = self.img1,
		    borderwidth = 0,
		    highlightthickness = 0,
		    cursor="hand2",
		    command = self.login,
		    relief = "flat")

		b1.place(
		    x = 528, y = 429,
		    width = 183,
		    height = 40)

		self.img2 = PhotoImage(file = f"img/img2.png")
		b2 = Button(
		    image = self.img2,
		    borderwidth = 0,
		    highlightthickness = 0,
		    cursor="hand2",
		    command = self.resetpassword,
		    relief = "flat")

		b2.place(
		    x = 522, y = 486,
		    width = 183,
		    height = 40)
	def resetpassword(self):
		self.root.geometry("500x600")
		self.canvas2 = Canvas(
		    self.root,
		    bg = "#FFFFFF",
		    height = 600,
		    width = 500,
		    bd = 0,
		    highlightthickness = 0,
		    relief = "ridge")
		self.canvas2.place(x = 0, y = 0)

		self.background_img = PhotoImage(file = f"img/imgbackground.png")
		background = self.canvas2.create_image(
		    250.0, 300.0,
		    image= self.background_img)

		self.entry0_img = PhotoImage(file = f"img/imgimg_textBox0.png")
		entry0_bg = self.canvas2.create_image(
		    250.0, 158.5,
		    image = self.entry0_img)

		self.email = Entry(
		    bd = 0,
		    bg = "#fffcfc",
		    highlightthickness = 0)

		self.email.place(
		    x = 108.5, y = 134,
		    width = 283.0,
		    height = 47)

		self.entry1_img = PhotoImage(file = f"img/imgimg_textBox1.png")
		entry1_bg = self.canvas2.create_image(
		    250.0, 409.5,
		    image = self.entry1_img)

		self.code= Entry(
		    bd = 0,
		    bg = "#fffcfc",
		    highlightthickness = 0)

		self.code.place(
		    x = 108.5, y = 385,
		    width = 283.0,
		    height = 47)

		self.img0 = PhotoImage(file = f"img/imgimg0.png")
		b0 = Button(
		    image = self.img0,
		    borderwidth = 0,
		    highlightthickness = 0,
		    command = self.sendotp,
		    relief = "flat")

		b0.place(
		    x = 135, y = 222,
		    width = 233,
		    height = 49)

		self.img1 = PhotoImage(file = f"img/imgimg1.png")
		b1 = Button(
		    image = self.img1,
		    borderwidth = 0,
		    highlightthickness = 0,
		    command = self.validateotp,
		    relief = "flat")

		b1.place(
		    x = 135, y = 473,
		    width = 233,
		    height = 49)

		self.img2 = PhotoImage(file = f"img/imgimg2.png")
		b2 = Button(
		    image = self.img2,
		    borderwidth = 0,
		    highlightthickness = 0,
		    command = self.loginform,
		    relief = "flat")

		b2.place(
		    x = 26, y = 15,
		    width = 49,
		    height = 39)
	def sendotp(self):
		try :
			con = pymysql.connect(host='localhost',user='root',password='passer',database='waxxtan')
			cur = con.cursor()
			email = self.email.get()
			cur.execute('select * from client where email=%s',(self.email.get()))
			row = cur.fetchone()
			if row == None :
				messagebox.showerror("Erreur", "Utilisateur introuvable", parent = self.root)
			else :
				self.otp = "".join([str(random.randint(0,9)) for i in range(4)])
				server = smtplib.SMTP('smtp.gmail.com',587)
				server.starttls()
				server.login('waxxtan@gmail.com','isadbnathspqtxya')
				message = MIMEText("Votre code est :"+self.otp)
				message['Subject'] = "Code de recupération de mot de passe"
				message['From'] = "waxxtan@gmail.com"
				message['To'] = self.email.get()
				msg = 'Votre code est : '+self.otp
				print(self.email.get()+''+msg)
				receiver = str(self.email.get())
				server.sendmail('waxxtan@gmail.com',f'{self.email.get()}',message.as_string())
				server.quit()
				messagebox.showinfo("Info",f"Code envoyé.Veuillez vérifier votre boite mail")
				
		except Exception as es:
			messagebox.showerror("Erreur", f"Erreur due à : {str(es)}", parent = self.root)
	
	def validateotp(self) : 
		code = self.code.get()
		if code == self.otp :
			self.chpass()
		else :
			messagebox.showerror("Erreur","Code erroné", parent = self.root)
	
	def chpass(self):
		self.root.geometry("1000x600")
		self.canvas = Canvas(
		    window,
		    bg = "#FFFFFF",
		    height = 600,
		    width = 1000,
		    bd = 0,
		    highlightthickness = 0,
		    relief = "ridge")
		self.canvas.place(x = 0, y = 0)

		self.background_img = PhotoImage(file = f"img/back.png")
		background = self.canvas.create_image(
		    500.0, 300.0,
		    image=self.background_img)

		self.entry0_img = PhotoImage(file = f"img/textBox0.png")
		entry0_bg = self.canvas.create_image(
		    210.0, 231.5,
		    image = self.entry0_img)

		self.mdp = Entry(
		    bd = 0,
		    show=".",
		    bg = "#ffffff",
		    highlightthickness = 0)

		self.mdp.place(
		    x = 83.5, y = 207,
		    width = 253.0,
		    height = 47)

		self.entry1_img = PhotoImage(file = f"img/textBox1.png")
		entry1_bg = self.canvas.create_image(
		    210.0, 379.5,
		    image = self.entry1_img)

		self.confmdp = Entry(
		    bd = 0,
		    show=".",
		    bg = "#ffffff",
		    highlightthickness = 0)

		self.confmdp.place(
		    x = 83.5, y = 355,
		    width = 253.0,
		    height = 47)

		self.img0 = PhotoImage(file = f"img/button.png")
		b0 = Button(
		    image = self.img0,
		    borderwidth = 0,
		    cursor = "hand2",
		    highlightthickness = 0,
		    command = self.changepassword,
		    relief = "flat")

		b0.place(
		    x = 38, y = 448,
		    width = 384,
		    height = 90)	
	
	def changepassword(self) : 
		try : 
			con = pymysql.connect(host='localhost',user='root',password='passer',database='waxxtan')
			cur = con.cursor()
			if self.mdp.get() != self.confmdp.get() :
				messagebox.showerror("Error", "Les mots de passe ne correspondent pas", parent = self.root)
			else : 
				passsword  = self.mdp.get()
				cur.execute("update client set password = %s",(self.mdp.get()))
				messagebox.showinfo("Info","Mot de passe modifié ave succes", parent = self.root)
				self.loginform()
		except Exception as es:
				messagebox.showerror("Error", f"Erreur due à : {str(es)}", parent = self.root)
			
	def login(self):	
		if self.name.get() =="" or self.password.get() == "":
			messagebox.showerror("Error", "Veuillez remplir tous les champs", parent = self.root)
		else:
			try:
				con=pymysql.connect(host='localhost',user='root',password='passer',database='waxxtan')
				cur=con.cursor()
				password = self.password.get()
				encoded=password.encode()
				key = hashlib.sha256(encoded)
				cur.execute('select * from client where username=%s and password=%s',(self.name.get(),str(key.hexdigest())))
				print(f"name : {self.name.get()}")
				print(f"password: {str(key.hexdigest())}")
				row=cur.fetchone()
				if row == None:
					messagebox.showerror("Error", "Verifiez les informations saisies", parent = self.root)
				else:
					self.appscreen()
					con.close()
			except Exception as es:
				messagebox.showerror("Error", f"Erreur due à : {str(es)}", parent = self.root)	
	def Register(self):
		self.canvas1 = Canvas(
			    window,
			    bg = "#FFFFFF",
			    height = 559,
			    width = 948,
			    bd = 0,
			    highlightthickness = 0,
			    relief = "ridge")
		self.canvas1.place(x = 0, y = 0)

		self.background_img1 = PhotoImage(file = f"img/background1.png")
		background = self.canvas1.create_image(
		    474.0, 279.5,
		    image=self.background_img1)

		self.entry0_img1 = PhotoImage(file = f"img/img_textBox01.png")
		entry0_bg = self.canvas1.create_image(
		    238.5, 180.0,
		    image = self.entry0_img1)

		self.name1 = Entry(
		    bd = 0,
		    bg = "#ffffff",
		    highlightthickness = 0)

		self.name1.place(
		    x = 68.0, y = 155,
		    width = 341.0,
		    height = 48)

		self.entry1_img1 = PhotoImage(file = f"img/img_textBox11.png")
		entry1_bg = self.canvas1.create_image(
		    238.5, 279.0,
		    image = self.entry1_img1)

		self.mail = Entry(
		    bd = 0,
		    bg = "#ffffff",
		    highlightthickness = 0)

		self.mail.place(
		    x = 68.0, y = 254,
		    width = 341.0,
		    height = 48)

		self.entry2_img1 = PhotoImage(file = f"img/img_textBox21.png")
		entry2_bg = self.canvas1.create_image(
		    170.0, 394.5,
		    image = self.entry2_img1)

		self.password1 = Entry(
		    bd = 0,
		    show=".",
		    bg = "#ffffff",
		    highlightthickness = 0)

		self.password1.place(
		    x = 59.5, y = 369,
		    width = 221.0,
		    height = 49)

		self.entry3_img1 = PhotoImage(file = f"img/img_textBox31.png")
		entry3_bg = self.canvas1.create_image(
		    452.0, 394.5,
		    image = self.entry3_img1)

		self.confirmpass = Entry(
		    bd = 0,
		    show=".",
		    bg = "#ffffff",
		    highlightthickness = 0)

		self.confirmpass.place(
		    x = 341.5, y = 369,
		    width = 221.0,
		    height = 49)

		self.img01 = PhotoImage(file = f"img/img01.png")
		b0 = Button(
		    image = self.img01,
		    borderwidth = 0,
		    highlightthickness = 0,
		    command = self.register,
		    cursor = "hand2",
		    relief = "flat")

		b0.place(
		    x = 131, y = 461,
		    width = 320,
		    height = 37)
		self.img11 = PhotoImage(file = f"img/img11.png")
		b1 = Button(
		    image = self.img11,
		    borderwidth = 0,
		    highlightthickness = 0,
		    cursor = "hand2",
		    command = self.loginform,
		    relief = "flat")

		b1.place(
		    x = 902, y = 30,
		    width = 54,
		    height = 46)

	def register(self):
		regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
		if self.name1.get() =="" or self.password1.get() == "" or self.mail.get() =="" or self.confirmpass.get() =="":
			messagebox.showerror("Error", "Veuillez remplir tous les champs", parent = self.root)
		elif self.password1.get() != self.confirmpass.get() : 
			messagebox.showerror("Error", "Les mots de passe ne correspondent pas", parent = self.root)
		elif re.fullmatch(regex,self.mail.get()) == None:
			messagebox.showerror("Error", "Format d'email non valide", parent = self.root)
		else: 
			try:
				con=pymysql.connect(host='localhost',user='root',password='passer',database='waxxtan')
				cur=con.cursor()
				cur.execute('select * from client where email=%s',(self.mail.get()))
				row=cur.fetchone()
				if row == None:
					password1 = self.password1.get()
					encoded=password1.encode()
					key1 = hashlib.sha256(encoded)
					cur.execute('insert into client(username,email,password) values(%s, %s, %s)', (self.name1.get(), self.mail.get(), str(key1.hexdigest())))
					con.commit()
					con.close()
					messagebox.showinfo("Success", "Inscription reussie", parent = self.root)
					self.loginform()			
				else :
					messagebox.showerror("Error", "Utilisateur déjà crée", parent = self.root)
			except Exception as es: 
				messagebox.showerror("Error", f"Erreur : {str(es)}", parent = self.root)
	
	def chatapp(self):
		t = threading.Thread(target=self.recv)
		while not t.is_alive():
			t.start()
		self.canvas = Canvas(
		    window,
		    bg = "#FFFFFF",
		    height = 600,
		    width = 1000,
		    bd = 0,
		    highlightthickness = 0,
		    relief = "ridge")
		self.canvas.place(x = 0, y = 0)

		self.appbackground_img = PhotoImage(file = f"img/appbackground.png")
		background = self.canvas.create_image(
		    500.0, 300.0,
		    image=self.appbackground_img)

		self.appentry0_img = PhotoImage(file = f"img/appimg_textBox0.png")
		entry0_bg = self.canvas.create_image(
		    624.5, 562.0,
		    image = self.appentry0_img)

		self.message = Entry(
		    bd = 0,
		    bg = "#fdf9f9",
		    highlightthickness = 0)

		self.message.place(
		    x = 465.0, y = 542,
		    width = 319.0,
		    height = 38)

		self.appimg0 = PhotoImage(file = f"img/appimg0.png")
		b0 = Button(
		    image = self.appimg0,
		    borderwidth = 0,
		    highlightthickness = 0,
		    # command = self.threadsendmsg,
		    relief = "flat")

		b0.place(
		    x = 857, y = 542,
		    width = 42,
		    height = 40)

		self.appimg1 = PhotoImage(file = f"img/appimg1.png")
		b1 = Button(
		    image = self.appimg1,
		    borderwidth = 0,
		    highlightthickness = 0,
		    command = self.appscreen,
		    relief = "flat")

		b1.place(
		    x = 385, y = 20,
		    width = 48,
		    height = 60)

		self.lstbx = Listbox(
	    		window,
	    		height = 20,
	    		width = 100)
		self.lstbx.place(x=379, y=126)
	def appscreen(self):

		self.root.geometry("500x600")
		self.canvas3 = Canvas(
			window,
			bg = "#FFFFFF",
			height = 600,
			width = 500,
			bd = 0,
			highlightthickness = 0,
			relief = "ridge")
		self.canvas3.place(x = 0, y = 0)
		self.profile_label = Label(
			self.root,
			bg="grey")
		self.profile_label.place(
			x=124, y=150, 
			width=251, 
			height=246)
		self.background_img = PhotoImage(file = f"img/pbackground.png")
		background = self.canvas3.create_image(
			250.0, 300.0,
			image=self.background_img)

		self.img0 = PhotoImage(file = f"img/pimg0.png")
		b0 = Button(
			image = self.img0,
			borderwidth = 0,
			cursor = "hand2",
			highlightthickness = 0,
			command = self.add_photo,
			relief = "flat")
		b0.place(
			x = 109, y = 425,
			width = 289,
			height = 54)

		self.img1 = PhotoImage(file = f"img/pimg1.png")
		b1 = Button(
			image = self.img1,
			borderwidth = 0,
			cursor = "hand2",
			highlightthickness = 0,
			command = self.process_data,
			relief = "flat")

		b1.place(
			x = 318, y = 546,
			width = 177,
			height = 36)

	def add_photo(self):
		self.image_path = filedialog.askopenfilename()
		image_name = os.path.basename(self.image_path)
		self.image_extension = image_name[image_name.rfind('.')+1:]

		if self.image_path:
			user_image = Image.open(self.image_path)
			user_image = user_image.resize((251, 246), Image.ANTIALIAS)
			user_image.save('resized'+image_name)
			user_image.close()

			self.image_path = 'resized'+image_name
			user_image = Image.open(self.image_path)

			user_image = ImageTk.PhotoImage(user_image)
			self.profile_label.image = user_image
			self.profile_label.config(image=user_image)

	def receive_data(self):
		while True:
			try:
				data_type = self.client_socket.recv(1024).decode()

				if data_type == 'notification':
					data_size = self.client_socket.recv(2048)
					data_size_int = struct.unpack('i', data_size)[0]

					b = b''
					while True:
						data_bytes = self.client_socket.recv(1024)
						b += data_bytes
						if len(b) == data_size_int:
							break
					data = pickle.loads(b)
					self.notification_format(data)

				else:
					data_bytes = self.client_socket.recv(1024)
					data = pickle.loads(data_bytes)
					self.received_message_format(data)

			except ConnectionAbortedError:
				print("you disconnected ...")
				self.client_socket.close()
				break
			except ConnectionResetError:
				messagebox.showinfo(title='No Connection !', message="Server offline..try connecting again later")
				self.client_socket.close()
				self.first_screen()
				break

	
	def process_data(self):
		if self.name.get():
			self.profile_label.config(image="")

			if len((self.name.get()).strip()) > 6:
				self.user = self.name.get()[:6]+"."
			else:
				self.user = self.name.get()

			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				client_socket.connect(("localhost", 12345))
				status = client_socket.recv(1024).decode()
				if status == 'not_allowed':
					client_socket.close()
					messagebox.showinfo(title="Can't connect !", message='Sorry, server is completely occupied.'
																			'Try again later')
					return

			except ConnectionRefusedError:
				messagebox.showinfo(title="Connexion impossible!", message="Serveeur hors ligne.")
				print("Serveur hors ligne. Veuillez reessayer")
				return

			client_socket.send(self.user.encode('utf-8'))
			try :
				if not self.image_path:
					self.image_path = self.user_image
				with open(self.image_path, 'rb') as image_data:
					image_bytes = image_data.read()

				image_len = len(image_bytes)
				image_len_bytes = struct.pack('i', image_len)
				client_socket.send(image_len_bytes)

				if client_socket.recv(1024).decode() == 'received':
					client_socket.send(str(self.image_extension).strip().encode())

				client_socket.send(image_bytes)

				clients_data_size_bytes = client_socket.recv(1024)
				clients_data_size_int = struct.unpack('i', clients_data_size_bytes)[0]
				b = b''
				while True:
					clients_data_bytes = client_socket.recv(1024)
					b += clients_data_bytes
					if len(b) == clients_data_size_int:
						break

				clients_connected = pickle.loads(b)

				client_socket.send('image_received'.encode())

				user_id = struct.unpack('i', client_socket.recv(1024))[0]
				print("connecté")
				messagebox.showinfo("Message","Connexion réussie")
				
			except Exception as es : 
				messagebox.showerror("Erreur",f"{str(es)}")
	
window=Tk()
ob=Login(window)
window.mainloop()
