from abc import abstractmethod

import yaml

class ConfigItemBase:
    def __init__(
            self,
            tybe: type,
            key: str,
            required: bool = False,
            prompt: str = None,
            allow_from_user_input: bool = False):
        self.__type = tybe
        self.key = key
        self._value = None
        self.prompt = prompt
        self._required = required
        self.allow_from_user_input = allow_from_user_input

    def from_value(self, value):
        assert type(value) == self.__type, 'Config data type does not match'
        self._value = value

    def from_user_input(self):
        self._value = self.__type(input(self.prompt))

    def get_type(self):
        return self.__type

    def value(self):
        if self._value is None and self.allow_from_user_input:
            self.from_user_input()
        return self._value

    def required(self):
        return self._required

class ConfigItem(ConfigItemBase):
    def __init__(
            self,
            tybe: type,
            key: str,
            allow_from_user_input: bool = True,
            default_value = None,
            prompt: str = None):
        super().__init__(tybe, key, default_value is None and allow_from_user_input, prompt)
        self._value = default_value

class ConfigModule(ConfigItemBase):
    def __init__(self, key: str, allow_from_user_input: bool = True):
        super().__init__(dict, key, allow_from_user_input=allow_from_user_input)
        self.__children = dict()

    def from_dict(self, data: dict):
        for k, v in self.__children.items():
            assert v.required() or k in data, 'Required field of config not specified: {}'.format(k)
            v.from_value(data[k])

    def from_value(self, value):
        self.from_dict(value)
        pass

    def from_user_input(self):
        for k, v in self.__children.items():
            v.from_user_input()

    def register_item(self, key: str, item: ConfigItem = None, **kwargs):
        assert key not in self.__children, "Item is already registered"
        self.__children[key] = item or ConfigItem(key=key, **kwargs)

    def register_module(self, key: str, module: 'ConfigModule' = None, **kwargs) -> 'ConfigModule':
        assert key not in self.__children, "Module is already registered"
        module = module or ConfigModule(key, allow_from_user_input=self.allow_from_user_input, **kwargs)
        self.__children[key] = module
        return module

    def item_path(self, path: list[str]) -> ConfigItemBase:
        n = self.__children[path[0]]
        if len(path) > 1:
            assert isinstance(n, ConfigModule)
            return n.item_path(path[1:])
        else:
            return n

    def item(self, key: str) -> ConfigItemBase:
        path = key.split('.')
        return self.item_path(path)

class Config:
    __modules = dict()

    def __init__(self):
        pass

    def register_module(self, key: str, required: bool = False, module: ConfigModule = None, **kwargs) -> ConfigModule:
        assert key not in self.__modules, "Module is already registered"
        module = module or ConfigModule(key, **kwargs)
        self.__modules[key] = (module, required)
        return module

    def read_from_file(self, filename: str):
        with open(filename, 'r') as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.SafeLoader)
        for key, module_tuple in self.__modules.items():
            assert module_tuple[1] or key in yaml_data, 'Required module {} not registered'.format(key)
            data = yaml_data[key]
            assert type(data) is dict, 'Module config need to be a dict for {}'.format(key)
            module = module_tuple[0]
            module.from_dict(data)

    def module(self, key: str) -> ConfigModule:
        return self.__modules[key][1]

