#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2023/01/11 22:41:49.401227
#+ Editado:	2023/02/10 17:48:55.923742
# ------------------------------------------------------------------------------
#* Strategy Interface (Strategy Pattern)
# ------------------------------------------------------------------------------
from abc import ABC, abstractmethod
# ------------------------------------------------------------------------------
from src.model.entity import Media, MediaGroup, MediaIssue
from src.model.entity import MediaType, MediaStatus
# ------------------------------------------------------------------------------
class iView(ABC):
    @abstractmethod
    def menu(self) -> None:
        pass

    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass

    @abstractmethod
    def add_media_type(self) -> MediaType:
        pass

    @abstractmethod
    def add_media_status(self) -> MediaStatus:
        pass

    @abstractmethod
    def add_media(self) -> Media:
        pass

    @abstractmethod
    def add_media_group(self, id_media: int = None) -> MediaGroup:
        pass

    @abstractmethod
    def add_media_issue(self) -> MediaIssue:
        pass
# ------------------------------------------------------------------------------

