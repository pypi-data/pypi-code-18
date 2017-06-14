import pandas as pd
import json
import urllib.request
import urllib.parse
import warnings
from collections import Counter

def pull_json_endpoint(endpoint, parameters):
    url = "%s?%s" % (endpoint, urllib.parse.urlencode(parameters))
    print("Hitting: %r" % url)
    request = urllib.request.urlopen(url)
    t = str(request.read().decode('utf-8'))
    return json.loads(t)

class TimeseriesDatasetMeasurement:
    extracted_fields = ["id", "dataset", "description", "queryBy", "key", "fields", "timepoints"]

    def __init__(self, ctx, dataset_name, descriptor):
        self.ctx = ctx
        self.dataset_name = dataset_name
        self._descriptor = descriptor
        # Extract basic parameters as properties.
        for field in self.extracted_fields:
            setattr(self, field, descriptor[field])

        # The timepoints field is strings of the form "yyyy-mm-dd".
        # This is inconvenient, so we move this over to be _raw, and reformat it.
        self.timepoints_raw = self.timepoints
        self.timepoints = pd.DatetimeIndex(self.timepoints_raw)

    def __repr__(self):
        return "Measurement %s fields=%r queryBy=%r #timepoints=%s" % (self.id, self.fields, self.queryBy, len(self.timepoints))

    def query(self, query_kind, query_value):
        if isinstance(query_value, list):
            query_string = ",".join(map(str, query_value))
        else:
            query_string = str(query_value)
        response = self.ctx.ctx.get("timeseries", self.dataset_name, self.id, "data", parameters={query_kind: query_string})
        column_index = pd.DatetimeIndex(response["timepoints"])
        dataframes = []
        for timeseries in response["timeseries"]:
            query_value = timeseries[self.key] #timeseries[query_kind]
            data = [pd.Series(seq, index=column_index) for seq in timeseries["values"]]
            df = pd.DataFrame.from_items(zip(response["fields"], data))
            df[self.key] = [query_value] * df.shape[0]
            dataframes.append(df)
        final_df = pd.concat(dataframes)
        return final_df

class TimeseriesDataset:
    def __init__(self, ctx, dataset_name, descriptor):
        self.ctx = ctx
        self.dataset_name = dataset_name
        self.descriptor = descriptor
        # List of all measurement IDs available.
        self.measurements = []
        self.measurement_cache = {}
        for entry in descriptor:
            self.measurements.append(entry["id"])
            self.measurement_cache[entry["id"]] = TimeseriesDatasetMeasurement(self.ctx, dataset_name, entry)
        self.get_measurement = self.__getitem__

    def __repr__(self):
        return "Dataset %s measurements=[%s]" % (self.dataset_name, ", ".join(self.measurements))

    def __getitem__(self, measurement_name):
        return self.measurement_cache[measurement_name]

# Each core Dynasty API gets a handler.

class TimeseriesHandler:
    def __init__(self, ctx):
        self.ctx = ctx
        self.datasets = None
        self.cache = {}
        self.get_dataset = self.__getitem__

    def list(self):
        self.datasets = self.ctx.get("timeseries")
        return self.datasets

    def __getitem__(self, dataset_name):
        if dataset_name not in self.cache:
            descriptor = self.ctx.get("timeseries", dataset_name)
            self.cache[dataset_name] = TimeseriesDataset(self, dataset_name, descriptor)
        return self.cache[dataset_name]

class SimpleHierarchyLeaf:
    def __init__(self, ctx, path, known_parameters):
        self.ctx = ctx
        self.path = path
        self.known_parameters = known_parameters

    def __repr__(self):
        return "API:/%s endpoint parameters: %r" % ("/".join(self.path), self.known_parameters)

    def __call__(self, **kwargs):
        if kwargs.keys() - set(self.known_parameters):
            warnings.warn("Accessing API endpoint with parameter that is outside of the known set")
        return self.ctx.get(*self.path, parameters=kwargs)

class SimpleHierarchyNode(SimpleHierarchyLeaf):
    _known_parameters = []

    def __init__(self, ctx, path_so_far, structure):
        self._ctx = ctx
        self._path_so_far = path_so_far
        self._structure = structure

    def __repr__(self):
        return "API:/%s: [%s]" % ("/".join(self._path_so_far), ", ".join(self._structure.keys()))

    def __getattr__(self, key):
        assert isinstance(key, str), "API is to be accessed by strings"
        if key not in self._structure.keys():
            warnings.warn("Accessing API location %r that is outside of the known hierarchy" % (key,))
        new_path = self._path_so_far + [key]
        substructure = self._structure.get(key, {})
        if isinstance(substructure, list):
            return SimpleHierarchyLeaf(self._ctx, new_path, substructure)
        return SimpleHierarchyNode(self._ctx, new_path, substructure)

class CachingBehavior:
    NO_CACHING     = 1
    MEMORY_CACHING = 2
    PICKLE_CACHING = 3

class APIContext:
    base_api_url = "https://api.dynasty.com/"
    geography_hierarchy = {
        "us": {
            "states": [],
            "counties": ["state"],
            "tracts": ["state"],
            "metros": [],
        },
    }
    property_hierarchy = { 
    "properties": [],
    "slates": [],
    }

    def __init__(self, token, caching=CachingBehavior.MEMORY_CACHING):
        self.token = token
        self.caching = caching
        self.api_cache = {}

        # Set our two main API handlers.
        self.timeseries = TimeseriesHandler(self)
        self.geography = SimpleHierarchyNode(self, ["geography"], self.geography_hierarchy)
        self.property = SimpleHierarchyNode(self, ["property"], self.property_hierarchy)

    def get_no_caching(self, *components, parameters={}):
        endpoint = self.base_api_url + "/".join(components)
        # Add our API token into the parameter set.
        parameters["token"] = self.token
        return pull_json_endpoint(endpoint, parameters)

    def get(self, *components, parameters={}):
        # Form a hashable canonicalized key from the request.
        access_key = (tuple(components), tuple(sorted(parameters.items())))
        # Dispatch behavior on caching mode.
        if self.caching == CachingBehavior.NO_CACHING:
            return self.get_no_caching(*components, parameters=parameters)
        elif self.caching in (CachingBehavior.MEMORY_CACHING, CachingBehavior.PICKLE_CACHING):
            if access_key not in self.api_cache:
                if self.caching == CachingBehavior.PICKLE_CACHING:
                    self.api_cache[access_key] = self.get_no_caching(*components, parameters=parameters)
                else:
                    self.api_cache[access_key] = self.get_no_caching(*components, parameters=parameters)
            return self.api_cache[access_key]
        assert False, "Bad caching mode set on APIContext."