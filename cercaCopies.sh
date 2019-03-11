#!/bin/bash
#CERCACOPIES.sh
#DESCRIPCIÓ: busca copies per el arbre de fitxers donats dos paths
#PARAMETRES:reb dos paths, el primer es el path origen i el segon el desti.

#comprovem que s'hagi escollit un directori destí
if [ $2 == "Escull" ]
then
	exit 1
fi

rm -f f1     #borrem contingut del fitxer intermig
rm -f semblants     #borrem contingut del fitxer intermig
rm -f iguals     #borrem contingut del fitxer intermig
rm -f originals
for file in $(ls -F $1)
do
	find $2 -name $file -type f >>f1    #busca i guarda el path de fitxers amb nom $file
done
for line in $(cat f1)
do
	filename=$(echo -n $line| rev | cut -d '/' -f1 |rev )	#nomFitxer
	echo $1/$filename>>originals			
	originalPath=$1/$filename
	val1=$(cat $originalPath)
	val2=$(cat $line)
	#evitem elements de la paperera
	if [ "$line" != "/home/milax/.local/share/Trash/files/$filename" ]
	then
	#evitem que els paths siguin el mateix 
	if [   "$originalPath" != "$line" ]
	then
		if [ "$val1" == "$val2" ]
		then
			echo $line>>iguals
		else
			echo $line>>semblants
		fi
	fi
	fi
done
exit 0
