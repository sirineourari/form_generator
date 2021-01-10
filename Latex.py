from pylatex import Document, Tabular,Command, Enumerate ,MultiColumn,Package,PageStyle,LongTabu
from pylatex.utils import NoEscape
import os
from Section import Information


class latex:
    def __init__(self):
        self.doc=Document()
        self.doc.packages.append(Package('enumitem',options="inline"))
        self.doc.packages.append(Package('geometry'))
        self.doc.packages.append(Package('tasks'))
        self.doc.packages.append(Package('supertabular'))
        self.g=1
        self.g1=1
        self.g2=1
    
    def generate(self,m,etab,date,info:list,taille,sect:Information,section:dict,tab,path):
        nom="form.pdf"
        if(os.path.exists(nom)):
            os.remove(nom)
        self.format(self.doc,m,etab,date,taille)
        self.informations(self.doc,info)
        #print(sect.retourner())
        for i,j in section.items():
            a=sect.recup(i)
            if(a!="rien"):
                self.doc.append(Command(NoEscape(r'section{'+a+'}')))
                if(len(j)>0):
                    self.generate1(self.g,j,tab)
                    self.g=1
                    self.g1=1
                    self.doc.append("\n")
                    self.doc.append("\n")
            else:
                self.generate1(self.g2,j,tab)
                self.g2+=1
        if(path!=""):
            path+="/"
        self.doc.generate_pdf(filepath=path+"form",clean_tex=True)
    #generer les pdfs
    def generate1(self,g1,liste_quest,m):    
        g=g1
        for j in liste_quest:
            self.doc.append(Command(NoEscape(r'fbox{')))
            self.doc.append(Command(NoEscape(r'begin{minipage}{1')))
            self.doc.append(Command(NoEscape(r'textwidth}')))
            #if(len(str(j[1][0]))>84):
            #    self.question_longue(self.doc,str(j[1][0]),g)
            #else:
            self.question(self.doc,str(j[1][0]),g)
            if("Grille" in j[2][0]):
                shape=""
                if("unique" in j[2][0]):
                    shape="unique"
                else:
                    shape="multiple"
                if(m>0):
                    self.Tab_longue(self.doc,shape,j[4],m)
                else:
                    self.grille(self.doc,shape,j[4])
            else:
                if(j[2][0]=="libre"):
                    self.rep_libre(self.doc,j[3][0])
                else:
                    if(len(j[4])>=1):
                        if(j[2][0]=="horizentale multiple"):
                            self.rep_hm(self.doc,j[4],j[3][0])
                        elif(j[2][0]=="horizentale unique"):
                            self.rep_hu(self.doc,j[4],j[3][0])
                        elif(j[2][0]=="verticale unique"):
                            self.rep_vu(self.doc,j[4])
                        elif(j[2][0]=="verticale multiple"):
                            self.rep_vm(self.doc,j[4]) 
                    else:
                        pass       
            self.doc.append(Command(NoEscape(r'end{minipage}}')))
            self.doc.append("\n")
            self.doc.append("\n")
            g+=1
    def rep_libre(self,doc,l):
        i=0
        while(i<l):
            doc.append(Command("par"))
            doc.append(Command(NoEscape(r'dotfill')))
            i+=1
        doc.append("\n")
    #format generale
    def format(self,doc,m,etab,date,taille):
        page_style = PageStyle("fancyhdr")
        doc.preamble.append(page_style)
        doc.change_document_style("fancy")
        doc.preamble.append(Command(NoEscape(r'setlength{')))
        doc.preamble.append(Command(NoEscape(r'headheight}{27.06pt}')))
        doc.preamble.append(Command(NoEscape(r'renewcommand')))
        doc.preamble.append(Command(NoEscape(r'headrulewidth{1pt}')))
        doc.preamble.append(Command(NoEscape(r'fancyhead[R]{'+etab+'}')))
        doc.preamble.append(Command(NoEscape(r'renewcommand')))
        doc.preamble.append(Command(NoEscape(r'footrulewidth{1pt}')))
        doc.preamble.append(Command(NoEscape(r'fancyfoot[C]{')))
        doc.preamble.append(Command(NoEscape(r'textbf{Page')))
        doc.preamble.append(Command(NoEscape(r'thepage}}')))
        doc.preamble.append(Command(NoEscape(r'fancyfoot[R]{'+date+'}')))
        self.radio_button(taille,doc)
        #carreau
        self.square_button(doc)
        #entete
        doc.append(Command(NoEscape(r'begin{center}')))
        doc.append(Command(NoEscape(r'bf')))
        doc.append(Command(NoEscape(r'huge{'+m+'}')))
        doc.append(Command((NoEscape(r'end{center}'))))
    

    def square_button(self,doc):
        doc.preamble.append(Command(NoEscape(r'newcommand{\square}{')))
        doc.preamble.append(Command(NoEscape(r'begin{tabular}{|c|}')))
        doc.preamble.append(Command(NoEscape(r'hline')))
        doc.preamble.append(Command("\\ "))
        doc.preamble.append(Command(NoEscape(r'hline')))
        doc.preamble.append(Command(NoEscape(r'end{tabular}}')))

    def radio_button(self,taille,doc):
        doc.packages.append(Package("tikz"))
        doc.preamble.append(Command(NoEscape(r'makeatletter')))
        doc.preamble.append(Command(NoEscape(r'newcommand*{\radiobutton}{')))
        doc.preamble.append(Command(NoEscape(r'@ifstar{\@radiobutton0}{\@radiobutton1}}')))
        doc.preamble.append(Command(NoEscape(r'newcommand*{\@radiobutton}[1]{')))
        doc.preamble.append(Command(NoEscape(r'begin{tikzpicture}%')))
        doc.preamble.append(Command(NoEscape(r'pgfmathsetlengthmacro\radius{height("X")}')))
        doc.preamble.append(Command(NoEscape(r'draw[radius='+taille+']circle;')))
        doc.preamble.append(Command(NoEscape(r'end{tikzpicture}}%')))
        doc.preamble.append(Command(NoEscape(r'makeatother')))

    def informations(self,doc,j:list):
        if(j.len()!=0):
            for i in range(j.len()):
                a=j.recup(i+1)
                doc.append(a+":............................")
                doc.append("\n")
            doc.append("\n")
        else: 
            pass
        
    def question(self,doc,quest,num):
        #doc.append(Command("par"))
        #doc.append(NoEscape(r'\hspace{1cm}'))
        doc.append(str(num)+"-"+quest)
        #doc.append("\n")

    def question_longue(self,doc,quest,num):
        m=len(quest)%84
        c=[]
        n=0 
        k=0
        while(n<len(quest) and k <=m):
            doc.append(Command("par"))
            doc.append(NoEscape(r'\hspace{1cm}'))
            c=quest[n:84+n]
            if(k==0):
                doc.append(str(num)+"-"+''.join(c))
                c=[]
                n+=84
            else:
                doc.append(''.join(c))
                c=[]
                n+=84
            k+=1
        doc.append("\n")
    def rep_vu(self,doc,rep):
        doc.append(Command(NoEscape(r'begin{itemize}')))
        for a in rep:
            doc.append(Command(NoEscape(r'item[')))
            doc.append(Command(NoEscape(r'radiobutton]')))
            doc.append(Command(NoEscape(r'hspace{2mm}')))
            doc.append(a[1])
        doc.append(Command(NoEscape(r'end{itemize}')))

    def rep_vm(self,doc,rep):
        doc.append(Command(NoEscape(r'begin{itemize}')))
        for s in rep:
            doc.append(Command(NoEscape(r'item[\square]')))
            doc.append(Command(NoEscape(r'hspace{2mm}')))
            doc.append(s[1])
        doc.append(Command(NoEscape(r'end{itemize}')))   
    def rep_hu(self,doc,j,n):   
        p=int(n)
        if(p==5):
            p+=1
        elif(p==4):
            p+=1
        m=str(p)      
        doc.append(Command(NoEscape(r'begin{tasks}(')))
        doc.append(m)
        doc.append(')')
        if(n==4):
            self.fixed_u(doc,int(n),j)
        elif(n==5):
            self.fixed_u(doc,int(n),j)
        else:
            for a in j:        
                doc.append(Command(NoEscape(r'task[')))
                doc.append(Command(NoEscape(r'radiobutton]')))
                doc.append(Command(NoEscape(r'hspace{2mm}')))    
                doc.append(a[1])
            doc.append(Command(NoEscape(r'end{tasks}')))
    #fonction pour les cas n=4 ou n=5 
    #il y a superpositin des radio button et fbox
    def fixed_u(self,doc,n,j:list):
        i=1
        for a in j:        
            doc.append(Command(NoEscape(r'task[')))
            doc.append(Command(NoEscape(r'radiobutton]')))
            doc.append(Command(NoEscape(r'hspace{2mm}')))    
            if(i==n):
                i=0
                doc.append(a[1])
                doc.append(Command(NoEscape(r'startnewitemline')))
            else:
                doc.append(a[1])
            i+=1
        doc.append(Command(NoEscape(r'end{tasks}')))

    def fixed_m(self,doc,n,j:list):
        i=1
        for a in j:        
            doc.append(Command(NoEscape(r'task[')))
            doc.append(Command(NoEscape(r'square]')))
            doc.append(Command(NoEscape(r'hspace{2mm}')))    
            if(i==n):
                i=0
                doc.append(a[1])
                doc.append(Command(NoEscape(r'startnewitemline')))
            else:
                doc.append(a[1])
            i+=1
        doc.append(Command(NoEscape(r'end{tasks}')))

    def rep_hm(self,doc,j,n):
        p=int(n)
        if(p==5):
            p+=1
        elif(p==4):
            p+=1
        m=str(p)      
        doc.append(Command(NoEscape(r'begin{tasks}(')))
        doc.append(m)
        doc.append(')')
        if(n==4):
            self.fixed_m(doc,int(n),j)
        elif(n==5):
            self.fixed_m(doc,int(n),j)
        else:
            for a in j:        
                doc.append(Command(NoEscape(r'task[')))
                doc.append(Command(NoEscape(r'square]')))
                doc.append(Command(NoEscape(r'hspace{2mm}')))    
                doc.append(a[1])
            doc.append("\n")
            doc.append(Command(NoEscape(r'end{tasks}')))
    
    def back(self,doc,j,n):
        m=(75-(n*2))/n
        if (m%n!=0):
            m+=1
        doc.append(Command(NoEscape(r'begin{tasks}(')))
        doc.append(n)
        doc.append(')')
        for a in j:        
            doc.append(Command(NoEscape(r'task[\square]')))
            doc.append(Command(NoEscape(r'hspace{2mm}')))
            if(len(a)>m):
                doc.append(Command(NoEscape(r'rlap')))
                #doc.append(a)
                #doc.append(Command(NoEscape(r'startnewitemline')))
                self.ajuster(a,m,doc)
            else:
                doc.append(a)
        doc.append(Command(NoEscape(r'end{tasks}')))

    def ajuster(self,j,m,doc):
        l=[]
        k=0
        i=0
        while( k < len(j) ):
            
            if(i<m):
                l.append(j[k])
                i+=1
            else:
                doc.append(''.join(l))
                doc.append("\n")
                l=[]
                i=0
            k+=1
    def apostrophe(self,mot):
        l=[]
        for i in mot:
            if (i=='\''):
                l.append("\\"+i)
            else:
                l.append(i)
        return ''.join(l)
    

    def grille(self,doc,shape,liste):
        doc.append("\n")
        if(shape=="unique"):
            typ=(Command(NoEscape(r'radiobutton')),)
            #typ=("a",)
        else:
            typ=(Command(NoEscape(r'square')),)
            #typ=("b",)
        if(liste[0]==[]):
            n=1
            tupc=(" "," ",)
        else:
            lis=[" "]
            for i in liste[0]:
                lis.append(i)
            #tuple colonne
            tupc=tuple(lis)
            n=len(tupc)-1
            print(tupc)
        #chaine=["p{1.5cm}"]
        chaine="c"
        for i in range(n):
            chaine+="c"
        with doc.create(Tabular(table_spec=chaine)) as table:
            table.add_row(tupc)
            #tuple ligne
            if(liste[1]!=[]):
                for i in liste[1]:
                    l1=[i]
                    tupl=tuple(l1)
                    for i in range(len(chaine)-1):
                        tupl=tupl+typ
                    table.add_row(tupl)
                    table.add_empty_row()
    def Tab_longue(self,doc,shape,liste,m):
        doc.append("\n")
        if(shape=="unique"):
            typ=(Command(NoEscape(r'radiobutton')),)
            #typ=("a",)
        else:
            typ=(Command(NoEscape(r'square')),)
            #typ=("b",)
        if(liste[0]==[]):
            n=1
            tupc=(" "," ",)
        else:
            lis=[" "]
            for i in liste[0]:
                lis.append(i)
            #tuple colonne
            tupc=tuple(lis)
            n=len(tupc)-1
            print(tupc)
        #chaine=["p{1.5cm}"]
        chaine="c"
        for i in range(n):
            chaine+="c"
        liste1=liste[1][0:m]
        liste2=liste[1][m:]
        print("LES LISTES")
        print(liste[1])
        print(liste1)
        print(liste2)
        with doc.create(Tabular(table_spec=chaine)) as table:
            table.add_row(tupc)
            #tuple ligne
            if(liste1!=[]):
                for i in liste1:
                    l1=[i]
                    tupl=tuple(l1)
                    for i in range(len(chaine)-1):
                        tupl=tupl+typ
                    table.add_row(tupl)
                    table.add_empty_row()
        doc.append("\n")
        doc.append("\n")
        doc.append(Command(NoEscape(r'end{minipage}}')))
        doc.append("\n")
        doc.append("\n")
        doc.append(Command(NoEscape(r'fbox{')))
        doc.append(Command(NoEscape(r'begin{minipage}{1')))
        doc.append(Command(NoEscape(r'textwidth}')))
        with doc.create(Tabular(table_spec=chaine)) as table:
            #tuple ligne
            if(liste2!=[]):
                for i in liste2:
                    l1=[i]
                    tupl=tuple(l1)
                    for i in range(len(chaine)-1):
                        tupl=tupl+typ
                    table.add_row(tupl)
                    table.add_empty_row()

    def derniere_rep(self,rep):
        caractere_speciaux=['(',')','{','}','[',']','\\','/','\'','#','$','^','&','+','=','-','*',',','?','_','~','!','|','%']
        k=""
        for i in rep :
            a=i in caractere_speciaux
            if(a== False):
                k+=str(i)
            else:
                k+=" "
                k+=str(i)
                k+=" "
        return k

    def afficher_dict(self,r):
        s="{"
        for i,j in r.items():
            s+="(cle:"+str(i)+","+"valeur:"+str(j)+")"
        s+="}"
        return s

