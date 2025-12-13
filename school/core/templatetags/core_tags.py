from django import template

register = template.Library()

@register.filter
def get_app_label(obj):
    """
    Returns the app label of a model instance.
    Usage: {{ object|get_app_label }} -> 'academics'
    """
    return obj._meta.app_label

@register.filter
def get_model_name(obj):
    """
    Returns the model name (lowercase) of a model instance.
    Usage: {{ object|get_model_name }} -> 'student'
    """
    return obj._meta.model_name

@register.filter
def get_attribute(obj, attr_name):
    """
    Dynamically accesses an attribute of an object using a string variable.
    Crucial for generic tables where column names are passed as strings.
    
    Usage: {{ object|get_attribute:'first_name' }}
    """
    try:
        # 1. Handle standard attributes (e.g., student.first_name)
        if hasattr(obj, attr_name):
            value = getattr(obj, attr_name)
            
            # 2. Handle 'get_FOO_display' for ChoiceFields (e.g., Gender: M -> Male)
            display_method = f"get_{attr_name}_display"
            if hasattr(obj, display_method):
                return getattr(obj, display_method)()
            
            # 3. Handle methods (if the attribute is a callable/function)
            if callable(value):
                return value()
                
            return value
            
    except Exception:
        return ""
        
    return ""