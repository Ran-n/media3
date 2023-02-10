#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2023/01/11 22:41:57.231414
#+ Editado:	2023/02/10 17:48:20.778116
# ------------------------------------------------------------------------------
#* Concrete Strategy (Strategy Pattern)
# ------------------------------------------------------------------------------
from src.view import iView
# ------------------------------------------------------------------------------
import logging
from typing import List, Union, Callable

from src.enum import PaginationEnum
from src.utils import Config

from src.model.entity import Media, MediaGroup, MediaIssue
from src.model.entity import MediaType, MediaStatus
# ------------------------------------------------------------------------------
class Terminal(iView):
    def __init__(self) -> None:
        logging.info(_('Starting Terminal view'))

        self.model = None
        self.controller = None

        print('----------------------------------------')
        print(_('Media4 Manager'))
        print('----------------------------------------')

    def menu(self, options: dict) -> int:
        print()
        print('*** '+_('MENU')+' ***')

        for key, value in zip(options.keys(), options.values()):
            print(f'{key}  {value[0]}')

        while True:
            option = input(_('Pick: '))
            if option in options:
                break

        print('*** '+_('MENU')+' ***')
        print()

        return option

    def save(self) -> None:
        print('* ' + _('The Database was saved') + ' *')

    def exit(self) -> None:
        print('----------------------------------------')

    def __pick_from_options(self, message: dict[str, str], option_count: int, add_fn: Callable, get_opts_fn: Callable, limit: int = None, offset: int = 0) -> Union[MediaType, MediaStatus, Media]:
        """
            message
            {'title': 'a', 'pick': 'b', 'empty': 'c'}
        """

        # if not option exists, it starts the add option function
        while option_count == 0:
            logging.warning(message['empty'])
            print(f'!! {message["empty"]}')
            add_fn()
            option_count += 1
            print()

        # this variable allows the print to be smart and only reprint
        # and reask for the options if anyting was changed
        load_options = True
        # loop choice of option
        while True:
            if load_options:
                load_options = False

                lst_option = get_opts_fn(limit= limit, offset= offset)

                title = f'< {message["title"]}'
                if limit:
                    title += f' {len(lst_option) + offset}/{option_count}'
                print(title)

                for index, ele in enumerate(lst_option):
                    print(f'{index + offset + 1}. {ele.name}')
            choice = input(f'> {message["pick"]}: ')

            # add new element
            if choice == '+':
                print()
                add_fn()
                option_count += 1
                load_options = True
            # move in pagination (limit = None | 0 will be false)
            elif limit and (choice in PaginationEnum.OPTIONS.value):
                choice_enum = PaginationEnum(choice)
                if (choice_enum == PaginationEnum.NEXT) and (option_count > offset + limit):
                    offset += limit
                    load_options = True
                elif (choice_enum == PaginationEnum.PREVIOUS) and (offset != 0):
                    offset -= limit
                    load_options = True
            # user selected something in the list
            elif choice.isdigit():
                choice = int(choice)
                if (choice > 0 and choice <= (len(lst_option) + offset)):
                    value = lst_option[choice - offset - 1]
                    break
        return value

    @staticmethod
    def __yn_question(message: str, as_str: bool = False) -> [str, int]:
        no_opts = ['n', 'no', 'non']
        str_answer = {0: _('No'), 1: _('Yes')}

        user_input = input(f'> {message}'+_(' [Y/n]')+': ')

        answer = 1  # yes by default
        if user_input.lower() in no_opts: answer = 0

        if as_str: return str_answer[answer]
        return answer

    @staticmethod
    def __pick_number(message: str, nullable: bool = False, equal_to: int = None, compare_msg: List[dict[str, str, str]] = None) -> int:
        """
        Questions the user to pick a number, the number selected can be within a set a defined constraints.

        @ Input:
        ╠═  * message    -   str
        ║   └ What will the user see to indicate what to insert.
        ╠═  · equal_to    -   str
        ║   └ What number will be used in case the user inputs the equal sign in the number picked.
        ╚═  · compare_msg -   List[dict[str, str, str]]
            └ Example: [{'number'= '14', 'symbol'= '>', 'message'= 'The number must be bigger than 14'}].
              The first part will be evaluated, and if failed will show the second one to the user.

        @ Output:
        ╚═  int -   The picked number by the user.
        """

        while True:
            exit = False
            number = input(f'> {message}: ')
            if nullable and number == '':
                number = None
                break
            elif number.isdigit():
                for ele in compare_msg:
                    if ele['number'] != None:
                        if eval(number + ele['symbol'] + ele['number']):
                            exit = True
                        else:
                            exit = False
                            print('!! '+ele['message'])
                            break

                if exit:
                    break
            elif equal_to and number == '=':
                number = equal_to
                break
        return number


    def add_media_type(self) -> MediaType:
        logging.info(_('Requesting the user for the information on the media type'))
        print('** '+_('Add Media Type')+' **')

        while True:
            name = input('> '+_('Name')+': ')
            if name != '':
                if len(self.model.get_by_name(MediaType.table_name, name)) == 0:
                    break
                print('!! '+_('The given name is already in use'))

        groupable = self.__yn_question(_('Groupable?'))

        print('** '+_('Add Media Type')+' **')

        return MediaType(name = name, groupable = groupable)

    def add_media_status(self) -> MediaStatus:
        logging.info(_('Requesting the user for the information on the media status'))
        print('** '+_('Add Media Status')+' **')

        while True:
            name = input('> '+_('Name')+': ')
            if name != '':
                if len(self.model.get_by_name(MediaStatus.table_name, name)) == 0:
                    break
                print('!! '+_('The given name is already in use'))

        print('** '+_('Add Media Status')+' **')

        return MediaStatus(name= name)

    def add_media(self) -> Media:
        logging.info(_('Requesting the user for the information on the media'))

        print('** '+_('Add Media')+' **')
        # name
        while True:
            name = input('> '+_('Name')+': ')
            if name != '':
                break
        print()

        # type_
        type_ = self.__pick_from_options(
                message     =   {
                    'title':    _('Types'),
                    'pick':     _('Type'),
                    'empty':    _('There are no media types available')
                },
                option_count    =   self.model.get_num(table_name= MediaType.table_name),
                add_fn          =   self.controller.add_media_type,
                get_opts_fn     =   lambda limit, offset: self.model.get_all(table_name= MediaType.table_name, limit= limit, offset= offset),
                limit           =   Config().pagination_limit
        )
        print()

        # status
        status = self.__pick_from_options(
                message     =   {
                    'title':    _('Statuses'),
                    'pick':     _('Status'),
                    'empty':    _('There are no media statuses available')
                },
                option_count    =   self.model.get_num(table_name= MediaStatus.table_name),
                add_fn          =   self.controller.add_media_status,
                get_opts_fn     =   lambda limit, offset: self.model.get_all(table_name= MediaStatus.table_name, limit= limit, offset= offset),
                limit           =   Config().pagination_limit
        )
        print()

        # year_start
        year_start = self.__pick_number(
                message     =   _('Start Year'),
                nullable    =   True,
                compare_msg =   [
                    {'symbol': '>=', 'number': '0', 'message': _('The start year must be equal or bigger than 0')}
                ]
        )
        print()

        # year_end
        year_end = self.__pick_number(
                message     =   _('End Year'),
                nullable    =   True,
                equal_to    =   year_start,
                compare_msg =   [
                    {'symbol': '>=', 'number': '0', 'message': _('The year end year must be equal or bigger than 0')},
                    {'symbol': '>=', 'number': f'{year_start}', 'message': _(f'The end year must be equal or bigger than the start one ({year_start})')}
                ]
        )
        print('** '+_('Add Media')+' **')

        return Media(
                name        =   name,
                type_       =   type_,
                status      =   status,
                year_start  =   year_start,
                year_end    =   year_end
        )

    def add_media_group(self, id_media: int) -> MediaGroup:
        logging.info(_('Requesting the user for the information on the media group'))
        print('** '+_('Add Media Group')+' **')

        # media
        if id_media == None:
            media = self.__pick_from_options(
                    message     =   {
                        'title':    _('Medias'),
                        'pick':     _('Media'),
                        'empty':    _('There are no medias available')
                    },
                    option_count    =   self.model.get_num(table_name= Media.table_name),
                    add_fn          =   self.controller.add_media,
                    get_opts_fn     =   lambda limit, offset: self.model.get_all(table_name= Media.table_name, limit= limit, offset= offset),
                    limit           =   Config().pagination_limit
            )
        else:
            media = self.model.get_by_id(table_name= Media.table_name, id_= id_media)
        print()

        # number
        while True:
            number = self.__pick_number(
                    message     =   _('Group Number'),
                    compare_msg =   [
                        {'symbol': '>=', 'number': '0', 'message': 'The group number must be bigger than 0'}
                    ]
            )

            if not self.model.exists(MediaGroup(media= media, number= number)):
                break
            else:
                logging.info(_('The requested media group to be added already exists, a number change will be adviced'))
                print('!! '+_('The Media Group already exists, pick another number.'))
        print()

        # name
        name = input('> '+_('Name')+': ')
        if name == '':
            name = None
        print()

        # year_start
        year_start = self.__pick_number(
                message     =   _('Start year'),
                nullable    =   True,
                compare_msg =   [
                    {'symbol': '>=', 'number': '0', 'message': _('The start year must be equal or bigger than 0')},
                    {'symbol': '>=', 'number': f'{media.year_start}', 'message': _(f'The start year must be equal or bigger than the start year of its Media ({media.year_start})')},
                    {'symbol': '<=', 'number': f'{media.year_end}', 'message': _(f'The start year must be equal or smaller than the end year of its Media ({media.year_end})')},
                ]
        )
        print()

        # year_end
        year_end = self.__pick_number(
                message     =   _('End year'),
                nullable    =   True,
                equal_to    =   year_start,
                compare_msg =   [
                    {'symbol': '>=', 'number': '0', 'message': _('The end year must be equal or bigger than 0')},
                    {'symbol': '>=', 'number': f'{year_start}', 'message': _(f'The end year must be equal or bigger than the start one ({year_start})')},
                    {'symbol': '<=', 'number': f'{media.year_end}', 'message': _(f'The end year must be equal or smaller than the end year of its Media ({media.year_end})')},
                    {'symbol': '>=', 'number': f'{year_start}', 'message': _(f'The end year must be equal or bigger than the start year ({year_start})')}
                ]
        )

        print('** '+_('Add Media Group')+' **')

        return MediaGroup(
                media       =   media,
                number      =   number,
                name        =   name,
                year_start  =   year_start,
                year_end    =   year_end
        )

    def add_media_issue(self) -> MediaIssue:
        """
        """

        logging.info(_('Requesting the user for the information on the media issue'))
        print('** '+_('Add Media Issue')+' **')

        # media
        media = self.__pick_from_options(
                message     =   {
                    'title':    _('Medias'),
                    'pick':     _('Media'),
                    'empty':    _('There are no medias available')
                },
                option_count    =   self.model.get_num(table_name= Media.table_name),
                add_fn          =   self.controller.add_media,
                get_opts_fn     =   lambda limit, offset: self.model.get_all(table_name= Media.table_name, limit= limit, offset= offset),
                limit           =   Config().pagination_limit
        )
        print()

        # media group
        media_group = self.__pick_from_options(
                message         =   {
                    'title':    _('Media Groups'),
                    'pick':     _('Media'),
                    'empty':    _('There are no media groups available')
                },
                option_count    =   self.model.get_media_group_num_by_media_id(media_id= media.id_),
                add_fn          =   lambda: self.controller.add_media_group(id_media= media.id_),
                get_opts_fn     =   lambda limit, offset: self.model.get_media_group_by_media_id(id_= media.id_, limit= limit, offset= offset),
                limit           =   Config().pagination_limit
        )
        print()


        # position
        while True:
            position = self.__pick_number(
                    message     =   _('Issue Number within the Group'),
                    compare_msg =   [
                        {'symbol': '>=', 'number': '0', 'message': 'The issue number must be bigger than 0'}
                    ]
            )

            if not self.model.exists(MediaIssue(media= media, media_group= media_group, position= position)):
                break
            else:
                logging.info(_('The requested media issue to be added already exists, a number change will be adviced'))
                print('!! '+_('The Media Issue already exists, pick another number.'))
        print()

        # name
        name = input('> '+_('Name')+': ')
        if name == '':
            name = None
        print()


        # date
        date = input('> '+_('Date')+': ')
        print()

        print('** '+_('Add Media Issue')+' **')

        return MediaIssue(
                position    =   position,
                media       =   media,
                media_group =   media_group,
                name        =   name,
                date        =   date
        )

# ------------------------------------------------------------------------------
