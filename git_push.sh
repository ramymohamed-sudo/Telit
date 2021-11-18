#!/bin/bash

hostname=$(hostname)
# echo $hostname
# echo "$PWD"

if [ $hostname == 'k8s-virtual-machine' ]
then
echo "This is the analytical server"
git add .;
git commit -m "$(date)";
git push origin master;

else
   echo "This is a Raspberry-PI "
   git pull origin master

fi


# DIR="/home/k8s/minikube/github-scripts/Telit-and-BG96/BG96-final"
# if [ -d "$DIR" ]; then
#   echo "Installing config files in ${DIR}..."
# fi