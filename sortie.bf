#Génération du brainfuck 
#Auteur : Lorisredstone 

# Anchor principale 
-
# Anchor des variables
>>>>>>>-- +[-<+]-

+[-<+]-++[-->++]-->>>---+[-<+]-
+[-<+]-++[-->++]--> # go au début et va sur la case des variables
[-]+ +[-<+]- # nombre de variables (1)
+[-<+]-+++[--->+++]---> # go au début et va sur la case des strings
[-]+ +[-<+]- # nombre de strings (1)

# CODE :
# stocke 
+[-<+]-+++[--->+++]--->> # va au bon endroit
+> #push la len

 : +++++++++++[-<+]- #retourne au début 

+[-<+]-++[-->++]--> > [-]+ +[-<+]- # set la variable c = 1
