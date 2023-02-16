#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2023/01/05 19:03:40.041474
#+ Editado:	2023/01/27 20:43:35.754298
# ------------------------------------------------------------------------------
from dataclasses import dataclass, field
# ------------------------------------------------------------------------------
@dataclass
class Sequence:
    """Entity Object"""
    table_name: str = field(init=False, repr=False, default='sqlite_sequence')
    name: str
    seq: int
# ------------------------------------------------------------------------------
