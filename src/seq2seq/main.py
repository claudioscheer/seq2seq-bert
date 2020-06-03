import os
import logging
import pandas as pd
from lib import Seq2SeqModel


def get_dataset(dataset_path):
    train = []
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_file_path, dataset_path), "r") as file:
        train = file.readlines()
    data = []
    i = 0
    while i < len(train):
        data.append([train[i], train[i + 1]])
        i += 2
    df = pd.DataFrame(data, columns=["input_text", "target_text"])
    return df


logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

train_df = get_dataset("../../dataset/twitter-dev-small/twitter_en.train.txt")

model_args = {
    "fp16": False,
    "overwrite_output_dir": True,
    "max_seq_length": 128,
    "train_batch_size": 8,
    "eval_batch_size": 1,
    "num_train_epochs": 64,
    "max_length": 128,
    "num_beams": 3,
    "early_stopping": False,
    "learning_rate": 1e-4,
    "save_eval_checkpoints": False,
    "save_model_every_epoch": False,
    "save_best_model": False,
}

model = Seq2SeqModel(encoder_type="bert", encoder_name="bert-base-cased", decoder_name="bert-base-cased", args=model_args)
model.train_model(train_df)