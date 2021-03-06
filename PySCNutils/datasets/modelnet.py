from .retrievaldataset import RetrievalDataset
from .classificationdataset import ClassificationDataset
from . import DATASET_FOLDER
import os
from glob import glob


class ModelNet40(ClassificationDataset, RetrievalDataset):
    name = 'ModelNet40'
    BASEDIR = os.path.join(DATASET_FOLDER, 'ModelNet/ModelNet40/')
    num_of_tests_per_class = {}

    def __init__(self, max_num_of_tests_per_class=20):
        self.search_map_to_class = {}
        self.class_labels = sorted(os.listdir(self.BASEDIR))
        self.class_for_sample = {}
        for _label, _class_name in enumerate(self.class_labels):
            samples = sorted(
                    os.listdir(os.path.join(
                        self.BASEDIR, _class_name, 'test'
                    )))[:max_num_of_tests_per_class]
            self.num_of_tests_per_class[_label] = len(samples)
            for fname in samples:
                self.search_map_to_class[fname] = _label
                self.class_for_sample[fname] = _class_name

        self.search_to_label = self.search_map_to_class.__getitem__
        self.query_to_label = self.search_map_to_class.__getitem__
        self.search_to_file = self.query_to_file

        self.classes = [
            glob(os.path.join(self.BASEDIR, _class_folder, 'train/*.off'))
            for _class_folder in self.class_labels
        ]

    def query_to_file(self, query, **kwargs):
        return os.path.join(self.BASEDIR, self.class_for_sample[query],
                            'test', query)

    def get_all_queries(self):
        return list(self.search_map_to_class.keys())

    def get_search_set_for_query_sample(self, query_sample):
        search_set = list(self.search_map_to_class.keys())
        search_set.remove(query_sample)
        return search_set

    def num_relevant_samples_for_query(self, query):
        return self.num_of_tests_per_class[self.query_to_label(query)] - 1
