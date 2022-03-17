#Génération du brainfuck 
#Auteur : Lorisredstone 

# Anchor principale 
-

# CODE :
+[-<+]->>>>> # go au début et va sur la case des variables
[-]+++ +[-<+]- # nombre de variables (3)
+[-<+]->>>>> > [-]++++ +[-<+]- # set la variable var1 = 4
+[-<+]->>>>> >> [-]+++ +[-<+]- # set la variable var2 = 3
+[-<+]->>>>> >>> [-] +[-<+]- # set la variable var3 = 0
+[-<+]->>>>> >-[+[-<+]->>++[-<+]->>>>++[-<+]->>>>> >-]+[-<+]->>++[-<+]->>>>+ #dupe and load var1 in ram1 
+[-<+]- >>>>- [ +[-<+]->>>>> >++[-<+]- >>>>-]+[-<+]->>>>> >+ # push back the original value 
+[-<+]->>>>> >>-[+[-<+]->>>++[-<+]->>>>++[-<+]->>>>> >>-]+[-<+]->>>++[-<+]->>>>+ #dupe and load var2 in ram2 
+[-<+]- >>>>- [ +[-<+]->>>>> >>++[-<+]- >>>>-]+[-<+]->>>>> >>+ # push back the original value 
+[-<+]->>>- [+[-<+]->++[-<+]->>>-]+[-<+]->+ # load la value 1 dans l'adder
+[-<+]->>- [+[-<+]->++[-<+]->>-]+[-<+]->+ # load la value 2 dans l'adder 
+[-<+]->-[+[-<+]->>>>> >>>++[-<+]->-]+[-<+]->>>>> >>>+ # store le résultat dans la variable var3
+[-<+]->>>>> >>> ++++++++++++++++++++++++++++++++++++++++++++++++.------------------------------------------------ # print la variable var3 en int
