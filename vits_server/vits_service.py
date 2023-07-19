import copy
import sys
import time
import soundfile
import os
import torch
import logging
import json
import vits_server.vits.commons as commons
import vits_server.vits.utils as utils
from vits_server.vits.models import SynthesizerTrn
from vits_server.vits.text.symbols import symbols
from vits_server.vits.text import text_to_sequence
from pydub import AudioSegment
from vits_server.utils.time import current_timestamp
from shortuuid import uuid

os.environ["PYTORCH_JIT"] = "0"
sys.path.append('vits_server/vits')

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm


class VitsService:
    def __init__(self, config):
        self.all_model_description = {}
        self.model = config.get("model")
        self.speed = config.get("speed", 1)
        self.output = config.get("output", "./output")
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        self.model_folder = config.get("model_folder", "models")
        self.get_model_description()
        model_map = self.all_model_description.get("modelMap", {})
        if self.model not in model_map:
            raise Exception(f"model:{self.model} does not Exist")
        self.hps = utils.get_hparams_from_file(self.model_config_path)
        self.net_g = SynthesizerTrn(
            len(symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            **self.hps.model).cuda()
        _ = self.net_g.eval()
        _ = utils.load_checkpoint(self.model_path, self.net_g, None)

    @property
    def model_path(self):
        model_map = self.all_model_description.get("modelMap", {})
        cfg = model_map[self.model]
        return os.path.join(self.model_folder, cfg.get("modelPath"))

    @property
    def model_config_path(self):
        model_map = self.all_model_description.get("modelMap", {})
        cfg = model_map[self.model]
        return os.path.join(self.model_folder, cfg.get("modelConfigPath"))

    @property
    def model_list(self):
        model_map = self.all_model_description.get("modelMap", {})
        res = []
        for key in model_map.keys():
            item = copy.deepcopy(model_map[key])
            item["name"] = key
            res.append(item)
        return {"list": res}

    def get_model_description(self):
        config_path = os.path.join(self.model_folder, "model_description")
        with open(config_path, encoding="utf-8") as f:
            config_str = f.read()
            self.all_model_description = json.loads(config_str)

    def read(self, text):
        text = text.replace('~', '！')
        stn_tst = get_text(text, self.hps)
        with torch.no_grad():
            x_tst = stn_tst.cuda().unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
            audio = \
                self.net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.2, length_scale=self.speed)[0][
                    0, 0].data.cpu().float().numpy()
        return audio

    def read_save(self, text, filename, sr=44100):
        stime = time.time()
        au = self.read(text)
        file_path = os.path.join(self.output, filename + ".wav")
        soundfile.write(file_path, au, sr)
        logging.info('VITS Synth Done, time used %.2f' % (time.time() - stime))
        return file_path

    def read_save_mp3(self, text, filename=None, bitrate="128k"):
        if filename is None:
            filename = f"{current_timestamp('%Y%m%d%H%M%S')}_{uuid()[:5].lower()}"
        wav_path = self.read_save(text, filename)
        sound = AudioSegment.from_wav(wav_path)
        mp3_path = os.path.join(self.output, filename + ".mp3")
        sound.export(mp3_path, format="mp3", bitrate=bitrate)
        return mp3_path
