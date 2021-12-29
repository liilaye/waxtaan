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
import sys

# sys.setrecursionlimit(1000000000)
print(sys.getrecursionlimit())
class Login(tk.Tk):
	def __init__(self,window):
		self.root = window
		self.root.title("WaxxTan")
		self.root.geometry("1000x600")
		self.root.configure(bg = "#ffffff")
		self.root.resizable(False,False)
		# self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.loginform()
		# self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
	
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
		    command = self.process_data,
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
	
	def ivalidateotp(self) : 	
		code = self.code.get()
		if code == self.otp :
			try:
				con=pymysql.connect(host='localhost',user='root',password='passer',database='waxxtan')
				cur=con.cursor()
				password1 = self.password1.get()
				encoded=password1.encode()
				key1 = hashlib.sha256(encoded)
				cur.execute('insert into client(username,email,password,photo) values(%s, %s, %s, %s)', (self.name1.get(), self.mail.get(), str(key1.hexdigest()), self.photo.get()))
				con.commit()
				con.close()
				messagebox.showinfo("Success", "Inscription reussie", parent = self.root)
				self.loginform()			
			except Exception as es: 
				messagebox.showerror("Error", f"Erreur : {str(es)}", parent = self.root)			
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
				password  = self.mdp.get()
				encoded=password.encode()
				key2 = hashlib.sha256(encoded)
				cur.execute('update client set password = %s WHERE email = %s',(str(key2.hexdigest()), self.email.get()))
				messagebox.showinfo("Info","Mot de passe modifié avec succes", parent = self.root)
				con.commit()
				con.close()
				print(str(key2.hexdigest()))
				print(self.email.get())
				self.loginform()
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

		self.entry4_img3 = PhotoImage(file = f"img/insimg_textBox0.png")
		entry4_bg = self.canvas.create_image(
			412.5, 490.0,
			image = self.entry4_img3)

		self.photo = Entry(
			bd = 0,
			bg = "#fffbfb",
			highlightthickness = 0)

		self.photo.place(
			x = 225, y = 475,
			width = 411,
			height = 30)		

		self.img01 = PhotoImage(file = f"img/img01.png")
		b0 = Button(
		    image = self.img01,
		    borderwidth = 0,
		    highlightthickness = 0,
		    command = self.register,
		    cursor = "hand2",
		    relief = "flat")

		b0.place(
		    x = 137, y = 520,
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
		
		self.img2 = PhotoImage(file = f"img/insimg.png")
		b2 = Button(
			image = self.img2,
			borderwidth = 0,
			highlightthickness = 0,
			command = self.add_photo,
			relief = "flat")

		b2.place(
			x = 45, y = 475,
			width = 180,
			height = 30)
	
	def otppage(self):
		window.geometry("500x600")
		self.canvas4 = Canvas(
			window,
			bg = "#FFFFFF",
			height = 600,
			width = 500,
			bd = 0,
			highlightthickness = 0,
			relief = "ridge")
		self.canvas4.place(x = 0, y = 0)

		self.background_img4 = PhotoImage(file = f"img/codebackground.png")
		background = self.canvas4.create_image(
			250.0, 300.0,
			image = self.background_img4)

		self.entry0_img4 = PhotoImage(file = f"img/imgimg_textBox1.png")
		entry0_bg = self.canvas4.create_image(
			263.0, 285.5,
			image = self.entry0_img4)

		self.code = Entry(
			bd = 0,
			bg = "#fffcfc",
			highlightthickness = 0)

		self.code.place(
			x = 121.5, y = 261,
			width = 283.0,
			height = 47)

		self.img0 = PhotoImage(file = f"img/imgimg1.png")
		b0 = Button(
			image = self.img0,
			borderwidth = 0,
			highlightthickness = 0,
			cursor = "hand2",
			command = self.ivalidateotp,
			relief = "flat")

		b0.place(
			x = 146, y = 361,
			width = 233,
			height = 49)

		self.img1 = PhotoImage(file = f"img/imgimg2.png")
		b1 = Button(
			image = self.img1,
			borderwidth = 0,
			highlightthickness = 0,
			cursor = "hand2",
			command = self.Register,
			relief = "flat")

		b1.place(
			x = 26, y = 15,
			width = 49,
			height = 39)

	def register(self):
		regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
		if self.name1.get() =="" or self.password1.get() == "" or self.mail.get() =="" or self.confirmpass.get() =="":
			messagebox.showerror("Error", "Veuillez remplir tous les champs", parent = self.root)
		elif self.photo.get() =="" : 
			messagebox.showerror("Error", "Veuillez ajouter une photo", parent = self.root)
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
					self.otp = "".join([str(random.randint(0,9)) for i in range(4)])
					server = smtplib.SMTP('smtp.gmail.com',587)
					server.starttls()
					server.login('waxxtan@gmail.com','isadbnathspqtxya')
					message = MIMEText("Votre code est :"+self.otp)
					message['Subject'] = "Code de validation d'inscription"
					message['From'] = "waxxtan@gmail.com"
					message['To'] = self.mail.get()
					msg = 'Votre code est : '+self.otp
					print(self.mail.get()+''+msg)
					receiver = str(self.mail.get())
					server.sendmail('waxxtan@gmail.com',f'{self.mail.get()}',message.as_string())
					server.quit()
					messagebox.showinfo("Info",f"Code envoyé.Veuillez vérifier votre boite mail")
					self.otppage()			
				else :
					messagebox.showerror("Error", "Utilisateur déjà crée", parent = self.root)
			except Exception as es: 
				messagebox.showerror("Error", f"Erreur : {str(es)}", parent = self.root)
	
	def add_photo(self):
		self.image_path = filedialog.askopenfilename()
		image_name = os.path.basename(self.image_path)
		self.image_extension = image_name[image_name.rfind('.')+1:]
		

		if self.image_path:
			user_image = Image.open(self.image_path)
			user_image = user_image.resize((251, 246), Image.ANTIALIAS)
			user_image.save('resized'+image_name)
			user_image.close()
			self.photo.insert(END,self.image_path)
			self.image_path = 'resized'+image_name
			user_image = Image.open(self.image_path)

			user_image = ImageTk.PhotoImage(user_image)
			self.profile_label.image = user_image
			self.profile_label.config(image=user_image)

	def process_data(self):
		if self.name.get() =="" or self.password.get() == "":
    			messagebox.showerror("Error", "Veuillez remplir tous les champs", parent = self.root)
		else:
			# try:
			con=pymysql.connect(host='localhost',user='root',password='passer',database='waxxtan')
			cur=con.cursor()
			password = self.password.get()
			encoded=password.encode()
			key = hashlib.sha256(encoded)
			cur.execute('select * from client where email=%s and password=%s',(self.name.get(),str(key.hexdigest())))
			cur1=con.cursor()
			cur1.execute('select photo from client where email=%s and password=%s',(self.name.get(),str(key.hexdigest())))
			row2 = cur1.fetchone()
			self.image_path1 = row2[0]
			image_name = os.path.basename(self.image_path1)
			self.image_extension1 = image_name[image_name.rfind('.')+1:]
			row=cur.fetchone()
			con.close()
			if row == None:
				messagebox.showerror("Error", "Verifiez les informations saisies", parent = self.root)
			else:
				# if len((self.name.get()).strip()) > 6:
				# 	self.user = self.name.get()[:6]+"."
				# else:
				self.user = self.name.get()

				client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				try:
					client_socket.connect(("localhost", 12345))
					status = client_socket.recv(1024).decode()
					if status == 'non_autorisé':
						client_socket.close()
						messagebox.showinfo(title="Connexion Impossible", message='Désolé le serveur est temporairement indisponible'
																				'Veuillez réessayer plus tard')
						return

				except ConnectionRefusedError:
					messagebox.showinfo(title="Connexion impossible!", message="Serveur hors ligne.")
					print("Serveur hors ligne. Veuillez reessayer")
					return

				client_socket.send(self.user.encode('utf-8'))

				with open(self.image_path1, 'rb') as image_data:
					image_bytes = image_data.read()

				image_len = len(image_bytes)
				image_len_bytes = struct.pack('i', image_len)
				client_socket.send(image_len_bytes)
				
				if client_socket.recv(1024).decode() == 'received':
						client_socket.send(str(self.image_extension1).strip().encode())

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
				print(f"{self.user} is user no. {user_id}")
				self.chatscreen(client_socket,clients_connected,user_id)		
			# except Exception as es:
			# 	messagebox.showerror("Error", f"Erreur due de à : {str(es)}", parent = self.root)
			# 	print(f"{str(es)}")
	
	def chatscreen(self, client_socket, clients_connected, user_id):
		self.root.geometry("1000x600")
		self.root.configure(bg = "#FFFFFF")
		self.canvas4 = Canvas(
			self.root,
			bg = "#FFFFFF",
			height = 600,
			width = 1000,
			bd = 0,
			highlightthickness = 0,
			relief = "ridge")
		self.canvas4.place(x = 0, y = 0)

		self.background_img4 = PhotoImage(file = f"img/chatbackground.png")
		background = self.canvas4.create_image(
			500.0, 300.0,
			image=self.background_img4)

		self.img4 = PhotoImage(file = f"img/chatimg0.png")
		b0 = Button(
			image = self.img4,
			borderwidth = 0,
			highlightthickness = 0,
			#command = self.bonjour,
			relief = "flat")

		b0.place(
			x = 307, y = 29,
			width = 43,
			height = 43)

		self.img41 = PhotoImage(file = f"img/chatimg1.png")
		b1 = Button(
			image = self.img41,
			borderwidth = 0,
			highlightthickness = 0,
			# command = btn_clicked,
			relief = "flat")

		b1.place(
			x = 921, y = 530,
			width = 50,
			height = 43)

		self.entry0_img4 = PhotoImage(file = f"img/chatimg_textBox0.png")
		entry0_bg = self.canvas4.create_image(
			664.0, 551.5,
			image = self.entry0_img4)

		self.message = Entry(
			bd = 0,
			bg = "#e8d6ff",
			highlightthickness = 0)

		self.message.place(
			x = 457.0, y = 530,
			width = 414.0,
			height = 41)
		self.client_socket = client_socket
		self.clients_connected = clients_connected
		self.user_id = user_id
		window.protocol("WM_DELETE_WINDOW", self.on_closing)

		con=pymysql.connect(host='localhost',user='root',password='passer',database='waxxtan')
		cur=con.cursor()
		mail = self.name.get()
		cur.execute("select * from client where email = %s",(mail))
		row = cur.fetchone()
		print(f"{row}")
		self.nom = row[1]
		self.mailcon = row[2]
		self.photoprofil = row[4]
		
		self.rectangle = self.canvas4.create_rectangle(107,32,277,69.5, outline="white", fill=self.canvas4["bg"])
		self.rectangle2 = self.canvas4.create_rectangle(475,32,952,69.5, outline="white", fill=self.canvas4["bg"])
		self.affichenom = self.canvas4.create_text(185, 55, text=f"WaxxTan", font="Roboto 25 bold", fill="black")
		self.photoprofil = os.path.basename(self.photoprofil)
		self.photoprofil = "resized"+self.photoprofil
		self.photoprofil = Image.open(f"{self.photoprofil}")
		self.photoprofil = self.photoprofil.resize((77,77),Image.ANTIALIAS)
		self.photoprofil = ImageTk.PhotoImage(self.photoprofil)
		entry011_bg = self.canvas4.create_image(
			45, 43,
			image = self.photoprofil) 
		
		cur2=con.cursor()
		cur2.execute("select * from client")
		row2 = cur2.fetchall()
		print(f"{row2}")
		for user  in row2 :
			a=0
			i=136
			j=143
			l=179
			b=88
			while a < len(row2):
				if self.mailcon != row2[a][2]:
					self.mailrcv = row2[a][2]
					self.pho = row2[a][4]
					self.pho = os.path.basename(self.pho)
					self.pho = "resized"+self.pho
					self.pho = Image.open(f"{self.pho}")
					self.pho = self.pho.resize((77,77),Image.ANTIALIAS)
					self.pho = ImageTk.PhotoImage(self.pho)
					entry011_bg = self.canvas4.create_image(
						45, i,
						image = self.pho)
					self.nomcontact = row2[a][1]
					# self.affichenomcontact = self.canvas4.create_text(185, j, text=f"{nom}", font="Montserrat 17 bold", fill="black")
					self.canvas4.create_line(0,l,360,l,fill="silver")
					self.affichenomcontact = Button(
						text = f"{self.nomcontact}",
						font = "Montserrat 17 bold",
						bg = "white",
						borderwidth = 0,
						cursor = "hand2",
						highlightthickness = 0,
						command = self.receiver,
						relief = "flat")

					self.affichenomcontact.place(
						x = 90, y = b,
						width = 269,
						height = 91)
					i=i+91
					j=j+91
					l=l+88
					b=b+91
				a=a+1
			print(f"{a}")

	def receiver(self):
		self.rx = self.affichenomcontact
		self.rx = self.rx.cget("text")
		self.rxphoto = self.pho
		entry012_bg = self.canvas4.create_image(
			416, 43,
			image = self.rxphoto)
		self.afficherx = self.canvas4.create_text(600,51.5,text=f"{self.rx}", font="Montserrat 22 bold", fill="black")
		self.mailrx = self.mailrcv


	def on_closing(self):
		# alert = "finduchat"
		# self.client_socket.send(alert.encode("utf-8"))
		if True : 
			self.client_socket.close()
			print("BYE")
			self.root.destroy()
    			
window=Tk()
ob=Login(window)
window.mainloop()


