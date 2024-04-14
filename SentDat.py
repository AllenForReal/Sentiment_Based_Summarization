import torch
from torch.utils.data import Dataset, DataLoader


class SentimentDataset(Dataset):
    def __init__(self, filepath, tokenizer, max_len, limit=None):
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.data = []

        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                split_line = line.strip().split(' ', 1)
                if len(split_line) == 2:
                    self.data.append((split_line[0], split_line[1]))
                if limit is not None and len(self.data) >= limit:
                    break

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            # Handle slicing directly in the dataset
            return [self[i] for i in range(*idx.indices(len(self)))]
        label, review = self.data[idx]
        label = 0 if label == '__label__1' else 1
        inputs = self.tokenizer.encode_plus(
            review,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_attention_mask=True,
            truncation=True,
            return_tensors='pt'
        )
        input_ids = inputs['input_ids'].squeeze(0)
        attention_mask = inputs['attention_mask'].squeeze(0)
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': torch.tensor(label, dtype=torch.long)
        }
