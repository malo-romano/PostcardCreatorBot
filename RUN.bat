@ECHO OFF

SET scriptname=%~d0%~p0appdata
ECHO "%scriptname%"

docker build -t pccb .
docker run -t -d --name PostCardCreatorBot -v %scriptname%:/usr/pccb/appdata pccb

echo Done. Container is now running in docker.

PAUSE