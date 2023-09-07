"""
POC for dynamically bootstrapping context.sources with Datasource factory methods.
"""
from __future__ import annotations

import logging
from pprint import pformat as pf
from typing import TYPE_CHECKING, Set, Type

from great_expectations.compatibility.pydantic import ModelMetaclass
from great_expectations.experimental.datasources.sources import _SourceFactories

if TYPE_CHECKING:
    from great_expectations.experimental.datasources.interfaces import Datasource


logger = logging.getLogger(__name__)


class MetaDatasource(ModelMetaclass):

    __cls_set: Set[Type] = set()

    def __new__(
        meta_cls: Type[MetaDatasource], cls_name: str, bases: tuple[type], cls_dict
    ) -> MetaDatasource:
        """
        MetaDatasource hook that runs when a new `Datasource` is defined.
        This methods binds a factory method for the defined `Datasource` to `_SourceFactories` class which becomes
        available as part of the `DataContext`.

        Also binds asset adding methods according to the declared `asset_types`.
        """
        logger.debug(f"1a. {meta_cls.__name__}.__new__() for `{cls_name}`")

        cls = super().__new__(meta_cls, cls_name, bases, cls_dict)

        if cls_name == "Datasource" or cls_name.startswith("_"):
            # NOTE: the above check is brittle and must be kept in-line with the Datasource.__name__
            logger.debug(f"1c. Skip factory registration of base `{cls_name}`")
            return cls

        logger.debug(f"  {cls_name} __dict__ ->\n{pf(cls.__dict__, depth=3)}")

        meta_cls.__cls_set.add(cls)
        logger.debug(f"Datasources: {len(meta_cls.__cls_set)}")

        def _datasource_factory(name: str, **kwargs) -> Datasource:
            # TODO: update signature to match Datasource __init__ (ex update __signature__)
            logger.debug(f"5. Adding '{name}' {cls_name}")
            datasource = cls(name=name, **kwargs)
            datasource.test_connection()
            return datasource

        _datasource_factory.__doc__ = cls.__doc__

        # TODO: generate schemas from `cls` if needed

        if cls.__module__ == "__main__":
            logger.warning(
                f"Datasource `{cls_name}` should not be defined as part of __main__ this may cause typing lookup collisions"
            )
        _SourceFactories.register_types_and_ds_factory(cls, _datasource_factory)

        return cls
