[//]: # ( -*- coding: utf-8 -*- )
[//]: # ( ---------------------------------------------------------------------- )
[//]: # (+ Autor:  	Ran# )
[//]: # (+ Creado: 	2023/01/04 21:56:10.000000 )
[//]: # (+ Editado:	2023/02/24 19:22:19.250077 )
[//]: # ( ---------------------------------------------------------------------- )

# media4
Manager for your own personal media library.\
Allows you to automatically add useful information about media files to a database and lets you manage your library and access information and stats regarding it.


## Index
- [Documentation](media/doc/index.md#documentation)
- [How to Start](#how-to-start)
- [Frequent Stuff](#frequent-stuff)
- [Code Features](#code-features)
- [Tasks](#tasks)
- [TODO](#todo)


## How to Start
1. You may copy the config.cnf file into a .cnf file and configure the options to your liking (if not, default config will be used).
2. Run the program executing the following:
    ```
    $ ./main.py
    ```

## Frequent Stuff
Information about common useful things

### About the .cnf file
If you comment any, the default (as shown) value will still be used.
You can not leave the right part of the parameter definition in blank, you either put something or delete it entirely.

## Code features
- Logging
- Configuration file

## Tasks
- [ ] Add the active flag to all i18n primary tables.
- [ ] Make a simplified version of the diagrams
- [ ] Make Add Function for WarehouseType
- [ ] Make Add Function for Warehouse
- [ ] Make Add Function for ShareSiteType
- [ ] Make Add Function for ShareSite
- [ ] Make Make Telegram service
- [ ] Automatically use the Telegram service for updating the subs of sharesite depending on platform (use thread)
- [ ] Make MediaIssue not always have MediaGroup.

## TODO
- [ ] Make "info.py" a service.
- [ ] Make the CustomTKinter GUI.
- [ ] Remake the insert media option and add other options.
- [ ] Migrate the app language everywhere in the code into english.
- [ ] Allow inserting dates before year 0.
- [ ] Check if a date of an issue is in between the appropiate years according to its group/media
- [ ] Automatically update the subs of the Telegram ShareSites.
- [ ] Dont only show name on groups since it can be null and number is more important anyways.
- [ ] Make less confusing what part of input you are in when a subinput is opened (insert media group of newly created media)
- [ ] Add authors (this is tricky because it would also imply, if done correctly, to add attributions).
