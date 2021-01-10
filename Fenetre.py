from tkinter import *
import os,sys, subprocess
from tkdocviewer import *
import tkinter.ttk as ttk
from date import DateEntry
from Section import Information
import tkinter.messagebox
from Latex import latex
from note import note
from tkinter import scrolledtext
from tkinter import filedialog

class Format:
    def __init__(self):
        self.repfic=""
        self.root=Tk()
        self.root.title("Générateur de formulaires")
        self.root.configure(background='ivory3')
        self.frame = Frame(self.root,width=715,height=800)
        self.frame.grid(row=0,column=0)
        self.frame.grid_propagate(0)
        self.frame1=Frame(self.root)
        self.frame.configure(background='ivory3')
        self.root.geometry('1600x800')
        #self.root.geometry('600x600')
        self.d=latex()
        self.note=note()
        self.liste_grille=[]
        #nombre ligne tableau long
        self.tab_long=0
        #taille radiobutton
        self.taille_Radio="2.5mm"
        #ce qu'on va trouver des qu'on ouvre la fenetre 
        self.initial(self.frame)
        #initialisation info
        self.numinf=0
        #liste contenant les infos
        self.informations=Information()
        #les num des question
        self.numq=0
        #les nums des reponses pour chaque question
        self.numr=0
        #compteur pour la format des questions et reponses
        self.j = 0
        self.i = 0
        #initialisation des bouttons
        self.bannuler=Button()
        self.button_ok_libre=Button()
        self.button_ok=Button()
        self.saisie_reponse=Button()
        self.nombre_rep_par_ligne=Spinbox()
        self.nombre_ligne=Spinbox()
        self.donner_nbr_ligne=Label()
        self.donner_nbr_rep_par_ligne=Label()
        self.entrer_rep= Label()
        self.entrer_reponse = Entry()
        self.entry_note=Entry()
        self.label_note=Label()
        self.myLabel_saisirq=Label()
        self.question=scrolledtext.ScrolledText()
        # liste des positions
        self.position=[]
        #initialisation section
        self.controle_sect=False
        self.numsect=0
        self.section=Information()#section=[(num sect, sect)]
        self.sections={} #sections={numsect:{numq:[quest],[type],[nombre],[liste rep],[note]}}
        #initialisation des reponses
        self.reponse=Information()         
        #le menu
        self.menu(self.root)
        #note
        self.notere=[]
        #fermer la fenetre
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.mainloop()  
    #Menubar
    def menu(self,master):
        menubar=Menu(master,activebackground='ivory4',background='ivory4')

        filemenu= Menu(menubar,tearoff=0,activebackground='ivory4',background='ivory4')
        filemenu.add_command(label="Nouveau",command= lambda: self.new(master),underline=0)
        filemenu.add_separator()
        filemenu.add_command(label="Enregistrer",command=lambda:self.callback_formulaire("None"),underline=0)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=lambda:self.quitter(master),underline=0)
        menubar.add_cascade(label="File",menu=filemenu)
        
        editmenu= Menu(menubar,tearoff=0,activebackground='ivory4',background='ivory4')
        self.modifier=Menu(editmenu,tearoff=0,activebackground='ivory4',background='ivory4')
        self.modifier.add_command(label="Modifier taille du Radiobutton",command= self.modifier_taille_RadioButton,state="disabled")
        self.modifier.add_separator()
        self.modifier_section_menu=Menu(self.modifier,tearoff=0,activebackground='ivory4',background='ivory4')

        editmenu.add_cascade(label="Modifier ...",menu=self.modifier)
        editmenu.add_separator()
        self.modifier.add_cascade(label="Modifier une section ...",menu=self.modifier_section_menu,state='disabled')
        self.modifier.add_separator()
        self.modifier_section_menu.add_command(label="Modifier le numéro de la section",command=lambda:
                                        self.modifier_section("section","numero","",""),state='disabled')
        self.modifier_section_menu.add_separator()
        self.modifier_section_menu.add_command(label="Modifier le titulaire de la section",command=lambda:
                                        self.modifier_section("section","contenu","",""))
        self.modifier_section_menu.add_separator()
        self.modifier_quests=Menu(self.modifier_section_menu,tearoff=0,activebackground='ivory4',background='ivory4')
        self.modifier_section_menu.add_cascade(label="Modifier une question de la section ..",menu=self.modifier_quests,state='disabled')
        self.modifier_section_menu.add_separator()
        self.modifier_section_menu.add_command(label="Supprimer une question de la section",command=lambda:
                                        self.modifier_section("section","question","supprimer",""),state='disabled')
        self.modifier_section_menu.add_separator()
        self.modifier_section_menu.add_command(label="Ajouter une question à la section",command=lambda:
                                        self.modifier_section("section","ajouter","",""),state='disabled')

        self.modifier_quests.add_command(label="Modifier le numéro de la question",state='disabled',command=lambda:
                                        self.modifier_section("section","question","numero",""))
        self.modifier_quests.add_separator()
        self.modifier_quests.add_command(label="Modifier le titulaire de la question",command=lambda:
                                        self.modifier_section("section","question","contenu",""))
        self.modifier_quests.add_separator()
        self.modifier_quests.add_command(label="Modifier le type de la question",command=lambda:
                                        self.modifier_section("section","question","type",""))
        self.modifier_quests.add_separator()
        self.modifier_quests.add_command(label="Modifier la note de la question si elle est une paragraphe/réponse courte ",state='disabled',
                                        command=lambda:self.modifier_section("section","question","libre",""))
        self.modifier_quests.add_separator()
        self.modifier_reponses=Menu(self.modifier_quests,tearoff=0,activebackground='ivory4',background='ivory4')
        self.modifier_quests.add_cascade(label="Modifier une réponse de la question ..",menu=self.modifier_reponses,state='disabled')
        self.modifier_quests.add_separator()
        self.modifier_quests.add_command(label="Supprimer une réponse de la question",command=lambda:
                                        self.modifier_section("section","question","reponse","supprimer"),state='disabled')
        self.modifier_quests.add_separator()
        self.modifier_quests.add_command(label="Ajouter une réponse à la question",command=lambda:
                                        self.modifier_section("section","question","ajouter",""),state='disabled')
        self.modifier_quests.add_separator()
        self.modifier_quests.add_command(label="Modifier nombre de lignes dans une grille",state='disabled',command=lambda:
                                            self.tableau_long("section"))

        self.modifier_reponses.add_command(label="Modifier le numéro de la réponse",command=lambda:
                                        self.modifier_section("section","question","reponse","numero"),state='disabled')
        self.modifier_reponses.add_separator()
        self.modifier_reponses.add_command(label="Modifier le titulaire de la réponse",command=lambda:
                                        self.modifier_section("section","question","reponse","contenu"))
        self.modifier_reponses.add_separator()
        self.modifier_reponses.add_command(label="Modifier la note de la réponse",command=lambda:
                                        self.modifier_section("section","question","reponse","note"),state='disabled')

        self.modifier_questq=Menu(self.modifier,tearoff=0,activebackground='ivory4',background='ivory4')
        self.modifier.add_cascade(label="Modifier une question ..",men=self.modifier_questq,state='disabled')
        self.modifier.add_separator()
        
        self.modifier_questq.add_command(label="Modifier le numéro de la question",command=lambda:
                                        self.modifier_section("question","question","numero",""),state='disabled')
        self.modifier_questq.add_separator()
        self.modifier_questq.add_command(label="Modifier le titulaire de la question",command=lambda:
                                        self.modifier_section("question","question","contenu",""))
        self.modifier_questq.add_separator()
        self.modifier_questq.add_command(label="Modifier le type de la question",command=lambda:
                                        self.modifier_section("question","question","type",""))
        self.modifier_questq.add_separator()
        self.modifier_questq.add_command(label="Modifier la note de la question si elle est une paragraphe/réponse courte ",command=lambda:
                                        self.modifier_section("question","question","libre",""),state='disabled')
        self.modifier_questq.add_separator()
        self.modifier_reponseq=Menu(self.modifier_questq,tearoff=0,activebackground='ivory4',background='ivory4')
        self.modifier_questq.add_cascade(label="Modifier une réponse de la question ..",menu=self.modifier_reponseq,state='disabled')
        self.modifier_questq.add_separator()
        self.modifier_questq.add_command(label="Supprimer une réponse de la question",command=lambda:
                                        self.modifier_section("question","question","reponse","supprimer"),state='disabled')
        self.modifier_questq.add_separator()
        self.modifier_questq.add_command(label="Ajouter une réponse à la question",command=lambda:
                                        self.modifier_section("question","question","ajouter",""),state='disabled')
        self.modifier_questq.add_separator()
        self.modifier_questq.add_command(label="Modifier nombre de lignes dans une grille",state='disabled',command=lambda:
                                            self.tableau_long("question"))
        
        self.modifier_reponseq.add_command(label="Modifier le numéro de la réponse",command=lambda:
                                        self.modifier_section("question","question","reponse","numero"),state='disabled')
        self.modifier_reponses.entryconfigure
        self.modifier_reponseq.add_separator()
        self.modifier_reponseq.add_command(label="Modifier le titulaire de la réponse",command=lambda:
                                        self.modifier_section("question","question","reponse","contenu"))
        self.modifier_reponseq.add_separator()
        self.modifier_reponseq.add_command(label="Modifier la note de la réponse",command=lambda:
                                        self.modifier_section("question","question","reponse","note"),state='disabled')
        self.modifier.add_command(label="Modifier une information",state='disabled',command=lambda:
                                        self.modifier_information("Modifier"))
        

        self.supprimer=Menu(editmenu,tearoff=0,activebackground='ivory4',background='ivory4')
        editmenu.add_cascade(label="Supprimer ...",menu=self.supprimer)
        supprimer_section=Menu(self.supprimer,tearoff=0,activebackground='ivory4',background='ivory4')
        self.supprimer.add_command(label="Supprimer une section",state='disabled',command=lambda:
                                        self.supprimer_section("Supprimer"))
        self.supprimer.add_separator()
        supprimer_question=Menu(supprimer_section,tearoff=0,activebackground='ivory4',background='ivory4')
        self.supprimer.add_command(label="Supprimer une question",state='disabled',command=lambda:
                                        self.supprimer_question("Supprimer"))
        self.supprimer.add_separator()
        self.supprimer.add_command(label="Supprimer une infotmation",state='disabled',command=lambda:
                                        self.modifier_information("Supprimer"))
        
        
        supprimer_section.add_command(label="Supprimer toute la section")
        

        supprimer_question.add_command(label="Supprimer toute la question")
        supprimer_question.add_separator()

        menubar.add_cascade(label="Edit",menu=editmenu)

        helpmenu=Menu(menubar,tearoff=0,activebackground='ivory4',background='ivory4')
        helpmenu.add_command(label="Manuel",command=self.manuel)
        menubar.add_cascade(label="Aide?",menu=helpmenu)
        master.config(menu=menubar)        
    #fonction quitter
    def quitter(self,master):
        nom1="form.pdf"
        nom2="form.tex"
        nom3='fiche_des_notes_du_form.xls'
        if(os.path.exists(nom1)):
            os.remove(nom1)
        elif(os.path.exists(nom2)):
            os.remove(nom2)
        elif(os.path.exists(nom3)):
            os.remove(nom3)
        master.destroy()
            
    def manuel(self):
        if sys.platform == "win32":
            os.startfile("Manuel.pdf")
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, "Manuel.pdf"])
        
    #fonction quitter a partir de l'icone
    def callback(self):
        print(self.numq)
        if(self.numsect==0 and os.path.exists("form.pdf")==True):
            if(tkinter.messagebox.askokcancel("Quit", "Voulez vous quitter?")):
                self.quitter(self.root)
        elif(os.path.exists("form.pdf")==False):
            if(tkinter.messagebox.askokcancel("Quit", "Voulez vous quitter?")):
                self.root.destroy()
        else:
            if tkinter.messagebox.askokcancel("Quit", "Voulez vous enregistrer?") :
                self.enregister("None")
                self.root.destroy()
            else:
                self.quitter(self.root)                      
    #fonction pour modifier la taille des radio button
    def modifier_taille_RadioButton(self):
        frame=Tk()
        frame.title("Modifier taille du Radiobutton")
        frame.configure(background='ivory3')
        l=Label(frame,text="Modifier taille du Radiobutton(en mm):",font=("Helvetica", 13),background='ivory3')
        l.grid(row=0,column=0)
        taille=ttk.Combobox(frame, values=["1.5","2", "2.5","3","3.5"],width=3)
        taille.current(2)
        taille.grid(row=0,column=1,sticky='w')
        b=Button(frame,background='ivory3',font=("Helvetica", 12),text="OK",command=lambda:self.ok_taille(frame,str(taille.get())))
        b.grid(row=1,columnspan=2)
    def ok_taille(self,frame,o):
        self.taille_Radio=o+"mm"
        frame.destroy()
        self.mise_a_jours()
    #reinitialize la fenetre principale
    def new(self,master):
        self.callback()
        Format()   
    #fonction relative au champ information
    def informaton(self,a,entryinfo):
        print("INFOR")
        print(self.informations.retourner())
        if(a!=""):
            self.numinf+=1
            self.informations.ajouter(self.numinf,a)
            entryinfo.delete(0,END)
            self.supprimer.entryconfigure("Supprimer une infotmation",state=tkinter.NORMAL)
            self.modifier.entryconfigure("Modifier une information",state=tkinter.NORMAL)
        self.mise_a_jours()
    #interface au debut            
    def initial(self,master):
        #date
        l=Label(master,font=("Helvetica", 13),background='ivory3',text="Date:")
        l.grid(row=0,column=0,sticky='w')
        self.date = DateEntry(master, font=('Helvetica', 10, NORMAL), border=0)
        self.date.grid(row=0,column=1,sticky='w')
        #module
        l=Label(master,font=("Helvetica", 13),background='ivory3',text="Titre:")
        l.grid(row=1,column=0,sticky='w')
        self.titre1=Entry(master,width=30,borderwidth= 5)
        self.titre1.grid(row=1,column=1,sticky='w',columnspan=2)
        #etablissement 
        l=Label(master,font=("Helvetica", 13),background='ivory3',text="Établissement:")
        l.grid(row=2,column=0,sticky='w')
        self.etab=Entry(master,width=30,borderwidth=5)
        self.etab.grid(row=2,column=1,sticky='w',columnspan=2)
        #note
        c=Label(master,font=("Helvetica", 13),background='ivory3',text="Ajouter notes:")
        c.grid(row=4,rowspan=2,column=0,sticky='w')
        self.donner_note=StringVar()
        a=Checkbutton(master,text='Oui',variable=self.donner_note,font=("Helvetica", 12),background='ivory3',activebackground='ivory3',highlightbackground='ivory3')
        a.grid(row=4,column=1,sticky='w')
        #informations
        info=Label(master,font=("Helvetica", 13),background='ivory3',text="Information:")
        info.grid(row=3,column=0,sticky='w')
        entryinfo=Entry(master,width=30,borderwidth=5)
        entryinfo.grid(row=3,column=1,sticky='w',columnspan=2)
        self.informationbt=Button(master,background='ivory3',font=("Helvetica", 12),text="OK",command=lambda: self.informaton(entryinfo.get(),entryinfo))
        self.informationbt.grid(row=3,column=3,sticky='w')
        #ajouter section
        sectionbt=Button(master,background='ivory3',font=("Helvetica", 12),text="Ajouter section",command=lambda:self.section1(master,sectionbt,self.liste))
        sectionbt.grid(row=6,column=0)
        #ajouter questin
        label_ajout=Label(master,font=("Helvetica", 13),background='ivory3',text="Ajouter question\n de type:")
        label_ajout.grid(row=7,column=0,sticky='w',rowspan=2)
        #type de de question
        option=[("Question de cases à cocher","Question à choix uniques"),
            ("Question à choix multiples","Question à choix multiples"), 
            ("Paragraphe/réponse courte","Question à choix libre"),
            ("Grille de cases à cocher","Grille à choix uniques"),
            ("Grille à choix multiples","Grille à choix multiples")]
        type_q=StringVar()
        j=7
        i=0
        for tx,mode in option:
            option[i]=Radiobutton(master,font=("Helvetica", 11),background='ivory3',activebackground='ivory3',highlightbackground='ivory3',text=tx,value=mode,variable=type_q)
            option[i].grid(row=j,column=1,sticky='w')
            i+=1
            j+=1
        #horizentale ou verticale
        position=StringVar()
        #self.position=[("Verticale","v"),("Échelle linéaire","h")]
        i=7
        j=0
        self.positionc=Checkbutton(master,text="Échelle\n linéaire",variable=position,font=("Helvetica", 12),background='ivory3',activebackground='ivory3',highlightbackground='ivory3')
        self.positionc.grid(row=7,column=2,sticky='w',rowspan=2)
        #for tx,mode in self.position:
        #    self.position[j]=Radiobutton(master,font=("Helvetica", 11),background='ivory3',activebackground='ivory3',highlightbackground='ivory3',text=tx,value=mode,variable=position)
        #    self.position[j].grid(row=i,column=2,sticky='w')
        #    i+=1
        #    j+=1
        #self.vert=self.position[0]
        #self.horiz=self.position[1]
        self.option_question=[option[0],option[1],option[2],option[3],option[4]]
        self.ques =Button(master,background='ivory3',font=("Helvetica", 12),text="Ajouter \nQuestion",command= lambda: self.choisir_nature_question(str(position.get()),str(type_q.get()),str(self.donner_note.get()),a,self.positionc,sectionbt))
        self.ques.grid(row=7,column=3,sticky='w',rowspan=2)  
        self.liste=[label_ajout,self.positionc,self.ques]
    #ajouter section
    def section1(self,master,bt,liste):
        for i in liste:
            i.config(state=DISABLED)
        for i in self.option_question:
            i.config(state=DISABLED)
        section=Entry(master,width=40,borderwidth=5)
        section.grid(row=6,column=1,sticky='w',columnspan=2)
        b=Button(master,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.oksection(master,bt,section.get(),b,section,liste))
        b.grid(row=6,column=3)
        bt.config(state=DISABLED)
        self.initialiser_under_section()
    def oksection(self,master,bt,sect,b,section,liste):
        if(sect==""):
            tkinter.messagebox.showerror("Error", "Veuillez saisir le titulaire de la section!")
            #self.bannuler=Button(master,background='ivory3',font=("Helvetica", 12),text="Annuler ajout",command=lambda:
            self.annuler_sect(self.bannuler,b,bt,section,liste)
            #self.bannuler.grid(row=6,column=3)
        else:
            bt.config(state=DISABLED)
            self.bannuler.destroy()
            for i in liste:
                i.config(state=NORMAL)
            for i in self.option_question:
                i.config(state=NORMAL)
            section.destroy()
            self.controle_sect=True
            b.destroy()
            self.numsect+=1
            self.section.ajouter(self.numsect,sect)
            self.modifier.entryconfigure("Modifier une section ...",state=tkinter.NORMAL)
            self.supprimer.entryconfigure("Supprimer une section",state=tkinter.NORMAL)
            self.sections[self.numsect]=[]
            self.mise_a_jours()
            self.numq=0
            if(len(self.numero_section())>=2):
                self.modifier_section_menu.entryconfigure("Modifier le numéro de la section",state=tkinter.NORMAL)
            if(len(self.sections[self.numsect])>0):
                b1=Button(master,background='ivory3',font=("Helvetica", 12),text="Fin Section",command=lambda:self.fin_sect(b1,bt,liste))
                b1.grid(row=6,column=3,sticky='w')
            #itha ken mazelnesh ajouter section besh nehsbou kol quest section wahadha
            #itha ken aamalna ok section besh naamrou dict te3 section
    def annuler_sect(self,b1,b,bt,entry,liste):
        b1.destroy()
        b.destroy()
        entry.destroy()
        bt.config(state=NORMAL)
        for i in liste:
            i.config(state=NORMAL)
        for i in self.option_question:
            i.config(state=NORMAL)
    def fin_sect(self,b1,bt,liste):
        bt.config(state=NORMAL)
        for i in self.option_question:
            i.config(state=NORMAL)
        for i in liste:
            i.config(state=NORMAL)
        b1.destroy()
        self.controle_sect=False  
        self.initialiser_under_section()   
        self.modifier_section_menu.entryconfigure("Ajouter une question à la section",state=tkinter.NORMAL)   
        self.modifier_quests.entryconfigure("Ajouter une réponse à la question",state=tkinter.NORMAL)
    #choisir le type de question
    def choisir_nature_question(self,position,type_q,note,oui,v,sect): 
        if(self.liste_grille!=[]):
            for i in self.liste_grille:
                i.destroy()
        self.entry_note.destroy()
        self.label_note.destroy()
        #self.informationbt.config(state=DISABLED)   
        if(note==""):
            note="n"
        else:
            note="o"
        #disable le changement de avec ou sans mote
        sect.config(state=DISABLED)
        
        oui.config(state=DISABLED)
        #si la question n'est pas libre on doit choisir la position soit horizentale soit verticale
        if(type_q==""):
            type_q="Question à choix uniques"
        if (type_q!="Question à choix libre" and position==""):
            position="v"
        if(position=="1"):
            position="h"
        self.ques.config(state=DISABLED)
        #disable le changement des etats
        v.config(state=DISABLED)
        for i in self.option_question:
            i.config(state=DISABLED)
        self.donner_nbr_rep_par_ligne.destroy()
        self.nombre_rep_par_ligne.destroy()
        self.saisie_reponse.destroy()
        self.entrer_rep.destroy()
        self.entrer_reponse.destroy()
        self.nombre_ligne.destroy()
        self.donner_nbr_ligne.destroy()
        print("HUUUU")
        print(type_q) 
        print(position)         
        if (type_q=="Question à choix uniques"):     
            self.modifier.entryconfigure("Modifier taille du Radiobutton",state=tkinter.NORMAL)       
            format="unique"
        elif (type_q=="Question à choix multiples"):          
            format="multiple"    
            self.ques.config(state=DISABLED) 
        elif(type_q=="Question à choix libre"):    
            format="libre"  
        elif("Grille" in type_q):
            format=type_q
        self.add_quest(format,position,type_q,note,v,sect)
        k=self.numero_question()  
        if(len(k)>=1):
            if(self.numq>=1):
                if( self.sections[self.numsect][self.numq-1][2][0]!="libre" ):
                    self.modifier_questq.entryconfigure("Ajouter une réponse à la question",state=tkinter.NORMAL) 
        d=self.numero_section()
        if(d!={}):
            print("HETHA D")
            print(d)
            if(len(self.sections[self.numsect])>=1):
                print(self.sections[self.numsect])
                if(self.numq>=1):
                    print("HI nadher faker")
                    print(self.numq)
                    print(self.numsect)
                    print(self.sections[self.numsect][self.numq-1])
                    if(self.sections[self.numsect][self.numq-1][2][0]!="libre"):
                        self.modifier_quests.entryconfigure("Ajouter une réponse à la question",state=tkinter.NORMAL)
    #ajouter question
    def add_quest(self,format,position,type_q,note,v,sect): 
        print("ICI")
        print(position)
        #initializer le num des rep pour chaque question    
        self.numr=0
        #initializer la liste des reponses pour chaque question
        self.reponse=Information()
        #label saisie de question
        self.myLabel_saisirq= Label(self.frame,font=("Helvetica", 13),background='ivory3', text="Saisir question:")
        self.myLabel_saisirq.grid(row=12, column=0,sticky='w')
        #entrer quest
        self.question=scrolledtext.ScrolledText(self.frame, width=50, height=2,borderwidth=5) 
        self.question.grid(row=12, column=1,padx=10,pady=10,columnspan=3,sticky='w')
        #self.button_ok.config(state=NORMAL)
        if("Grille" in type_q):
            l=[]
            c=[]
            self.button_ok=Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda: self.grilles(str(self.question.get('1.0', 'end-1c')),sect,v,note,self.button_ok,l,c,type_q))
            self.button_ok.grid(row=12,column=4,sticky='w')
        else:
            #Question à choix libre
            if (type_q=="Question à choix libre"):  
                #fonctionalite note
                if(note=="o" or note=="1"):
                    #avec la note
                    self.label_note=Label(self.frame,font=("Helvetica", 13),background='ivory3',text="Donner la note:")
                    self.label_note.grid(row=15,column=0,sticky='w')
                    self.entry_note=Entry(self.frame,width=10,borderwidth=5)
                    self.entry_note.grid(row=15,column=1)      
                    self.button_ok_libre=Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.choisir_fct_libre(str(self.question.get('1.0', 'end-1c')),self.button_ok_libre,note,str(self.entry_note.get()),v,sect))
                    self.button_ok_libre.grid(row=12,column=4,sticky='w')
                else:
                    #sans note
                    self.button_ok_libre=Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.choisir_fct_libre(str(self.question.get('1.0', 'end-1c')),self.button_ok_libre,note,0,v,sect))
                    self.button_ok_libre.grid(row=12,column=4,sticky='w')
                #nombre de ligne a laisser pour la reponse 
                self.donner_nbr_ligne=Label(self.frame,font=("Helvetica", 13),background='ivory3',text="Donner le nombre de lignes:")
                self.donner_nbr_ligne.grid(row=14,column=0,columnspan=2,sticky='w')
                self.nombre_ligne=Spinbox(self.frame,from_=1, to=10, width=2)
                self.nombre_ligne.grid(row=14,column=2)
            else:
                #verticale
                if(position=="v"or position=="0"):
                    self.donner_nbr_rep_par_ligne.destroy()
                    self.nombre_rep_par_ligne.destroy()    
                    self.nombre_ligne.destroy()  
                    self.button_ok=Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda: self.choisir_fct_quest(str(self.question.get('1.0', 'end-1c')),self.button_ok,position,type_q,0,note,v,sect,format))
                    self.button_ok.grid(row=12,column=4,sticky='w')
                    #horizentale
                elif(position=="h" or position=="1" ):            
                    #realiser levenement 
                    self.donner_nbr_rep_par_ligne=Label(self.frame,font=("Helvetica", 13),background='ivory3',text="Donner le nombre de réponses /ligne:")
                    self.donner_nbr_rep_par_ligne.grid(row=13,column=0,columnspan=2,sticky='w')
                    self.nombre_rep_par_ligne=IntVar()
                    self.nombre_rep_par_ligne=Spinbox(self.frame,from_=2, to=10, width=2)
                    self.nombre_rep_par_ligne.grid(row=13,column=2)
                    self.button_ok=Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda: self.choisir_fct_quest(str(self.question.get('1.0', 'end-1c')),self.button_ok,position,type_q,int(self.nombre_rep_par_ligne.get()),note,v,sect,format))
                    self.button_ok.grid(row=12,column=4,sticky='w')    
    #question libre
    def choisir_fct_libre(self,quest,button_ok_libre,note,champ_note,v,sect):
        if(quest=="" ):
            #il faut entrer une quest
            tkinter.messagebox.showerror("Error", "Veuillez saisir une question")
        else:
            if(self.sections!={}):
                if(len(self.sections[self.numsect])==0):
                    b1=Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Fin Section",command=lambda:self.fin_sect(b1,sect,self.liste))
                    b1.grid(row=6,column=3,sticky='w')
            #enable la position
            self.ques.config(state=NORMAL)  
            v.config(state=NORMAL)
            for i in self.option_question:
                i.config(state=NORMAL)
            if(note=="o" or note=="1"):
                if(champ_note=="" ):
                    tkinter.messagebox.showerror("Error", "Veuillez entrer la note de cette question!")
                else:
                    if(champ_note.isdigit()!=True):
                        tkinter.messagebox.showerror("Error", "Veuillez entrer un chiffre!")
                    else:       
                        self.modifier_quests.entryconfigure("Modifier la note de la question si elle est une paragraphe/réponse courte ",state=tkinter.NORMAL)    
                        #disable le button ok pour ne pas le confondre avec boutton ajouter question
                        button_ok_libre.destroy()
                        #increpenter le num des questions
                        if(self.controle_sect==True): 
                            self.modifier_quests.entryconfigure("Modifier la note de la question si elle est une paragraphe/réponse courte ",state=tkinter.NORMAL)
                            self.numq+=1
                            self.sections[self.numsect].append([[self.numq],[quest],["libre"],[int( self.nombre_ligne.get())],[],[champ_note]])
                            self.modifier_section_menu.entryconfigure("Modifier une question de la section ..",state=tkinter.NORMAL) 
                            self.modifier_section_menu.entryconfigure("Supprimer une question de la section",state=tkinter.NORMAL) 
                            d=self.numero_section()
                            if(len(d)!=0):
                                for i in d.values():
                                    if(i[1]>=2):
                                        self.modifier_quests.entryconfigure("Modifier le numéro de la question",state=tkinter.NORMAL)
                        else:
                            sect.config(state=NORMAL)
                            self.numq=1
                            self.numsect+=1
                            self.section.ajouter(self.numsect,"rien")
                            self.sections[self.numsect]=[[[self.numq],[quest],["libre"],[int( self.nombre_ligne.get())],[],[champ_note]]]
                            self.modifier.entryconfigure("Modifier une question ..",state=tkinter.NORMAL) 
                            self.supprimer.entryconfigure("Supprimer une question",state=tkinter.NORMAL)
                            self.modifier_questq.entryconfigure("Modifier la note de la question si elle est une paragraphe/réponse courte ",state=tkinter.NORMAL)  
                            if(self.numsect>1):
                                self.modifier_questq.entryconfigure("Modifier le numéro de la question",state=tkinter.NORMAL)        
                            self.mise_a_jours()
            else:         
                #disable le button ok pour ne pas le confondre avec boutton ajouter question
                button_ok_libre.destroy()
                champ_note=0             
                #increpenter le num des questions
                if(self.controle_sect==True):
                    self.numq+=1
                    self.sections[self.numsect].append([[self.numq],[quest],["libre"],[int( self.nombre_ligne.get())],[],[champ_note]])
                    self.modifier_section_menu.entryconfigure("Modifier une question de la section ..",state=tkinter.NORMAL) 
                    self.modifier_section_menu.entryconfigure("Supprimer une question de la section",state=tkinter.NORMAL) 
                    d=self.numero_section()
                    if(len(d)!=0):
                        for i in d.values():
                            if(i[1]>=2):
                                self.modifier_quests.entryconfigure("Modifier le numéro de la question",state=tkinter.NORMAL)
                else:
                    sect.config(state=NORMAL)
                    self.numq=1
                    self.numsect+=1
                    self.section.ajouter(self.numsect,"rien")
                    self.sections[self.numsect]=[[[self.numq],[quest],["libre"],[int( self.nombre_ligne.get())],[],[champ_note]]]
                    self.modifier.entryconfigure("Modifier une question ..",state=tkinter.NORMAL) 
                    self.supprimer.entryconfigure("Supprimer une question",state=tkinter.NORMAL)
                    self.modifier_questq.entryconfigure("Modifier la note de la question si elle est une paragraphe/réponse courte ",state=tkinter.NORMAL)  
                    if(self.numsect>1):
                        self.modifier_questq.entryconfigure("Modifier le numéro de la question",state=tkinter.NORMAL)        
                    self.mise_a_jours()     
    #question multiple ou unique
    def choisir_fct_quest(self,quest,button_ok,position,type_q,nombre_rep_par_ligne,note,v,sect,format):
        if(quest==""):
            #il faut entrer une quest
            tkinter.messagebox.showerror("Error", "Please entrer question")
        else:
            if(self.sections!={}):
                if(len(self.sections[self.numsect])==0):
                    b1=Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Fin Section",command=lambda:self.fin_sect(b1,sect,self.liste))
                    b1.grid(row=6,column=3,sticky='w')
            shape=""
            if(position=="h"):
                #remplir la liste des rep par ligne 
                nombre_rep=int(nombre_rep_par_ligne)
                self.add_format(quest,button_ok,position,type_q,nombre_rep_par_ligne,note,v,sect)
                shape="horizentale "+format
            else:
                #dans le cas verticale le rep par ligne=1
                nombre_rep=1
                self.add_format(quest,button_ok,position,type_q,nombre_rep_par_ligne,note,v,sect) 
                shape="verticale "+format
            #ajouter au dictionneur conteneur des questions cette question avec intialisation de la liste des reponses   
            #increpenter le num des questions
            if(self.controle_sect==True):
                self.numq+=1
                self.notere=[]
                self.sections[self.numsect].append([[self.numq],[quest],[shape],[nombre_rep],[],[]])
                self.modifier_section_menu.entryconfigure("Modifier une question de la section ..",state=tkinter.NORMAL) 
                self.modifier_section_menu.entryconfigure("Supprimer une question de la section",state=tkinter.NORMAL) 
                d=self.numero_section()
                if(len(d)!=0):
                    for i in d.values():
                        if(i[1]>=2):
                            self.modifier_quests.entryconfigure("Modifier le numéro de la question",state=tkinter.NORMAL) 
            else:
                self.numq=1
                self.notere=[]
                self.numsect+=1
                self.section.ajouter(self.numsect,"rien") 
                sect.config(state=NORMAL) 
                self.sections[self.numsect]=[[[self.numq],[quest],[shape],[nombre_rep],[],[]]]
                self.modifier.entryconfigure("Modifier une question ..",state=tkinter.NORMAL) 
                self.supprimer.entryconfigure("Supprimer une question",state=tkinter.NORMAL)
                if(len(self.numero_question())>1):
                    self.modifier_questq.entryconfigure("Modifier le numéro de la question",state=tkinter.NORMAL)
            self.mise_a_jours()      
    def add_format(self,quest,button_ok,position,type_q,nombre_rep_par_ligne,note,v,sect):
        if(note=="o" or note=="1"):
            self.label_note=Label(self.frame,font=("Helvetica", 13),background='ivory3',text="Donner la note:")
            self.label_note.grid(row=15,column=0,sticky='w')
            self.entry_note=Entry(self.frame,width=10,borderwidth=5)
            self.entry_note.grid(row=15,column=1)
            self.saisie_reponse =Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Ajouter réponse",command=lambda: self.choisir_fct_rep(quest,self.entrer_reponse.get(),position,type_q,nombre_rep_par_ligne,note,self.entry_note.get(),v,sect))
            self.saisie_reponse.grid(row=14,column=4,sticky='w')
        else:
            self.saisie_reponse =Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Ajouter réponse",command=lambda: self.choisir_fct_rep(quest,self.entrer_reponse.get(),position,type_q,nombre_rep_par_ligne,note,0,v,sect))
            self.saisie_reponse.grid(row=14,column=4,sticky='w')
        #ajouter rep
        self.entrer_rep= Label(self.frame,font=("Helvetica", 13),background='ivory3', text="Saisir réponse")
        self.entrer_rep.grid(row=14, column=0,sticky='w')
        #entrer rep
        self.entrer_reponse = Entry(self.frame, width=50,borderwidth= 5)
        self.entrer_reponse.grid(row=14, columnspan=3,column=1,padx=10,pady=10,sticky='w')                        
        #self.verif_quest(quest)
        #disable la fonction l ajout des questions jusqu'a celui ci ait au moins une reponse
        self.ques.config(state=DISABLED)
        #disable le bouton ok des questions
        button_ok.config(state=DISABLED)      
    #reponses des questions                  
    def choisir_fct_rep(self,quest,repon,position,type_q,nombre_rep_par_ligne,note,valeur_note,v,sect):
        if(repon==""):
            #il faut entrer une quest
            tkinter.messagebox.showerror("Error", "Veuillez saisir la reponse!")
        else:
            #enable les radibutton verticale et horizentale
            for i in self.option_question:
                i.config(state=NORMAL)
            v.config(state=NORMAL)
            if(note=="o" or note=="1"):
                if(valeur_note==""):
                    tkinter.messagebox.showerror("Error", "Veuillez entrer la note de cette réponse!")
                else:
                    if(valeur_note.isdigit()!=True):
                        tkinter.messagebox.showerror("Error", "Veuillez entrer un chiffre!")
                    else:
                        if(self.controle_sect==True):
                            self.modifier_reponses.entryconfigure("Modifier la note de la réponse",state=tkinter.NORMAL)
                        else:
                            self.modifier_reponseq.entryconfigure("Modifier la note de la réponse",state=tkinter.NORMAL)
                        #incrementer le nombre de reponse pour chaque question 
                        self.numr+=1    
                        self.verif_rep(repon,valeur_note)
                        #des qu'on a joute au moins une seule reponse pour chaque question on peut qjouter d'autres questions
                        self.ques.config(state=NORMAL)
                        #oublier la valeur ancienne de la note
                        self.entry_note.delete(0,END)
                        #oublier la valeur ancienne de la reponse
                        self.entrer_reponse.delete(0,END)
            else:
                valeur_note=0
                #incrementer le nombre de reponse pour chaque question 
                self.numr+=1    
                self.verif_rep(repon,valeur_note)
                #des qu'on a joute au moins une seule reponse pour chaque question on peut qjouter d'autres questions
                self.ques.config(state=NORMAL)
                #oublier la valeur ancienne de la reponse
                self.entrer_reponse.delete(0,END)
    def verif_rep(self,repon,valeur_note):     
        # ajouter le rep a la liste des reponses
        self.reponse.ajouter(self.numr,repon)
        self.notere.append(valeur_note)  
        if(self.controle_sect==False):
            self.sections[self.numsect][self.numq-1][4]=self.reponse.retourner()
            self.sections[self.numsect][self.numq-1][5]=self.notere
            self.modifier_reponseq.entryconfigure("Modifier le titulaire de la réponse",state=tkinter.NORMAL)
            self.modifier_questq.entryconfigure("Modifier une réponse de la question ..",state=tkinter.NORMAL)
            self.modifier_questq.entryconfigure("Supprimer une réponse de la question",state=tkinter.NORMAL)
            if(self.reponse.len()>=2):
                self.modifier_reponseq.entryconfigure("Modifier le numéro de la réponse",state=tkinter.NORMAL)
        else:
            self.sections[self.numsect][self.numq-1][4]=self.reponse.retourner()
            self.sections[self.numsect][self.numq-1][5]=self.notere
            self.modifier_reponses.entryconfigure("Modifier le titulaire de la réponse",state=tkinter.NORMAL)
            if(self.reponse.len()>=2):
                self.modifier_reponses.entryconfigure("Modifier le numéro de la réponse",state=tkinter.NORMAL)
            self.modifier_quests.entryconfigure("Modifier une réponse de la question ..",state=tkinter.NORMAL)
            self.modifier_quests.entryconfigure("Supprimer une réponse de la question",state=tkinter.NORMAL)
        self.mise_a_jours()
    def numero_question(self):
        l={}
        c=1
        n=[]
        for i,j in self.sections.items() :
            b=self.section.recup(i)
            if(b=="rien"):
                n=self.sections[i][0]
                print(n)
                if("Grille" in n[2][0]):
                    print("oui")
                    if(len(n[4][0])!=0 or len(n[4][1])!=0):
                        l[c]=[i,max(len(n[4][0]),len(n[4][1]))]
                    else:
                        l[c]=[i,0]
                else:
                    if(n[4]!=[]):
                        l[c]=[i,len(n[4])]
                    else:
                        l[c]=[i,0]
                c+=1
        return l
    
    def numero_section(self):
        #dict={cle=numsec:valeur=[numsect dans sections,len des questions]}
        l={}
        c=1
        for i,j in self.sections.items() :
            b=self.section.recup(i)
            if(b!="rien"):
                if(j!=[]):
                    l[c]=[i,len(j)]                   
                else:
                    l[c]=[i,0]
                c+=1
        return l
    
    def grilles(self,quest,sect,v,note,ok,l,c,type_q):
        if(quest=="" ):
            #il faut entrer une quest
            tkinter.messagebox.showerror("Error", "Veuillez saisir une question")
        else:
            self.modifier_quests.entryconfig("Modifier nombre de lignes dans une grille",state=tkinter.NORMAL)
            self.modifier_questq.entryconfig("Modifier nombre de lignes dans une grille",state=tkinter.NORMAL)
            if("uniques" in type_q):
                self.modifier.entryconfig("Modifier taille du Radiobutton",state=tkinter.NORMAL)
            if(self.sections!={}):
                if(len(self.sections[self.numsect])==0):
                    b1=Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Fin Section",command=lambda:self.fin_sect(b1,sect,self.liste))
                    b1.grid(row=6,column=3,sticky='w')
            #enable la position
            v.config(state=NORMAL)
            for i in self.option_question:
                i.config(state=NORMAL)
            ok.config(state=DISABLED)
            if(self.controle_sect==True):
                self.numq+=1
                self.sections[self.numsect].append([[self.numq],[quest],[type_q],[],[[],[]],[]])
                self.modifier_section_menu.entryconfigure("Modifier une question de la section ..",state=tkinter.NORMAL) 
                self.modifier_section_menu.entryconfigure("Supprimer une question de la section",state=tkinter.NORMAL) 
                d=self.numero_section()
                if(len(d)!=0):
                    for i in d.values():
                        if(i[1]>=2):
                            self.modifier_quests.entryconfigure("Modifier le numéro de la question",state=tkinter.NORMAL) 
            else:
                self.numq=1
                self.numsect+=1
                self.section.ajouter(self.numsect,"rien") 
                sect.config(state=NORMAL) 
                self.sections[self.numsect]=[[[self.numq],[quest],[type_q],[],[[],[]],[]]]
                self.modifier.entryconfigure("Modifier une question ..",state=tkinter.NORMAL) 
                self.supprimer.entryconfigure("Supprimer une question",state=tkinter.NORMAL)
                if(len(self.numero_question())>1):
                    self.modifier_questq.entryconfigure("Modifier le numéro de la question",state=tkinter.NORMAL)
            self.l1=Label(self.frame,font=("Helvetica", 13),background='ivory3',text="Ajouter ligne:")
            self.l1.grid(row=13,column=0,sticky='w')
            self.entre_ligne=Entry(self.frame, width=50,borderwidth= 5)
            self.entre_ligne.grid(row=13,columnspan=3, column=1,padx=10,pady=10,sticky='w')
            self.l2=Label(self.frame,font=("Helvetica", 13),background='ivory3',text="Ajouter colonne:")
            self.l2.grid(row=15,column=0,sticky='w')
            self.entre_colonne=Entry(self.frame, width=50,borderwidth= 5)
            self.entre_colonne.grid(row=15,columnspan=3, column=1,padx=10,pady=10,sticky='w')
            self.ok_col=Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Ajouter colonne",command=lambda:self.ajouter_colonne(str(self.entre_colonne.get()),self.entre_colonne))
            self.ok_col.grid(row=15,column=4,sticky='w')
            if(note=="o" or note=="1"):
                self.note1=Label(self.frame,font=("Helvetica", 13),background='ivory3',text="Donner la note:")
                self.note1.grid(row=14,column=0,sticky='w')
                self.entree_note=Entry(self.frame,width=10,borderwidth=5)
                self.entree_note.grid(row=14,column=1)
                self.ok_lign=Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Ajouter ligne",command= lambda:self.ajouter_ligne(note,str(self.entre_ligne.get()),self.entree_note.get(),self.entre_ligne,self.entree_note))
                self.ok_lign.grid(row=13,column=4,sticky='w')
                self.liste_grille=[self.entre_colonne,self.entre_ligne,self.entree_note,self.l1,self.l2,self.ok_lign,self.note1,self.ok_col]
            else:
                self.ok_lign=Button(self.frame,background='ivory3',font=("Helvetica", 12),text="Ajouter ligne",command= lambda: self.ajouter_ligne(note,str(self.entre_ligne.get()),str(0),self.entre_ligne,0))
                self.ok_lign.grid(row=13,column=4,sticky='w')
                self.liste_grille=[self.entre_colonne,self.entre_ligne,self.l1,self.l2,self.ok_lign,self.ok_col]  
            self.mise_a_jours()
            
    def ajouter_colonne(self,rep,a):
        if(rep==""):
            tkinter.messagebox.showerror("Error", "Veuillez saisir la reponse!")
        else:
            a.delete('0', END)
            self.sections[self.numsect][self.numq-1][4][0].append(rep)
            if(self.controle_sect==False):
                self.modifier_reponseq.entryconfigure("Modifier le titulaire de la réponse",state=tkinter.NORMAL)
                self.modifier_questq.entryconfigure("Modifier une réponse de la question ..",state=tkinter.NORMAL)
                self.modifier_questq.entryconfigure("Supprimer une réponse de la question",state=tkinter.NORMAL)
                if(len(self.sections[self.numsect][self.numq-1][4][0])>=2):
                    self.modifier_reponseq.entryconfigure("Modifier le numéro de la réponse",state=tkinter.NORMAL)
            else:
                self.modifier_reponses.entryconfigure("Modifier le titulaire de la réponse",state=tkinter.NORMAL)
                if(len(self.sections[self.numsect][self.numq-1][4][0])>=2):
                    self.modifier_reponses.entryconfigure("Modifier le numéro de la réponse",state=tkinter.NORMAL)
                self.modifier_quests.entryconfigure("Modifier une réponse de la question ..",state=tkinter.NORMAL)
                self.modifier_quests.entryconfigure("Supprimer une réponse de la question",state=tkinter.NORMAL)
            self.mise_a_jours()
            self.ques.config(state=NORMAL)
    def ajouter_ligne(self,oui,rep,note,a,b):
        if(rep==""):
            tkinter.messagebox.showerror("Error", "Veuillez saisir la reponse!")
        else:
            
            if(oui=="o" or oui=="1"):
                b.delete('0', END)
                self.modifier_reponseq.entryconfig("Modifier la note de la réponse",state=tkinter.NORMAL)
                self.modifier_reponses.entryconfig("Modifier la note de la réponse",state=tkinter.NORMAL)
                if(note==""):
                    tkinter.messagebox.showerror("Error", "Veuillez entrer la note de cette ligne!")
                else:
                    if(note.isdigit()!=True):
                        tkinter.messagebox.showerror("Error", "Veuillez entrer un chiffre!")
                    else:
                        a.delete('0', END)
                        self.sections[self.numsect][self.numq-1][5].append(int(note))
                        self.sections[self.numsect][self.numq-1][4][1].append(rep)         
                        if(self.controle_sect==False):
                            self.modifier_reponseq.entryconfigure("Modifier le titulaire de la réponse",state=tkinter.NORMAL)
                            self.modifier_questq.entryconfigure("Modifier une réponse de la question ..",state=tkinter.NORMAL)
                            self.modifier_questq.entryconfigure("Supprimer une réponse de la question",state=tkinter.NORMAL)
                            if(len(self.sections[self.numsect][self.numq-1][4][1])>=2):
                                self.modifier_reponseq.entryconfigure("Modifier le numéro de la réponse",state=tkinter.NORMAL)
                        else:
                            self.modifier_reponses.entryconfigure("Modifier le titulaire de la réponse",state=tkinter.NORMAL)
                            if(len(self.sections[self.numsect][self.numq-1][4][1])>=2):
                                self.modifier_reponses.entryconfigure("Modifier le numéro de la réponse",state=tkinter.NORMAL)
                            self.modifier_quests.entryconfigure("Modifier une réponse de la question ..",state=tkinter.NORMAL)
                            self.modifier_quests.entryconfigure("Supprimer une réponse de la question",state=tkinter.NORMAL)
                        self.mise_a_jours()
                        self.ques.config(state=NORMAL)
            else:
                self.sections[self.numsect][self.numq-1][5].append(int(note))
                self.sections[self.numsect][self.numq-1][4][1].append(rep)         
                if(self.controle_sect==False):
                    self.modifier_reponseq.entryconfigure("Modifier le titulaire de la réponse",state=tkinter.NORMAL)
                    self.modifier_questq.entryconfigure("Modifier une réponse de la question ..",state=tkinter.NORMAL)
                    self.modifier_questq.entryconfigure("Supprimer une réponse de la question",state=tkinter.NORMAL)
                    if(len(self.sections[self.numsect][self.numq-1][4][1])>=2):
                        self.modifier_reponseq.entryconfigure("Modifier le numéro de la réponse",state=tkinter.NORMAL)
                else:
                    self.modifier_reponses.entryconfigure("Modifier le titulaire de la réponse",state=tkinter.NORMAL)
                    if(len(self.sections[self.numsect][self.numq-1][4][1])>=2):
                        self.modifier_reponses.entryconfigure("Modifier le numéro de la réponse",state=tkinter.NORMAL)
                    self.modifier_quests.entryconfigure("Modifier une réponse de la question ..",state=tkinter.NORMAL)
                    self.modifier_quests.entryconfigure("Supprimer une réponse de la question",state=tkinter.NORMAL)
                self.mise_a_jours()
                self.ques.config(state=NORMAL)
   
    #modifier..
    #modifier secion 
    def modifier_section(self,st,qt,rt,tt):#appelle modifier question
        liste_commande=[st,qt,rt,tt]
        frame=Tk()
        frame.configure(background='ivory3')
        if(st!="section"):
            frame.title("Modifier question")
            #nombre max des questions
            b=1
            #nomre max des reponses
            n=0
            d=self.numero_question()
            if(len(d)==1):
                b=1
            else:
                b=len(d)
            for i,j in d.items():
                if(n<j[1]):
                    n=j[1]
            row=0
            liste_max=[0,b,n]
            self.modifier_question(frame,liste_commande,row,liste_max,"n")
            #bt=Button(frame,text="OK",command=lambda:self.modifier_question(frame,liste_commande,row,liste_max,bt))
            #bt.grid(row=0,column=2)
        else:
            frame.title("Modifier section")
            ls=Label(frame,text="Donner numéro section :",font=("Helvetica", 13),background='ivory3')
            ls.grid(row=0,column=0,sticky='w')
            d=self.numero_section()
            if(len(d)==1):
                #nombre max des questions dans les sections
                a=1
                #numero de la section avec max de question
                b=1
                ls1=Label(frame,text="1",font=("Helvetica", 13),background='ivory3')
                ls1.grid(row=0,column=1,sticky='w')
                a=1
                for i,j in d.items():
                    if(a<j[1]):
                        a=j[1]
                        b=j[0] 
                n=1
                for i in self.sections[b]:
                    if(i[4]!=[]):
                        if(len(i[4])>n):
                            n=len(i[4])
                row=1
                liste_max=[len(d),a,n]
                bt=Button(frame,background='ivory3',font=("Helvetica", 12),text="OK",command=lambda:self.modifier_question(frame,liste_commande,row,liste_max,bt))
                bt.grid(row=0,column=2)
            else:
                a=1
                b=1
                self.numeros=Spinbox(frame,from_=1, to=len(d), width=2)
                self.numeros.grid(row=0,column=1,sticky='w')
                for i,j in d.items():
                    if(a<j[1]):
                        a=j[1]
                        b=j[0] 
                n=1
                for i,j in self.sections.items():
                    for k in j:
                        if(k[4]!=[]):
                            if(len(k[4])>n):
                                n=len(k[4])
                row=1
                liste_max=[len(d),a,n]
                bt=Button(frame,text="OK",background='ivory3',font=("Helvetica", 12),command=lambda:self.modifier_question(frame,liste_commande,row,liste_max,bt))
                bt.grid(row=0,column=2)
                
    def modifier_question(self,frame,liste_commande,row,liste_max,b):# appelle mofi_section et modi_question 
        if(liste_commande[1]=="question"):
            if(liste_commande[0]=="section"):
                b.config(state=DISABLED)
            lq=Label(frame,text="Donner le numéro question :",font=("Helvetica", 13),background='ivory3')
            lq.grid(row=row,column=0,sticky='w')
            if(liste_max[1]==1):
                lq1=Label(frame,text="1",font=("Helvetica", 13),background='ivory3')
                lq1.grid(row=row,column=1,sticky='w')
            else:
                self.numeroq=Spinbox(frame,from_=1, to=liste_max[1], width=2)
                self.numeroq.grid(row=row,column=1,sticky='w')
            ok=Button(frame,text="ok",background='ivory3',font=("Helvetica", 12),command=lambda:self.modi_question(frame,liste_commande,ok,row+1,liste_max,b))
            ok.grid(row=row,column=2,sticky='w')
        elif(liste_commande[1]=="contenu"):
            lq1=Label(frame,text="Saisir le nouveau titulaire de la section :",font=("Helvetica", 13),background='ivory3')
            lq1.grid(row=row,column=0,sticky='w')
            saisie=Entry(frame,width=50,borderwidth=5)
            saisie.grid(row=row,column=1,sticky='w')
            row+=1
            b=Button(frame,text="Ok",background='ivory3',font=("Helvetica", 12),command=lambda:self.mofi_section(frame,liste_commande[1],b,saisie.get()))
            #command=lambda:self.modifier_contenu(frame,liste_commande,saisie.get(),[],0))
            b.grid(row=row, columnspan=2)
        elif(liste_commande[1]=="numero"):
            lq1=Label(frame,text="Donner le nouveau numéro de la section :",font=("Helvetica", 13),background='ivory3')
            lq1.grid(row=row,column=0,sticky='w')
            self.numeros1=Spinbox(frame,from_=1, to=liste_max[0], width=2)
            self.numeros1.grid(row=row,column=1,sticky='w')
            row+=1
            b=Button(frame,text="Ok",background='ivory3',font=("Helvetica", 12),command=lambda:self.mofi_section(frame,liste_commande[1],b,"vv"))
            #,command=lambda:self.modifier_contenu(frame,st,qt,rt,tt,self.numeros1.get(),[],0))
            b.grid(row=row, columnspan=2)
        elif(liste_commande[1]=="ajouter"):
            row+=1
            lq1=Label(frame,text="Donner le nouveau type de question:",font=("Helvetica", 13),background='ivory3')
            lq1.grid(row=row,column=0,sticky='w')
            type_q=StringVar()
            e=Radiobutton(frame,background='ivory3',highlightbackground='ivory3',font=("Helvetica", 12),text="Question de cases à cocher",value="u",variable=type_q,command=lambda:self.afficher_t("unique"))
            e.grid(row=row,column=1,sticky='w')
            f=Radiobutton(frame,background='ivory3',highlightbackground='ivory3',font=("Helvetica", 12),text="Question de choix multiples",value="m",variable=type_q,command=lambda:self.afficher_t("multiple"))
            f.grid(row=row+1,column=1,sticky='w')
            g=Radiobutton(frame,background='ivory3',highlightbackground='ivory3',font=("Helvetica", 12),text="Paragraphe/réonse courte",value="l",variable=type_q,command=lambda:self.afficher_t("libre"))
            g.grid(row=row+2,column=1,sticky='w')
            h=Radiobutton(frame,background='ivory3',highlightbackground='ivory3',font=("Helvetica", 12),text="Grille de cases à cocher",value="gu",variable=type_q,command=lambda:self.afficher_t("Grille unique"))
            h.grid(row=row+3,column=1,sticky='w')
            i=Radiobutton(frame,background='ivory3',highlightbackground='ivory3',font=("Helvetica", 12),text="Grille de choix multiples",value="gm",variable=type_q,command=lambda:self.afficher_t("Grille multiple"))
            i.grid(row=row+4,column=1,sticky='w')
            #position=[("Verticale","v"),("Horizental","h")]
            pos=StringVar()
            b=Checkbutton(frame,background='ivory3',font=("Helvetica", 12),text="Échelle linéaire",variable=pos,command=lambda:self.afficher_p("horizentale"))
            b.grid(row=row,column=2,sticky='w')
            liste=[b,e,f,g,h,i]
            self.liste_modif=""
            b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.mofi_section(frame,liste_commande[1],b,liste))
            #,command=lambda:self.modifier_contenu(frame,st,qt,rt,tt,b,liste,0))
            b.grid(row=row,column=3)
    
    #fonctions pour retourner le types choisis pour les questions
    def afficher_t(self,pos):
        self.liste_modif=pos
    def afficher_p(self,pos):
        print(self.liste_modif)
        print(pos)
        if(pos=="horizentale"):
            name="horizentale "+self.liste_modif
            self.liste_modif=name
            print(name)
        else:
            name="verticale "+self.liste_modif
            self.liste_modif=name  

    def mofi_section(self,frame,commande,b,nom):#appelle ok_ajouter_question
        num=1
        d=self.numero_section()
        if(len(d)!=1):
            num=int(self.numeros.get())
        numsec_reel=d[num][0]
        if(commande=="contenu"):
            self.section.modifier(numsec_reel,nom)
        elif(commande=="numero"):
            nums1=1
            for i,j in d.items():
                if(i==int(self.numeros1.get())):
                    nums1=j[0]
            l=self.sections[nums1]
            self.sections[nums1]=self.sections[numsec_reel]
            self.sections[numsec_reel]=l
            self.section.permuter(numsec_reel,nums1)
            self.numq=len(self.sections[self.numsect])    
        elif(commande=="ajouter"):
            type_q=self.liste_modif
            self.ok_ajouter_quest(frame,type_q,7,b,nom,numsec_reel)
        self.mise_a_jours()
    #commande ajoute question dans section
    def ok_ajouter_quest(self,frame,type_q,row,b,liste,sect):#appelle valider_question et valider_question_grille
        for i in liste:
            i.config(state=DISABLED)
        b.destroy()
        row+=1
        lq1=Label(frame, text="Saisir question:",font=("Helvetica", 13),background='ivory3')
        lq1.grid(row=row, column=0,sticky='w')
        #entrer quest
        question=scrolledtext.ScrolledText(frame, width=50, height=2,borderwidth=5) 
        question.grid(row=row, column=1,padx=10,pady=10,columnspan=2,sticky='w')
        row+=1
        if("Grille" in type_q):
            ok=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ajouter",command=lambda:self.valider_question_grille(frame,str(question.get('1.0','end-1c')),type_q,sect))
            ok.grid(row=row,column=3)
        elif(type_q=="libre"):
            l1=Label(frame,text="Donner le nombre de lignes:",font=("Helvetica", 13),background='ivory3')
            l1.grid(row=row,column=0,sticky='w')
            nombre=Spinbox(frame,from_=1, to=10, width=2)
            nombre.grid(row=row,column=1,sticky='w')
            row+=1
            ok=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ajouter",command=lambda:self.valider_question(frame,str(question.get('1.0','end-1c')),type_q,int(nombre.get()),sect))
            ok.grid(row=row,column=3)
        elif("horizentale" in type_q):
            l1=Label(frame,text="Donner le nombre de réponses /ligne:",font=("Helvetica", 13),background='ivory3')
            l1.grid(row=row,column=0,sticky='w')
            nombre=Spinbox(frame,from_=2, to=10, width=2)
            nombre.grid(row=row,column=1,sticky='w')
            row+=1
            ok=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ajouter",command=lambda:self.valider_question(frame,str(question.get('1.0','end-1c')),type_q,int(nombre.get()),sect))
            ok.grid(row=row,column=3)
        else:
            row+=1
            ok=Button(frame,text="Ajouter",command=lambda:self.valider_question(frame,str(question.get('1.0','end-1c')),type_q,1,sect))
            ok.grid(row=row,column=3)
    def valider_question(self,frame,nom,typ,nombre,num):
        if(nom==""):
            tkinter.messagebox.showerror("Error", "Veuillez saisir une question")
        else:
            n=len(self.sections[num])
            self.sections[num].append([[n+1],[nom],[typ],[nombre],[],[]])
            self.mise_a_jours()
            print(self.sections)
            frame.destroy()
    def valider_question_grille(self,frame,nom,typ,num):
        if(nom==""):
            tkinter.messagebox.showerror("Error", "Veuillez saisir une question")
        else:
            n=len(self.sections[num])
            self.sections[num].append([[n+1],[nom],[typ],[],[[],[]],[]])
            self.mise_a_jours()
            frame.destroy()
    
    def modi_question(self,frame,rt,ok,row,liste_max,b_ok):#appelle mofi_question et modifier_reponse
        ok.destroy()
        num=1
        if(rt[0]=="section"):
            d=self.numero_section()
            if(len(d)!=1):
                num=int(self.numeros.get())
        else:
            d=self.numero_question()       
            num=1
            if(len(d)>1):
                num=int(self.numeroq.get())
        numsec_reel=d[num][0]
        if(rt[2]=="numero"):
            row+=1
            lq1=Label(frame,text="Donner le nouveau numéro question :",font=("Helvetica", 13),background='ivory3')
            lq1.grid(row=row,column=0,sticky='w')
            self.numeroq1=Spinbox(frame,from_=1, to=liste_max[1], width=2)
            self.numeroq1.grid(row=row,column=1,sticky='w')
            row+=1
            b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.mofi_question(frame,rt,numsec_reel,"vv",b,0,liste_max,b_ok))
            #,command=lambda:self.modifier_contenu(frame,st,qt,rt,tt,self.numeroq1,[],0))
            b.grid(row=row, columnspan=2)
        elif(rt[2]=="contenu"):
            row+=1
            lq1=Label(frame,text="Saisir le nouveau titulaire de la question :",font=("Helvetica", 13),background='ivory3')
            lq1.grid(row=row,column=0,sticky='w')
            saisie=scrolledtext.ScrolledText(frame, width=60, height=2,borderwidth=5) 
            saisie.grid(row=row,column=1,padx=10,pady=10,sticky='w')
            row+=1
            b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.mofi_question(frame,rt,numsec_reel,saisie.get('1.0', 'end-1c'),b,0,liste_max,b_ok))
            #,command=lambda:self.modifier_contenu(frame,st,qt,rt,tt,str(saisie.get('1.0','end-1c')),[],0))
            b.grid(row=row, columnspan=2)
        elif(rt[2]=="type"):
            row+=1
            lq1=Label(frame,text="Donner le nouveau type de question:",font=("Helvetica", 13),background='ivory3')
            lq1.grid(row=row,column=0,sticky='w')
            type_q=StringVar()
            e=Radiobutton(frame,background='ivory3',font=("Helvetica", 12),text="Question de cases à cocher",value="u",variable=type_q,command=lambda:self.afficher_t("unique"))
            e.grid(row=row,column=1,sticky='w')
            f=Radiobutton(frame,background='ivory3',font=("Helvetica", 12),text="Question à choix multiples",value="m",variable=type_q,command=lambda:self.afficher_t("multiple"))
            f.grid(row=row+1,column=1,sticky='w')
            g=Radiobutton(frame,background='ivory3',font=("Helvetica", 12),text="Paragraphe/réponse courte",value="l",variable=type_q,command=lambda:self.afficher_t("libre"))
            g.grid(row=row+2,column=1,sticky='w')
            h=Radiobutton(frame,background='ivory3',font=("Helvetica", 12),text="Grille de cases à cocher",value="gu",variable=type_q,command=lambda:self.afficher_t("Grille unique"))
            h.grid(row=row+3,column=1,sticky='w')
            i=Radiobutton(frame,background='ivory3',font=("Helvetica", 12),text="Grille à choix multiples",value="gm",variable=type_q,command=lambda:self.afficher_t("Grille multiple"))
            i.grid(row=row+4,column=1,sticky='w')
            #position=[("Verticale","v"),("Horizental","h")]
            pos=StringVar()
            b=Checkbutton(frame,background='ivory3',font=("Helvetica", 12),text="Échelle linéaire",variable=pos,command=lambda:self.afficher_p("horizentale"))
            b.grid(row=row,column=2,sticky='w')
            liste=[b,e,f,g,h,i]
            self.liste_modif=""
            b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.mofi_question(frame,rt,numsec_reel,liste,b,row+5,liste_max,b_ok))
            #,command=lambda:self.modifier_contenu(frame,st,qt,rt,tt,b,liste,0))
            b.grid(row=row, column=3)
        elif(rt[2]=="supprimer"):
            row+=1
            b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Supprimer question",command=lambda:self.mofi_question(frame,rt,numsec_reel,"vv",b,row,liste_max,b_ok))
            b.grid(row=row,columnspan=2)
        elif(rt[2]=="libre"):
            row+=1
            ln=Label(frame,text="Note:",font=("Helvetica", 13),background='ivory3')
            ln.grid(row=row,column=0)
            note=Entry(frame,width=10,borderwidth=5)
            note.grid(row=row,column=1)
            row+=1  
            b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Modifier note",command=lambda:self.mofi_question(frame,rt,numsec_reel,note.get(),0,row,liste_max,b_ok))
            b.grid(row=row, columnspan=2)
        elif(rt[2]=="ajouter"):
            row+=1
            self.mofi_question(frame,rt,numsec_reel,"vv","vv",row,liste_max,b_ok)
        else:
            self.mofi_question(frame,rt,numsec_reel,"bb","bb",row,liste_max,b_ok)


    def mofi_question(self,frame,rt,numsec_reel,nom,b,row,liste_max,b_ok):#apelle modifier_type pour rt=type
        numq=1
        if(len(self.sections[numsec_reel])!=1):
            numq=int(self.numeroq.get())
        if(rt[2]=="contenu"):
            self.sections[numsec_reel][numq-1][1]=[nom]
        elif(rt[2]=="numero"):
            b.destroy()
            if(rt[0]=="section"):
                l=self.sections[numsec_reel][int(self.numeroq1.get())-1]
                self.sections[numsec_reel][int(self.numeroq1.get())-1]=self.sections[numsec_reel][numq-1]
                self.sections[numsec_reel][numq-1]=l
            else:
                d=self.numero_question()
                numq1=1
                for i,j in d.items():
                    if(i==int(self.numeroq1.get())):
                        numq1=j[0]
                l=self.sections[numq1]
                self.sections[numq1]=self.sections[numsec_reel]
                self.sections[numsec_reel]=l
            frame.destroy()
        elif(rt[2]=="libre"):
            if(nom.isdigit()!=True):
                tkinter.messagebox.showerror("Error", "Veuillez entrer un chiffre!")
            else:
                print("LIBRE")
                print(self.sections[numsec_reel][numq-1])
                self.sections[numsec_reel][numq-1][5]=[nom]
                print(self.sections[numsec_reel][numq-1])
                frame.destroy()
        elif(rt[2]=="type"):#il faut traiter cas des grilles
            b.destroy()
            print("JE SUIS LA")
            if(("horizentale" in self.liste_modif)==False and ("verticale" in self.liste_modif)==False and ("libre" in self.liste_modif)==False):
                c="verticale "
                c+=self.liste_modif
                self.liste_modif=c
            typ=self.liste_modif
            print(typ)
            self.modifier_type(frame,typ,b,numsec_reel,numq,nom,row)
            self.liste_modif=[]
        elif(rt[2]=="supprimer"):
            l=self.sections[numsec_reel]
            del l[numq-1]
            self.sections[numsec_reel]=l
            self.numq=len(self.sections[self.numsect])                
        elif(rt[2]=="ajouter"):#il faut traiter cas des grilles
            typr=self.sections[numsec_reel][numq-1][2][0]
            if("Grille" in typr):
                l1=Label(frame,text="Ajouter ligne:",font=("Helvetica", 13),background='ivory3')
                l1.grid(row=row,column=0,sticky='w')
                entre_ligne=Entry(frame, width=50,borderwidth= 5)
                entre_ligne.grid(row=row, column=1,padx=10,pady=10,sticky='w')
                b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ajouter ligne",command=lambda:self.ajouter_lig(numsec_reel,numq,entre_ligne.get()))
                b.grid(row=row,column=2)
                l2=Label(frame,text="Ajouter colonne:",font=("Helvetica", 13),background='ivory3')
                l2.grid(row=row+1,column=0,sticky='w')
                entre_colonne=Entry(frame, width=50,borderwidth= 5)
                entre_colonne.grid(row=row+1, column=1,padx=10,pady=10,sticky='w')
                b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ajouter ligne",command=lambda:self.ajouter_col(numsec_reel,numq,entre_colonne.get()))
                b.grid(row=row+1,column=2)
            else:
                row+=1
                l=Label(frame, text="Saisir réponse",font=("Helvetica", 13),background='ivory3')
                l.grid(row=row, column=0,sticky='w')
                #entrer rep
                reponse= Entry(frame, width=50,borderwidth= 5)
                reponse.grid(row=row, column=1,padx=10,pady=10,sticky='w')  
                ok=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ajouter",command=lambda:self.ajouter_dans_question(numsec_reel,numq,reponse.get()))
                #,command=lambda:self.modifier_contenu(frame,st,qt,rt,tt,reponse.get(),[],0))
                ok.grid(row=row+1,columnspan=2)
                
                #frame.destroy()
        else:
            self.modifier_reponse(frame,rt,row,liste_max,numsec_reel,numq)
        self.mise_a_jours()
        b_ok.config(state=DISABLED)
                    
    def modifier_type(self,frame,type_q,b,numsec_reel,numq,liste,row):#appelle ok_modifier_type
        b.destroy()
        for i in liste:
            i.config(state=DISABLED)
        if(type_q=="libre"):
            l1=Label(frame,text="Donner le nouveau nombre de lignes:",font=("Helvetica", 13),background='ivory3')
            l1.grid(row=row,column=0,sticky='w')
            nombre=Spinbox(frame,from_=1, to=10, width=2)
            nombre.grid(row=row,column=1,sticky='w')
            row+=1
            ok=Button(frame,background='ivory3',font=("Helvetica", 12),text="Modifier",command=lambda:self.ok_modifier_type(frame,int(nombre.get()),type_q,numsec_reel,numq))
            ok.grid(row=row,columnspan=3)
        elif("horizentale" in type_q):
            l1=Label(frame,text="Donner le nouveau nombre de réponses /ligne:",font=("Helvetica", 13),background='ivory3')
            l1.grid(row=row,column=0,sticky='w')
            nombre=Spinbox(frame,from_=2, to=10, width=2)
            nombre.grid(row=row,column=1,sticky='w')
            row+=1
            ok=Button(frame,background='ivory3',font=("Helvetica", 12),text="Modifier",command=lambda:self.ok_modifier_type(frame,int(nombre.get()),type_q,numsec_reel,numq))
            ok.grid(row=row,columnspan=3)
        else:
            ok=Button(frame,background='ivory3',font=("Helvetica", 12),text="Modifier",command=lambda:self.ok_modifier_type(frame,1,type_q,numsec_reel,numq))
            ok.grid(row=row,columnspan=3)    
    def ok_modifier_type(self,frame,nombre,type_q,numsec_reel,numq):
        print("tt")
        tay=self.sections[numsec_reel][numq-1][2][0]
        if("Grille" in type_q):
            print("je vais modifier une question en une grille")
            if("Grille" in tay):
                print("je suis une grille")
                if("unique" in type_q):
                    print("je vais me changer en unique")
                    type_q="Grille à choix uniques"
                    self.sections[numsec_reel][numq-1][2]=[type_q]
                elif("multiple" in type_q):
                    print("je vais me changer en multiple")
                    type_q="Grille à choix multiples"
                    self.sections[numsec_reel][numq-1][2]=[type_q]
                print(self.sections)
                self.mise_a_jours()
            else:
                tkinter.messagebox.showerror("Error", "C'est une question de type autre que grille vous ne pouvez pas la changer.\n Veullez voir Aide? pour plus d'info")
                frame.destroy()
        else:
            if("Grille" in tay):
                tkinter.messagebox.showerror("Error", "C'est une grille vous ne pouvez pas la changer.\n Veullez voir Aide? pour plus d'info")
                frame.destroy()
            else:
                if(type_q=="libre"):
                    self.sections[numsec_reel][numq-1][2]=[type_q]
                    self.sections[numsec_reel][numq-1][3]=[nombre]
                    self.sections[numsec_reel][numq-1][4]=[]
                    self.sections[numsec_reel][numq-1][5]=[0]
                elif("horizentale" in type_q):
                    self.sections[numsec_reel][numq-1][2]=[type_q]
                    self.sections[numsec_reel][numq-1][3]=[nombre]
                else: 
                    self.sections[numsec_reel][numq-1][2]=[type_q]
                    self.sections[numsec_reel][numq-1][3]=[1]
                self.mise_a_jours()
                print(self.sections[numsec_reel])
                frame.destroy()
    #fonctions pour ajouter des reponses aux # questions
    def ajouter_dans_question(self,numsec_reel,numq,nom):
        l=Information()
        l.egale(self.sections[numsec_reel][numq-1][4])
        l.ajouter(l.len()+1,nom)
        self.sections[numsec_reel][numq-1][4]=l.retourner()
        self.sections[numsec_reel][numq-1][5].append(0)
        self.mise_a_jours()
    def ajouter_col(self,numsec_reel,numq,nom):
        self.sections[numsec_reel][numq-1][4][0].append(nom)
        self.sections[numsec_reel][numq-1][5].append(0)
        self.mise_a_jours()
    def ajouter_lig(self,numsec_reel,numq,nom):
        self.sections[numsec_reel][numq-1][4][1].append(nom)
        self.sections[numsec_reel][numq-1][5].append(0)
        self.mise_a_jours()


    def modifier_reponse(self,frame,rt,row,n,sect,quest):
        lr=Label(frame,text="Donner le numéro réponse :",font=("Helvetica", 13),background='ivory3')
        lr.grid(row=row,column=0,sticky='w')
        if(n[2]==1):
            lr1=Label(frame,text="1",font=("Helvetica", 13),background='ivory3')
            lr1.grid(row=row,column=1,sticky='w')
        else:
            self.numeror=Spinbox(frame,from_=1, to=n[2], width=2)
            self.numeror.grid(row=row,column=1,sticky='w') 
        row+=1
        numero_utile=[sect,quest]
        b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.modi_reponse(frame,row,rt,b,n,numero_utile))
        b.grid(row=row,column=2)
    #front        
    def modi_reponse(self,frame,row,rt,b,n,numero_utile):#il faut traiter le cas des grilles dans ce qui suit
        numr=1
        typr=self.sections[numero_utile[0]][numero_utile[1]-1][2][0]
        if("Grille" in typr):
            if(rt[3]=="note"):
                if(len(self.sections[numero_utile[0]][numero_utile[1]-1][4][1])>1):
                    numr=int(self.numeror.get())
                b.destroy()
                numero_utile.append(numr)
                self.mod_ligne(frame,row+1,rt[3],[],[],numero_utile)
            else:
                a=len(self.sections[numero_utile[0]][numero_utile[1]-1][4][0])
                e=len(self.sections[numero_utile[0]][numero_utile[1]-1][4][1])
                if(a>1 or e >1):
                    numr=int(self.numeror.get())
                numero_utile.append(numr)
                row+=1
                b.destroy()
                b3=[]
                b1=Button(frame,background='ivory3',font=("Helvetica", 12),text="Modifier ligne",command=lambda:self.mod_ligne(frame,row+1,rt[3],b3,n,numero_utile))
                b1.grid(row=row,column=0)
                b2=Button(frame,background='ivory3',font=("Helvetica", 12),text="Modifier colonne",command=lambda:self.mod_colonne(frame,row+1,rt[3],b3,n,numero_utile))
                b2.grid(row=row,column=1)
                b3=[b1,b2]
        else:
            if(len(self.sections[numero_utile[0]][numero_utile[1]-1][4])>1):
                numr=int(self.numeror.get())
            if(rt[3]=="numero"):
                b.destroy()
                row+=1
                lq1=Label(frame,text="Donner le nouveau numéro de la réponse :",font=("Helvetica", 13),background='ivory3')
                lq1.grid(row=row,column=0,sticky='w')
                self.numeror1=Spinbox(frame,from_=1, to=n[2], width=2)
                self.numeror1.grid(row=row,column=1,sticky='w')
                b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.mofi_reponses_question(frame,rt[3],numero_utile[0],numero_utile[1],numr,"VV"))
                #,command=lambda:self.modifier_contenu(frame,st,qt,rt,tt,self.numeror1,[],0))
                b.grid(row=row+1, columnspan=2)
            elif(rt[3]=="contenu"):
                b.destroy()
                row+=1
                lq1=Label(frame,text="Saisir le nouveau titulaire de réponse :",font=("Helvetica", 13),background='ivory3')
                lq1.grid(row=row,column=0,sticky='w')
                saisie=Entry(frame, width=50,borderwidth= 5)
                saisie.grid(row=row, column=1,padx=10,pady=10,sticky='w') 
                row+=1
                ok=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.mofi_reponses_question(frame,rt[3],numero_utile[0],numero_utile[1],numr,saisie.get()))#,command=lambda:self.modifier_cont(frame,st,qt,rt,tt,row,n))
                ok.grid(row=row+1,columnspan=2)
            elif(rt[3]=="note"):
                b.destroy()
                row+=1
                ln=Label(frame,text="Note:",font=("Helvetica", 13),background='ivory3')
                ln.grid(row=row,column=0)
                note=Entry(frame,width=10,borderwidth=5)
                note.grid(row=row,column=1)
                row+=1
                b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Modifier note",command=lambda:self.mofi_reponses_question(frame,rt[3],numero_utile[0],numero_utile[1],numr,note.get()))#,command=lambda:self.modifier_contenu(frame,st,qt,rt,tt,note.get(),[],0))
                b.grid(row=row, columnspan=2)
            elif(rt[3]=="supprimer"):
                row+=1
                b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Supprimer",command=lambda:self.mofi_reponses_question(frame,rt[3],numero_utile[0],numero_utile[1],numr,"vv"))
                #,command=lambda:self.modifier_contenu(frame,st,qt,rt,tt,"supp",[],0))
                b.grid(row=row, columnspan=2)
    #back
    def mofi_reponses_question(self,frame,tt,numsec_reel,numq,numr,nom):
        if(tt=="contenu"):
            self.sections[numsec_reel][numq-1][4][numr-1]=(numr,nom)
            frame.destroy()
        elif(tt=="numero"):
            l=Information()
            l.egale(self.sections[numsec_reel][numq-1][4])
            l.permuter(numr,int(self.numeror1.get()))
            self.sections[numsec_reel][numq-1][4]=l.retourner()
            frame.destroy()
        elif(tt=="supprimer"):
            l=Information()
            l.egale(self.sections[numsec_reel][numq-1][4])
            l.supprimer(numr)
            self.sections[numsec_reel][numq-1][4]=l.retourner()
            #frame.destroy()
        else:   
            if(nom.isdigit()!=True):
                tkinter.messagebox.showerror("Error", "Veuillez entrer un chiffre!")
            else:
                self.sections[numsec_reel][numq-1][5][numr-1]=int(nom)
                print(self.sections[numsec_reel][numq-1][5])
        self.mise_a_jours()
    
    #modifier les reponses d'une grille
    def mod_colonne(self,frame,row,rt,b,n,numero_utile):
        for i in b:
            i.config(state=DISABLED)
        if(rt=="numero"):
            lq1=Label(frame,text="Donner le nouveau numéro de la colonne :",font=("Helvetica", 13),background='ivory3')
            lq1.grid(row=row,column=0,sticky='w')
            self.numeror1=Spinbox(frame,from_=1, to=n[2], width=2)
            self.numeror1.grid(row=row,column=1,sticky='w')
            b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.modifier_cont_grille(frame,row,rt,b,numero_utile,0))
            b.grid(row=row+1, columnspan=2)
        elif(rt=="contenu"):
            lq1=Label(frame,text="Saisir le nouveau titulaire de réponse :",font=("Helvetica", 13),background='ivory3')
            lq1.grid(row=row,column=0,sticky='w')
            saisie=Entry(frame, width=50,borderwidth= 5)
            saisie.grid(row=row, column=1,padx=10,pady=10,sticky='w') 
            row+=1
            ok=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.mofi_reponse_grille(rt,saisie.get(),frame,numero_utile,0))
            ok.grid(row=row+1,columnspan=2)
        elif(rt=="supprimer"):
            b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Supprimer",command=lambda:self.mofi_reponse_grille(rt,"vv",frame,numero_utile,0))
            b.grid(row=row, columnspan=2)    
    def mod_ligne(self,frame,row,rt,b,n,numero_utile):
        for i in b:
            i.config(state=DISABLED)
        if(rt=="numero"):
            lq1=Label(frame,text="Donner le nouveau numéro de la ligne :",font=("Helvetica", 13),background='ivory3')
            lq1.grid(row=row,column=0,sticky='w')
            self.numeror1=Spinbox(frame,from_=1, to=n[2], width=2)
            self.numeror1.grid(row=row,column=1,sticky='w')
            b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ok")
            b.grid(row=row+1, columnspan=2,command=lambda:self.modifier_cont_grille(frame,row,rt,b,numero_utile,1))
        elif(rt=="contenu"):
            lq1=Label(frame,text="Saisir le nouveau titulaire de réponse :",font=("Helvetica", 13),background='ivory3')
            lq1.grid(row=row,column=0,sticky='w')
            saisie=Entry(frame, width=50,borderwidth= 5)
            saisie.grid(row=row, column=1,padx=10,pady=10,sticky='w') 
            row+=1
            ok=Button(frame,background='ivory3',font=("Helvetica", 12),text="Ok",command=lambda:self.mofi_reponse_grille(rt,saisie.get(),frame,numero_utile,1))
            ok.grid(row=row+1,columnspan=2)
        elif(rt=="supprimer"):
            b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Supprimer",command=lambda:self.mofi_reponse_grille(rt,"vv",frame,numero_utile,1))
            b.grid(row=row, columnspan=2)
        else:
            ln=Label(frame,text="Note:",font=("Helvetica", 13),background='ivory3')
            ln.grid(row=row,column=0)
            note=Entry(frame,width=10,borderwidth=5)
            note.grid(row=row,column=1)
            row+=1
            b=Button(frame,background='ivory3',font=("Helvetica", 12),text="Modifier note",command=lambda:self.mofi_reponse_grille(rt,note.get(),frame,numero_utile,1))
            b.grid(row=row, columnspan=2)
    #front
    def modifier_cont_grille(self,frame,row,rt,b,numero_utile,lc):
        if(rt=="numero"):
            row+=1
            b.destroy()
            permuter=Button(frame,background='ivory3',font=("Helvetica", 12),text="Permuter",command=lambda:self.mofi_reponse_grille(rt,"vv",frame,numero_utile,lc))
            permuter.grid(row=row+1,columnspan=2)
    #lc colonne ou ligne
    def mofi_reponse_grille(self,rt,nom,frame,numero_utile,lc):
        if(rt=="numero"):
            l=self.sections[numero_utile[0]][numero_utile[1]-1][4][lc]
            a=l[numero_utile[2]-1]
            l[numero_utile[2]-1]=l[int(self.numeror1.get())-1]
            l[int(self.numeror1.get())-1]=a
            self.sections[numero_utile[0]][numero_utile[1]-1][4][lc]=l
            self.mise_a_jours()
        elif(rt=="contenu"):
            l=self.sections[numero_utile[0]][numero_utile[1]-1][4][lc]
            l[numero_utile[2]-1]=nom
            self.sections[numero_utile[0]][numero_utile[1]-1][4][lc]=l
            self.mise_a_jours()
        elif(rt=="supprimer"):
            l=self.sections[numero_utile[0]][numero_utile[1]-1][4][lc]
            del l[numero_utile[2]-1]
            self.sections[numero_utile[0]][numero_utile[1]-1][4][lc]=l
            self.mise_a_jours()
        else:
            if(nom.isdigit()!=True):
                tkinter.messagebox.showerror("Error", "Veuillez entrer un chiffre!")
            else:
                l=self.sections[numero_utile[0]][numero_utile[1]-1][4][lc]
                l[numero_utile[2]-1]=int(nom)
                self.sections[numero_utile[0]][numero_utile[1]-1][4][lc]=l
                self.mise_a_jours()
   
   #modifier information
    def modifier_information(self,info):
        frame= Tk()
        frame.configure(background='ivory3')
        l=Label(frame,text="Donner numero information: ",font=("Helvetica", 13),background='ivory3')
        l.grid(row=0,column=0,sticky='w')
        if(self.informations.len()==1):
            l1=Label(frame,text="1",font=("Helvetica", 13),background='ivory3')
            l1.grid(row=0,column=1,sticky='w')
        else:
            self.num_info=Spinbox(frame,from_=1, to=self.informations.len(), width=2)
            self.num_info.grid(row=0,column=1,sticky='w')
        if(info=="Modifier"):
            frame.title("Modifier information")
            lentry=Label(frame,text="Saisir information: ",font=("Helvetica", 13),background='ivory3')
            lentry.grid(row=1,column=0,sticky='w')
            entry_info=Entry(frame,width=30,borderwidth=5)
            entry_info.grid(row=1,column=1,sticky='w')
            b=Button(frame,text="Modifier",command=lambda:self.ok_modifier_information(entry_info.get()),background='ivory3',font=("Helvetica", 12))
            b.grid(row=0,column=2,rowspan=2)
        else:
            frame.title("Supprimer information")
            b=Button(frame,text="Supprimer",command=lambda:self.supprimer_info("rien",frame),background='ivory3',font=("Helvetica", 12))
            b.grid(row=0,column=2,rowspan=2)
    def ok_modifier_information(self,information):
        print("hihiahaiha")
        if(self.informations.len()==1):
            num=1
        else:
            num=int(self.num_info.get())
        print(num)
        self.informations.modifier(num,information)
        self.mise_a_jours()             
    def supprimer_info(self,info,frame):
        if(self.informations.len()==1):
            num=1
        else:
            num=int(self.num_info.get())
        self.numinf-=1
        self.informations.supprimer(num)
        self.mise_a_jours()
        frame.destroy()

    #modifier nombre de ligne dans un tableau long
    def tableau_long(self,st):
        frame=Tk()
        frame.title("Ajuster tableau")
        frame.configure(background='ivory3')
        if(st=="section"):
            l=Label(frame,text="Donner numero section: ",font=("Helvetica", 13),background='ivory3')
            l.grid(row=0,column=0,sticky='w')
            if(len(self.numero_section())==1):
                l1=Label(frame,text="1",font=("Helvetica", 13),background='ivory3')
                l1.grid(row=0,column=1,sticky='w')
            else:
                self.num_sectionmod=Spinbox(frame,from_=1, to=len(self.numero_section()), width=2)
                self.num_sectionmod.grid(row=0,column=1,sticky='w')
            b=Button(frame,text="Ok",command=lambda:self.ok_section(frame))
            b.grid(row=0,column=2,rowspan=2)    
        else:    
            l=Label(frame,text="Donner numero question: ",font=("Helvetica", 13),background='ivory3')
            l.grid(row=0,column=0,sticky='w')
            if(len(self.numero_question())==1):
                l1=Label(frame,text="1",font=("Helvetica", 13),background='ivory3')
                l1.grid(row=0,column=1,sticky='w')
            else:
                self.num_questionmod=Spinbox(frame,from_=1, to=len(self.numero_question()), width=2)
                self.num_questionmod.grid(row=0,column=1,sticky='w')
            b=Button(frame,text="Ok",command=lambda:self.ok_question(frame,1,b))
            b.grid(row=0,column=2,rowspan=2)   
    def ok_question(self,frame,row,b):
        b.destroy()
        l1=Label(frame,text="Nombre de ligne: ",font=("Helvetica", 13),background='ivory3')
        l1.grid(row=row,column=0,sticky='w')
        self.nombre_l_tab=Spinbox(frame,from_=1 ,to=20)
        self.nombre_l_tab.grid(row=row,column=1,sticky='w')
        b=Button(frame,text="Ok",command=self.egale)
        b.grid(row=row,column=2)
    def egale(self):
        self.tab_long=int(self.nombre_l_tab.get())
        print(self.tab_long)
        self.mise_a_jours()
    def ok_section(self,frame):
        l=Label(frame,text="Donner numero question: ",font=("Helvetica", 13),background='ivory3')
        l.grid(row=1,column=0,sticky='w')
        if(len(self.numero_question())==1):
            l1=Label(frame,text="1",font=("Helvetica", 13),background='ivory3')
            l1.grid(row=1,column=1,sticky='w')
        else:
            self.num_questionmod=Spinbox(frame,from_=1, to=len(self.numero_question()), width=2)
            self.num_questionmod.grid(row=1,column=1,sticky='w')
        b=Button(frame,text="Ok",command=self.ok_question(frame,2,b))
        b.grid(row=1,column=2)   
    
    #supprimer section
    def supprimer_section(self, info):
        frame= Tk()
        frame.title("Supprimer section")
        frame.configure(background='ivory3')
        l=Label(frame,text="Numéro section: ",font=("Helvetica", 13),background='ivory3')
        l.grid(row=0,column=0,sticky='w')
        if(len(self.numero_section())==1):
            l=Label(frame,text="1",font=("Helvetica", 13),background='ivory3')
            l.grid(row=0,column=1,sticky='w')
        else:
            self.num_sectionsup=Spinbox(frame,from_=1, to=len(self.numero_section()), width=2)
            self.num_sectionsup.grid(row=0,column=1,sticky='w')
        b=Button(frame,text="Supprimer",command=lambda:self.ok_supprimer_section(frame),background='ivory3',font=("Helvetica", 12))
        b.grid(row=0,column=2,rowspan=2)
    def ok_supprimer_section(self,frame):
        if(len(self.numero_section())==1):
            num=1
        else:
            num=int(self.num_sectionsup.get())
        numsec_reel=self.numero_section()[num][0]
        del self.sections[numsec_reel]
        self.update_sections()
        self.section.supprimer(numsec_reel)
        self.numsect-=1
        self.mise_a_jours() 
        frame.destroy()   
    def update_sections(self):
        l={}
        j=1
        for k in self.sections.values():
            l[j]=k
            j+=1
        self.sections={}
        self.sections=l
    
    #supprimer question
    def supprimer_question(self,info):
        frame= Tk()
        frame.title("Supprimer question")
        frame.configure(background='ivory3')
        l=Label(frame,text="Numéro question: ",font=("Helvetica", 13),background='ivory3')
        l.grid(row=0,column=0,sticky='w')
        if(len(self.numero_question())==1):
            l=Label(frame,text="1",font=("Helvetica", 13),background='ivory3')
            l.grid(row=0,column=1,sticky='w')
        else:
            self.num_questionsup=Spinbox(frame,from_=1, to=len(self.numero_question()), width=2)
            self.num_questionsup.grid(row=0,column=1,sticky='w')
        b=Button(frame,text="Supprimer",command=lambda:self.ok_supprimer_question(frame),background='ivory3',font=("Helvetica", 12))
        b.grid(row=0,column=2,rowspan=2)
    def ok_supprimer_question(self,frame):
        if(len(self.numero_question())==1):
            num=1
        else:
            num=int(self.num_questionsup.get())
        numsec_reel=self.numero_question()[num][0]
        del self.sections[numsec_reel]
        self.update_sections()
        self.section.supprimer(numsec_reel)
        self.numsect-=1
        self.mise_a_jours() 
        frame.destroy()  
    #fonction qui genere le pdf+ note + fichier.tex
    def enregister(self,path):
        if(str(self.donner_note.get())=="o" or str(self.donner_note.get())=="1"):
            self.note.inserer_rep_avec_note(self.sections,self.titre,path)
        else:
            self.note.inserer_rep_sans_note(self.sections,self.titre,path)
    
    #fonction save dans menubar
    def callback_formulaire(self,path):
        if tkinter.messagebox.askyesno('','Voulez vous enregister ?'):
            self.enregister(path)
        else:
            nom1="form.pdf"
            nom2="form.tex"
            nom3="fiche_des_notes_du_form.xls"
            if(os.path.exists(nom1)):
                os.remove(nom1)
            elif(os.path.exists(nom2)):
                os.remove(nom2)
            elif(os.path.exists(nom3)):
                os.remove(nom3)
    #mise a jour du pdf a chaque fois qu'on ajoute une information 
    def mise_a_jours(self):
        a=StringVar()
        b=StringVar()
        a=self.date.get()[0]
        b=self.date.get()[1]
        if(a!='' or b!=''):
            date_format=a+"/"+b
        else:
            date_format="" 
        self.titre=self.titre1.get()
        nom="form.pdf"
        if(os.path.exists(nom)):
            self.frame1.destroy()
            self.d=latex()
            os.remove(nom)
            self.frame1 =Frame(self.root,width=850)
            self.frame1.grid(column=1,row=0)
            self.frame1.grid_propagate(0)
        else:
            self.frame1 =Frame(self.root,width=850)
            self.frame1.grid(column=1,row=0)
            self.frame1.grid_propagate(0)
        self.d.generate(self.titre1.get(),self.etab.get(),date_format,self.informations,self.taille_Radio,
                                            self.section,self.sections,self.tab_long,self.repfic)
        v = DocViewer(self.frame1, width=805, height=800)
        v.pack(side="top", expand=1, fill="both")
        #v.grid(row=0,column=0,sticky='w')
        v.display_file(nom)
                    
    def afficher (self,r:dict):
        s="["
        if(r==[]):
            print ("vide")
            return "[]"
        else:
            for i in r:
                s+=str(i)
                s+=","
            s+="]"
            return s
    def afficher_dict(self,r):
        s="{"
        for i,j in r.items():
            s+="(cle:"+str(i)+","+"valeur:"+str(j)+")"
        s+="}"
        return s

    def initialiser_under_section(self):
        #ki nenzel ajouter section wela fin section kol shay yetnaha
        liste_init=[self.label_note,self.entry_note,self.button_ok_libre,self.donner_nbr_ligne,self.nombre_ligne,
        self.donner_nbr_rep_par_ligne,self.nombre_rep_par_ligne,self.button_ok,self.saisie_reponse,self.entrer_rep,
        self.entrer_reponse]
        self.question.delete('1.0', END)
        for i in liste_init:
            i.destroy()


if __name__ == "__main__":
    
    
    hi=Format()
    
