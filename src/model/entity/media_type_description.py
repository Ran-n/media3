#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2023/02/19 14:14:24.670867
#+ Editado:	2023/02/19 14:15:16.131282
# ------------------------------------------------------------------------------
from dataclasses import dataclass, field

from src.utils import Config
from src.model.entity import BaseEntity, MediaType
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
@dataclass
class MediaTypeDescription(BaseEntity):
    """Entity Object"""
    table_name: str = field(init=False, repr=False,
                            default=Config().get_table_name('MediaTypeDescription'))
    desc: str
    media_type: MediaType
# ------------------------------------------------------------------------------
