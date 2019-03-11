

from tkinter import *

import os


finestra=Tk()
finestra.title("Cerca fitxers Redundants")
finestra.minsize(600,500)

f1=Frame(finestra)
f2=Frame(finestra)

#BOTO SORTIR
b=Button(finestra,text='Sortir',command=finestra.quit)
b.pack(side=BOTTOM,anchor=W)



directorifontE = Entry(f1,justify=CENTER)

directorifontE.delete(0,END)
contentFont = os.getcwd()
directorifontE.insert(0,contentFont)
directorifontE.configure(state='readonly')

directoriDestiE = Entry(f2,justify=CENTER)
directoriDestiE.delete(0,END)
directoriDestiE.insert(0,"Escull Directori")
directoriDestiE.configure(state='readonly')
#=========================================================================
#Escull directori i posa a readonly
def wd(entry):
	x=tkFileDialog.askdirectory()
	if len(x)>1:
		entry.configure(state='normal')
		entry.delete(0,END)   
		entry.insert(0,x)
		entry.configure(state='readonly')

#=========================================================================
#La funcioCerca crida a l'script cercaCopies.sh i interpreta els fitxers que crea aquest
def funcioCerca(igual,semblant,original):
	#Eliminem els elements de la listbox
	igual.delete(0,END)
	original.delete(0,END)
	semblant.delete(0,END)
	val=os.system("./cercaCopies.sh "+directorifontE.get()+" "+ directoriDestiE.get())
	# si no s'ha escollit un directori desti saltara el missatge d'error
	if val==256: 
		tkMessageBox.showinfo("ERROR","Falta escollir un directori destí.")
	else:
		#Agafem info dels fitxers creats per l'script i ho posem a les listbox
		igf=open("iguals","r")
		iguals=igf.read().splitlines()
		igual.insert(END,*iguals)
		igf.close()

		sem=open("semblants","r")
		semblants=sem.read().splitlines()
		semblant.insert(END,*semblants)
		sem.close()

		ori=open("originals","r")
		originals=ori.read().splitlines()
		path2=""
		for path in originals:
			if path != path2:
				original.insert(END,path)		
			path2=path
		ori.close()
	#borrem fitxers intermedis
	os.system("rm -f "+os.getcwd()+"/semblants")
	os.system("rm -f "+os.getcwd()+"/iguals")
	os.system("rm -f "+os.getcwd()+"/originals")
	os.system("rm -f "+os.getcwd()+"/f1")

#=========================================================================
#FUNCIO AUXILIAR-->obte el path del fitxer "original" de la listbox 
def getOriginal(listbox,original):
	listbox.select_set(0,END)
	elements=listbox.curselection()
	if elements:
		for ele in elements:
			content=listbox.get(ele)
			if original in content:
				return content
	else:
		tkMessageBox.showinfo("ERROR","No hi ha l'element original a la llista \n (If this is shown something is really broken)")

#==============================================================================
#esborra els fitxers seleccionats	
def esborra(listbox):
	elements=listbox.curselection()	
	if elements:
		for ele in elements:
			choice = tkMessageBox.askquestion("Esborrar","Vols borrar "+listbox.get(ele)+"?",icon='warning')
			if choice == "yes":
				os.system("rm -f "+listbox.get(ele))
				
			
	else:
		tkMessageBox.showinfo("ERROR","Heu de escullir algun element.")

#==============================================================================
#crea un hard link entre el fitxer seleccionat i l'original
def hL(listbox,listoriginal):
	elements=listbox.curselection()
	if elements:
		for ele in elements:
			content,x = listbox.get(ele).rsplit('/',1)
			pathOri=getOriginal(listoriginal,x)
			os.system("rm -f "+listbox.get(ele))		
			os.system("ln "+pathOri+" "+listbox.get(ele))
	
	else:
		tkMessageBox.showinfo("ERROR","Heu de escullir algun element.")
	listoriginal.selection_clear(0,END)

#=============================================================================
#crea un soft link entre el fitxer seleccionat i l'original
def sL(listbox,listoriginal):
	elements=listbox.curselection()
	if elements:
		for ele in elements:
			content,x = listbox.get(ele).rsplit('/',1)
			pathOri=getOriginal(listoriginal,x)
			os.system("rm -f "+listbox.get(ele))
			os.system("ln -s "+pathOri+" "+listbox.get(ele))
	
	else:
		tkMessageBox.showinfo("ERROR","Heu de escullir algun element.")
	listoriginal.selection_clear(0,END)

#============================================================================
#seleciona tots els elements
def sT(listbox):
	listbox.select_set(0,END)
	
#============================================================================
#ens deseleciona tots els elements
def sC(listbox):
	listbox.selection_clear(0,END)
	
#===========================================================================
#compara els element seleccionat a l'original i permet editarlo
def compara(listbox,listoriginal):
	elements=listbox.curselection()
	if elements:
		for ele in elements:
			content,x = listbox.get(ele).rsplit('/',1)
			pathOri=getOriginal(listoriginal,x)
			os.system("./compara.sh "+pathOri+" "+listbox.get(ele))
			pathOri=os.path.relpath(pathOri)
			pathS=os.path.relpath(listbox.get(ele))
			info=open("compara","r")
			inode=info.read().splitlines()
			#printem tot en un message box
			tkMessageBox.showinfo("COMPARA","Num linies diferents: "+inode[2]+"\nFitxer Original:\n\tPATH :"+pathOri+"\n\tINODE: "+inode[0]+"\nFitxer Semblant:\n\tPATH :"+pathS+"\n\tINODE: "+inode[1])
			#preguntem si es vol editar amb gvim
			choice = tkMessageBox.askquestion("Editar","Vols editar els fitxers amb gvim?")
			if choice == "yes":
				os.system("gvimdiff "+pathOri+" "+pathS)
	else:
		tkMessageBox.showinfo("ERROR","Heu de escullir algun element.")
	listoriginal.selection_clear(0,END)

#===============================================================================
#Renombra els fitxers escollits
def renombra(listbox):
	elements=listbox.curselection()	
	if elements:
		for ele in elements:
			choice = tkMessageBox.askquestion("Esborrar","Vols renombrar "+listbox.get(ele)+"?",icon='warning')
			if choice == "yes":
				x=tkSimpleDialog.askstring("Escull nom", finestra)
				if x != None:
					content,y = listbox.get(ele).rsplit('/',1)
					content+="/"+x				
					os.system("mv "+listbox.get(ele)+" "+content)
			
	else:
		tkMessageBox.showinfo("ERROR","Heu de escullir algun element.")


directorifontB = Button( f1,text=" Escolliu directori font ",command= lambda: wd(directorifontE))
directoriDestiB = Button (f2, text = "Escolliu directori destí",command= lambda: wd(directoriDestiE))
#pack font
directorifontB.pack(side= LEFT)
directorifontE.pack(fill=X)
#pack desti
directoriDestiB.pack(side=LEFT)


#=================================================================================
#FRAMES llistes i buttons
f4=Frame(finestra)
f43=Frame(f4)

f431=Frame(f43)
l2=Label(f431,text="Fitxers Originals:")
l2.pack(side=LEFT)
f431.pack(side=TOP,fill=X)

f432=Frame(f43)
scrollist = Scrollbar(f432,orient=VERTICAL)
list1 = Listbox(f432,yscrollcommand=scrollist.set,width= 40)
scrollist.config(command=list1.yview)
list1.pack(side=LEFT,expand=TRUE,fill=BOTH)
scrollist.pack(side=LEFT,fill=Y)
f432.pack(side=BOTTOM,fill=BOTH,expand=TRUE)

f41=Frame(f4)
f42=Frame(f4)


f413=Frame(f41)
l1=Label(f413,text="Fitxers Iguals:")
l1.pack(side=LEFT)
f413.pack(side=TOP,fill=X)



f412=Frame(f41)
scrollist2 = Scrollbar(f412,orient=VERTICAL)
list2 = Listbox(f412,yscrollcommand=scrollist.set,width=40)
scrollist2.config(command=list2.yview)
scrollist2.pack(side=LEFT,fill=Y)
list2.pack(side=TOP,expand=TRUE,fill=BOTH)
f412.pack(side=LEFT,expand=TRUE,fill=BOTH)

f423=Frame(f42)
l1=Label(f423,text="Fitxers Semblants:")
l1.pack(side=LEFT)
f423.pack(side=TOP,fill=X)

f421=Frame(f42)
scrollist3 = Scrollbar(f421,orient=VERTICAL)
list3 = Listbox(f421,yscrollcommand=scrollist.set,width=40)
scrollist3.config(command=list3.yview)
scrollist3.pack(side=LEFT,fill=Y)
list3.pack(side=BOTTOM,expand=TRUE,fill=BOTH)
f421.pack(side=LEFT,expand=TRUE,fill=BOTH)

cercaB = Button( f2, text="Cerca",command=lambda: funcioCerca(list2,list3,list1)) 
cercaB.pack(side=RIGHT)
directoriDestiE.pack(fill=X)

f422=Frame(f42)
comp=Button(f422,text="Compara",command=lambda: compara(list3,list1))
comp.pack()
rename=Button(f422,text="Renombra",command=lambda: renombra(list3))
rename.pack()
borrar=Button(f422,text="Esborra",command=lambda: esborra(list3))
borrar.pack()
selectT0=Button(f422,text="Select Tots",command=lambda: sT(list3))
selectT0.pack()
selectC0=Button(f422,text="Select Cap", command=lambda: sC(list3))
selectC0.pack()
f422.pack(side=RIGHT)

f411=Frame(f41)
esborrar=Button(f411,text="Esborra",command=lambda: esborra(list2))
esborrar.pack()
hLB=Button(f411,text="Hard Link",command=lambda: hL(list2,list1))
hLB.pack()
sLB=Button(f411,text="Soft Link",command=lambda : sL(list2,list1))
sLB.pack()
selectT=Button(f411,text="Select Tots",command=lambda: sT(list2))
selectT.pack()
selectC=Button(f411,text="Select Cap",command=lambda: sC(list2))
selectC.pack()
f411.pack(side=RIGHT)

#Ultim frame ultims bottons
f5=Frame(finestra)
tots=Button(f5,text="Selecciona Tots",command=lambda: sT(list1))
tots.pack(side=LEFT)
cap=Button(f5,text="Selecciona Cap",command=lambda: sC(list1))
cap.pack(side=LEFT)

#PACK FRAMES
f43.pack(side=LEFT,expand=TRUE,fill=BOTH)
f41.pack(expand=TRUE,side=TOP,fill=BOTH)
f42.pack(expand=TRUE,side=BOTTOM, fill=BOTH)
f1.pack(fill=X,side=TOP,anchor=W)
f2.pack(fill=X)
f4.pack(expand=TRUE,fill=BOTH)
f5.pack(side=LEFT)

finestra.mainloop()

