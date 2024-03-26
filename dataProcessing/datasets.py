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
            self.dataset = value
            self._cleanData()
    
    def _cleanData(self):
        # Drop all empty rows
        self.dataset.dropna(subset=self.dataset.columns, inplace=True)

        for col in self.dataset:
            if not isinstance(self.dataset[col][0], float):
                variables = set(self.dataset[col])
                changeVar = {}

                for index, var in enumerate(variables, 1):
                    changeVar[var] = index

                self.dataset = self.dataset.reset_index()
                for val in range(len(self.dataset[col])):
                    self.dataset.loc[val, col] = changeVar[self.dataset[col][val]]

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        self._dataset = dataset
    
    def get_dataset_names(self):
        return list(self._datasets.keys())
