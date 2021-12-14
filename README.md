# Lookup Server

Portage du lookup-server pour nextcloud

## Installation :

```pip install -r requirements.txt```

## Env :

```export MONGO_URI=mongodb://localhost:3001/meteor``` => The mongo URI to access the database

```export APP_SIGN=salutLaCompagnie``` => The app signature to be recongnize by nextCloud

## Requests :

```/users``` => returns all users

```/users?search=searchstring``` => returns users matching searchstring

```# users?search=searchstring&exact=1``` => returns a single user matching exact searchstring on username

```# users?search=searchstring&exact=1&keys=["email"]``` => returns a single user matching exact searchstring on emails

```# users?search=searchstring&keys=["email"]``` => returns users matching searchstring only on emails field