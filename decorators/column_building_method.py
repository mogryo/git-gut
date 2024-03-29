"""Column building method decorator"""
from enums.columns import CliTableColumn


def column_building_method(column: CliTableColumn):
    """Decorator maker"""
    def decorator(func):
        """Decorator function"""

        def wrapper(*args, **kwargs):
            """Wrapper"""
            func(*args, **kwargs)

        setattr(wrapper, 'builder_column_name', column)
        return wrapper

    return decorator
