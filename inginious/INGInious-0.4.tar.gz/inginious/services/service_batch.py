# coding=utf-8
from abc import abstractmethod, ABCMeta

from inginious.services.service import Service


class BatchService(Service, metaclass=ABCMeta):
    @abstractmethod
    def get_batch_containers_metadata(self):
        """
            Returns the arguments needed by a particular batch container (cached version)
            :returns: a dict of dict in the form
                {
                    "container title": {
                        "container description in restructuredtext",
                        {
                            "key":
                            {
                                "type:" "file", #or "text",
                                "path": "path/to/file/inside/input/dir", #not mandatory in file, by default "key"
                                "name": "name of the field", #not mandatory in file, default "key"
                                "description": "a short description of what this field is used for", #not mandatory, default ""
                                "custom_key1": "custom_value1",
                                ...
                            }
                        }
                    }
                }
        """
        pass

    @abstractmethod
    def new_batch_job(self, container_name, inputdata, callback, launcher_name="Unknown"):
        """ Add a new batch job. callback is a function that will be called asynchronously in the client's process.
            inputdata is a dict containing all the keys of get_batch_containers_metadata()[container_name]["parameters"].
            The values associated are file-like objects for "file" types and  strings for "text" types.
        """
        pass
