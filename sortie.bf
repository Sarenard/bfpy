#Génération du brainfuck 
#Auteur : Lorisredstone 

# Anchor principale 
-
# Anchor des variables
>>>>>>-- +[-<+]-

+[-<+]-++[-->++]-->>>>>---+[-<+]-
+[-<+]-++[-->++]--> # go au début et va sur la case des variables
[-]+++ +[-<+]- # nombre de variables (3)
+[-<+]-+++[--->+++]---> # go au début et va sur la case des strings
[-]+ +[-<+]- # nombre de strings (1)

# CODE :
# stocke 
+[-<+]-+++[--->+++]--->> # va au bon endroit
+> #push la len

 : +++++++++++[-<+]- #retourne au début 

+[-<+]-++[-->++]--> > [-]++++++ +[-<+]- # set la variable a = 6
+[-<+]-++[-->++]--> >> [-]++++++ +[-<+]- # set la variable b = 6
+[-<+]-++[-->++]--> >>> [-] +[-<+]- # set la variable c = 0
+[-<+]-++[-->++]--> >>-[+[-<+]->>++[-<+]->>>>++[-<+]-++[-->++]--> >>-]+[-<+]->>++[-<+]->>>>+ #dupe and load b in ram1 
+[-<+]- >>>>- [ +[-<+]-++[-->++]--> >>++[-<+]- >>>>-]+[-<+]-++[-->++]--> >>+ # push back the original value 
+[-<+]-++[-->++]--> >-[+[-<+]->>>++[-<+]->>>>++[-<+]-++[-->++]--> >-]+[-<+]->>>++[-<+]->>>>+ #dupe and load a in ram2 
+[-<+]- >>>>- [ +[-<+]-++[-->++]--> >++[-<+]- >>>>-]+[-<+]-++[-->++]--> >+ # push back the original value 
+[-<+]- >> >>[-]>[-] <<<[>>>+<<<-]+ >[>>-<+<-] >[<+>-] >[<<<->>>[-]] << [-] < [-<+>] +[-<+]->  [-[+[-<+]-++[-->++]--> >>>++[-<+]->-]+[-<+]-++[-->++]--> >>>++[-<+]->[-]] # store le résultat dans la variable c
+[-<+]-++[-->++]--> >>> ++++++++++++++++++++++++++++++++++++++++++++++++.------------------------------------------------ # print la variable c en int
