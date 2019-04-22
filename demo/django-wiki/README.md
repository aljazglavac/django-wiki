# Administration pannel wiki plugin

**Wiki operation extension for Django administration site.**

## Overview 

Wiki extension focuses only on Django administrations pannel and has no effect on other parts of your aplication. The concept is based on well known site Wikipedia. Whole point of this extension it is, openinig the database to annonimous users that can contribute their own knowledge and expend aplications database. Extension logic separates users into two groups, site administrators and annonimous users(anno), but other users can be added. Annonimous users can view all entries, but any changes done on them, will result in creation of a new wiki entrie. With this we can keep original database entries intact. All wiki entries are put into review stage. In review stage, any user can further update this entry, but can't create any more wiki instances, out of it. This instances become valid after review from administrator. Admin can accept or reject staged entry.


### Use case

Extension can be very usefull in any sort of tourist aplication, where locals can add their own points of interest.


### Features

* Global annonimous and admin user.
* Every model can have it's separate annonimous and admin user.
* Messaging system is adapted for submiting, reviewing and other operations on models.
* Built in custom model managers for filtering out valid and wiki entries.
* Administrators have a list of current staged objects on index site.
* Each model or app can have it's own administrator and annonimous user.
* Custom admin change site buttons.
* Support for any model entity.


## Requirements

* Python(2.7, 3.6)
* Django(2.2)

## Limitations

For now, this extension can work with three types of models:  
* Basic (model with no foreign keys)
* One foreign key (two models can be in relation by one atribute)
* Inline presentation (stacked)

## Instalation

1. Install "django admin wiki extension":

```
pip install django-admin-wiki-widget
```

2. Add "wiki" to your INSTALLED_APPS in settings like this:

```python
INSTALLED_APPS = [
	...
	'wiki',
]
```


## Basic usage

### Models configuration

**Example for two models (Author and Book)**
* Every model that you want to use wiki extension needs to be derived from `WikiModel`.
* `WikiModel` automatically and `wiki_id` field, that is necessary for wiki operations to work.

**Imports**
```python
from wiki.models import WikiModel
```

**Basic model**
```python
class Author(WikiModel):
    name = models.CharField(max_length=100)
```

**Relation model**
```python
class Book(WikiModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
```


### Admin configuration

**Imports**
* `WikiModelAdmin` extends original html and other presentation, for easier usage.
* Import `WikiInlineModelForm`, if you are planning on using stacked inline presentation of relation model.
```python
from wiki.admin import WikiModelAdmin, WikiInlineModelForm # for inline option
```

**Basic admin**
* To use wiki extension on administration site, eveny admin register class needs to be extended from `WikiModelAdmin`.
```python
@admin.register(Author)
class AuthorAdmin(WikiModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(WikiModelAdmin):
    pass
```

**Inline admin** 
* In stacked inline admin class, form needs to be specified.
```python
class BookInline(admin.StackedInline):
    model = Book
    extra = 0
    form = WikiInlineModelForm


@admin.register(Author)
class AuthorAdmin(WikiModelAdmin):
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(WikiModelAdmin):
    pass
```


### Using custom management command 

Create top level administrator and annonimous user.
```
./manage.py wiki user
```

Display models and which one have admin or anno user.
```
./manage.py wiki list [MODELS]
```

Creates admin or anno users and grous for models.   
```
./manage.py wiki create admin|anno [MODELS]
```
When creating **admin**, super user needs to set password in administration site:
1. Home
2. Authentication and Authorization
3. Users
4. Created user
5. Under password, click 'this form' link


#### Example for models up above

This will create:
* top level admin (username and password: wikiadmin)
* top level annonimous user
* specific anonimous users for author and book models
```
./manage.py wiki user 
./manage.py wiki create anno author book
```

### Using administration site as annonimous user

New endpoits are created:
* **/wiki** -> will automaticlly login main annonimous user
* **/wiki/MODEL** -> will login annonimous user for specified model

**NOTE:** endpoint /wiki/MODEL requires annonimous user to exist.

## Screenshots

## Demo

```
git clone --single-branch --branch demo 
cd ./django-wiki
pipenv install && pipenv shell
cd demo
./manage.py runserver
```

1. Create new wiki entry on /wiki.
2. Logout and login as admin (admin, admin).
3. Accept or reject wiki entry that you have created.
