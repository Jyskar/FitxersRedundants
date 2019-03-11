#!/bin/bash

rm -f compara
ls -inum $1|cut -d' ' -f1>>compara
ls -inum $2|cut -d' ' -f1>>compara
diff $1 $2 | grep "^>" | wc -l>>compara

exit 0


