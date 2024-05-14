import pytest
from great_expectations_v1.profile.base import Profiler


@pytest.mark.unit
def test_base_class_not_instantiable_due_to_abstract_methods():
    with pytest.raises(TypeError):
        Profiler()
