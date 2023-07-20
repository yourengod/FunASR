import os

from modelscope.metainfo import Trainers
from modelscope.trainers import build_trainer

from funasr.datasets.ms_dataset import MsDataset
from funasr.utils.modelscope_param import modelscope_args


def modelscope_finetune(params):
    if not os.path.exists(params.output_dir):
        os.makedirs(params.output_dir, exist_ok=True)
    # dataset split ["train", "validation"]
    ds_dict = MsDataset.load(params.data_path)
    kwargs = dict(
        model=params.model,
        data_dir=ds_dict,
        dataset_type=params.dataset_type,
        work_dir=params.output_dir,
        batch_bins=params.batch_bins,
        max_epoch=params.max_epoch,
        lr=params.lr,
        mate_params=params.param_dict)
    trainer = build_trainer(Trainers.speech_asr_trainer, default_args=kwargs)
    trainer.train()


if __name__ == '__main__':
    params = modelscope_args(model="damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch", data_path="./data")
    params.output_dir = "./checkpoint"              # m模型保存路径
    params.data_path = "./example_data/"            # 数据路径
    params.dataset_type = "small"                   # 小数据量设置small，若数据量大于1000小时，请使用large
    params.batch_bins = 2000                       # batch size，如果dataset_type="small"，batch_bins单位为fbank特征帧数，如果dataset_type="large"，batch_bins单位为毫秒，
    params.max_epoch = 5                           # 最大训练轮数
    params.lr = 0.00005                             # 设置学习率
    init_param = []
    freeze_param = []
    ignore_init_mismatch = True
    use_lora = False
    params.param_dict = {"init_param":init_param, "freeze_param": freeze_param, "ignore_init_mismatch": ignore_init_mismatch}
    if use_lora:
        enable_lora = True
        lora_bias = "all"
        lora_params = {"lora_list":['q','v'], "lora_rank":8, "lora_alpha":16, "lora_dropout":0.1}
        lora_config = {"enable_lora": enable_lora, "lora_bias": lora_bias, "lora_params": lora_params}
        params.param_dict.update(lora_config)
    
    modelscope_finetune(params)
