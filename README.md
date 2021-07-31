# Flask_task
Calculates if the sent location is in the MKAD line of Moskov or not. If it's outside it calculates the distance as well.

Send your location's name into as a json object like raw {"address":"sao paulo"} as a POST request 
to see if it's inside the MKAD line or not.
http://localhost:5000/api/api/calculate_distance

If it's inside no distance will be calculated it'll just return it's inside the line.
If it's outside it'll return the distance in kms and say it's outside of the MKAD line

All you need to do is dowload the zip and
run EXPORT FLASK_APP=neuro
run flask run \*(outside of the directory)

