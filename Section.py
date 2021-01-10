class Information:
    def __init__(self):
        self.r=[]
    def ajouter(self,num,rep):
        self.r.append((num,rep))

    def supprimer(self,num):
        for i in self.r:
            if(i[0]==num):
                a=self.r.index(i)
                del self.r[a]
        self.update()
    
    #mise a jour des listes
    def update(self):
        l=[]
        j=1
        for i in self.r:
            a=i[1]
            l.append((j,a))
            j+=1
        self.r=[]
        self.r=l
    
    def permuter(self,a,b):
        j=self.recup(a)
        i=self.recup(b)
        print(i)
        self.r[a-1]=(a,i)
        self.r[b-1]=(b,j)

    #modification d'une reponse
    def modifier(self,num,rep):
        l=[]
        print("modifier")
        print(self.r)
        for i in self.r:
            if(i[0]==num):
                l.append((num,rep))
            else:
                l.append((i[0],i[1]))
        self.r=[]
        self.r=l
        print(self.r)
    #recuperer la reponse a  partir du son num
    def recup(self,num):
        for i in self.r:
            if(i[0]==num):
                a=self.r.index(i)
                return self.r[a][1]
    
    def retourner(self):
        return self.r
    
    def len(self):
        return len(self.r)
    
    def afficher(self):
        s="["
        for i in self.r:
            s+="("+str(i[0])+","+str(i[1])+")"
        s+="]"
        return s

    def egale(self,m):
        self.r=m
        print(self.r)        

        

    

    
    
    
  