Set-ExecutionPolicy unrestricted

$env:FLASK_APP = "lexengine"
$env:FLASK_ENV = "development"
flask run