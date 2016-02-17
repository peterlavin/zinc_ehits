#!/usr/bin/env bash

if [ -z $1 ]
then
  echo $0 directoryName contentDirectory
  exit 1
fi

directoryName=$1
contentDirectory=$2

# list all jars in directoryName
find $directoryName -name '*.jar' > jar.list

# traverse all .jar files to find x.y.z.contentDirectory.w for example
for i in `cat jar.list`; 
do  
  jar tf $i | grep $contentDirectory 

  # only echo jar files name if previous grep is not empty
  if [ $? == "0" ]
  then
    echo "Above files were contained in: $i"
  fi
done
