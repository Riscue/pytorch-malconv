import numpy as np
from torch.utils.data import Dataset


class ExeDataset(Dataset):
    def __init__(self, fp_list, data_path, label_list, first_n_byte=2000000):
        self.fp_list = fp_list
        self.data_path = data_path
        self.label_list = label_list
        self.first_n_byte = first_n_byte

    def __len__(self):
        return len(self.fp_list)

    def __getitem__(self, idx):
        with open(self.data_path + self.fp_list[idx], 'rb') as f:
            tmp = [i + 1 for i in f.read()[:self.first_n_byte]]
            tmp = tmp + [0] * (self.first_n_byte - len(tmp))

        return np.array(tmp), np.array([self.label_list[idx]]).astype(float)
