import pandas as pd
import os

# Datasets loads in all the files from the ../assets folder and loads them on demand into pandas dataframes
class datasets(object):
    def __init__(self, logger):
        logger.info("Loading in data")
        self._datasets = {}
        for file in os.listdir("assets"):
            # TODO lazy load if necessary for performance
            self._datasets[file.split(".")[0]] = pd.read_csv(os.path.join("assets", file))
        self.logger = logger
        self._intalize()
        self._dataset = None
    
    # After loading in the data on create, we clean the data by dropping all empty rows and assigning integer values to each variable
    def _intalize(self):
        self.logger.info("Cleaning data")
        for value in self._datasets.values():
            self._dataset = value
            self._cleanData()
    
    def _cleanData(self):
        # Drop all empty rows
        self._dataset.dropna(subset=self._dataset.columns, inplace=True)

        for col in self._dataset:
            if not isinstance(self._dataset[col][0], float):
                variables = set(self._dataset[col])
                changeVar = {}

                for index, var in enumerate(variables, 1):
                    changeVar[var] = index

                self._dataset = self._dataset.reset_index()
                for val in range(len(self._dataset[col])):
                    self._dataset.loc[val, col] = changeVar[self._dataset[col][val]]

    @property
    def dataset(self):
        return self._dataset

    # Takes a name and uses the name to get the dataset from the dictionary
    @dataset.setter
    def dataset(self, name: str):
        if name not in self._datasets:
            raise ValueError(f"Dataset {name} not found")
        self._dataset = self._datasets[name]
    
    def get_dataset_names(self) -> list[str]:
        return list(self._datasets.keys())
