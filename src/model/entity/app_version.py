#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2023/02/02 22:59:18.477529
#+ Editado:	2023/02/16 23:34:04.805910
# ------------------------------------------------------------------------------
from dataclasses import dataclass, field
from typing import Optional

from src.utils import Config
from src.model.entity import BaseEntity, App
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
@dataclass
class AppVersion(BaseEntity):
    """AppVersion Entity Object"""
    table_name: str = field(init=False, repr=False,
                            default=Config().get_table_name('AppVersion'))
    app: App
    number: int
    name: Optional[str] = field(default=None)
    active: Optional[int] = field(default=1)
    num_bit_processor: Optional[int] = field(default=None)
    id_: Optional[int] = field(default=None)
    added_ts: Optional[str] = field(default=None)
    modified_ts: Optional[str] = field(default=None)
# ------------------------------------------------------------------------------
