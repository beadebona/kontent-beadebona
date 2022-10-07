
class ContentSerializer:
    valid_inputs = {
        "title" : str,
        "module": str,
        "students" : int,
        "description": str,
        "is_active": bool,
    }

    def __init__(self, **kwargs):
        self.data = kwargs
        self.errors = {}
    
    def is_valid(self):
        self.cleaner()

        try:
            self.validator()
            return True
        except:
            return False


    def cleaner(self):
        data_keys = set(self.data.keys())
        for key in data_keys:
            if key not in self.valid_inputs.keys():
                self.data.pop(key)


    def validator(self):
        for key, key_type in self.valid_inputs.items():
            if key not in self.data.keys():
                self.errors[key] = "missing key"
            elif type(self.data[key]) is not key_type:
                self.errors[key] = f"must be a {key_type.__name__}"
        
        if self.errors:
            raise KeyError
