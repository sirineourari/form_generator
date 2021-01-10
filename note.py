from xlwt import Workbook
#from Section import Information
class note:
    def __init__(self):
        self.book= Workbook()
        self.feuill=self.book.add_sheet('page1')        
    def inserer_rep_sans_note(self,sections,titre,path):
        feuil1= self.feuill
        k,n=0,1
        for i in sections.values():
            for j in i:
                g=j[1][0]
                feuil1.write(k,0,j[2][0])
                q="q"+str(n)
                feuil1.write(k+1,1,q)
                n+=1
                feuil1.write(k,1,g) 
                m=2  
                b='a' 
                print("type")
                print (j[2])
                print(j[4])
                if("Grille" in j[2][0]):
                    for a in j[4][1]:
                        feuil1.write(k,m,a)
                        feuil1.write(k+1,m,b)
                        b=chr(ord(b)+1)
                        m+=1
                else:            
                    for a in j[4]:
                        feuil1.write(k,m,str(a[1]))
                        feuil1.write(k+1,m,b)
                        b=chr(ord(b)+1)
                        m+=1
                k+=2  
        self.enregistrer()
    def inserer_rep_avec_note(self,sections,titre,path):
        feuill=self.feuill
        k,p=0,1
        for n in sections.values():
            for j in n:
                g=j[1][0]
                feuill.write(k,0,j[2][0])
                q="q"+str(p)
                feuill.write(k+1,1,q)
                p+=1
                feuill.write(k,1,g)
                m=2
                if("Grille" in j[2][0]):
                    compteur=0
                    for a in j[4][1]:
                        feuill.write(k,m,a)
                        feuill.write(k+1,m,j[5][compteur])
                        m+=1
                        compteur+=1
                else:
                    print("MAMA")
                    print(j)
                    if(j[2][0]=="libre"):
                        feuill.write(k+1,m,j[5])
                    else:
                        compteur=0
                        for a in j[4]:
                            feuill.write(k,m,str(a[1]))
                            feuill.write(k+1,m,j[5][compteur])
                            m+=1
                            compteur+=1
                    k+=2
        self.enregistrer()
    def enregistrer(self):
        self.book.save('fiche_des_notes_du_form.xls')
    

        

