#!/bin/bash
#This script checks the if theres a hard link to a file or not
#Primer parametre a de ser el fitxer el cual volem comprovar
if [ $# -ne 2 ] || [ $1 == "-h" ] || [ $1 == "-help" ] 
then
	echo "Ús: checkHardlink.sh"
	echo "Printa el numero d'inode i el path relatiu dels fitxers que apunten a el mateix inode"
	echo "PARAMETRES:"
	echo "1: path al fitxer que es vol comprovar"
	echo "2: path al directori al qual es vol buscar els hard links"
	echo "Codi retorn:"
	echo " 0 si tot OK"

exit 1
fi
x=$(ls -i $1 | cut -d ' ' -f1)
echo Numero Inode $x
echo Path relatiu als fitxers que apunten al mateix inode:
find $2 -inum $x

exit 0
