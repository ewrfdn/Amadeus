import wave

import numpy as np
import pyaudio
import sys

sys.path.append('vits_server/vits')
from vits_server.vits_service import VitsService

config_combo = [
    # ("vits_server/models/CyberYunfei3k.json", "vits_server/models/yunfei3k_69k.pth"),
    ("C:/dev/digitial-life/vits_server/models/paimon6k.json",
     "C:/dev/digitial-life/vits_server/models/paimon6k_390k.pth"),
    # ("vits_server/models/ayaka.json", "vits_server/models/ayaka_167k.pth"),
    # ("vits_server/models/ningguang.json", "vits_server/models/ningguang_179k.pth"),
    # ("vits_server/models/nahida.json", "vits_server/models/nahida_129k.pth"),
    # ("vits_server/models_unused/miko.json", "vits_server/models_unused/miko_139k.pth"),
    # ("vits_server/models_unused/yoimiya.json", "vits_server/models_unused/yoimiya_102k.pth"),
    # ("vits_server/models/noelle.json", "vits_server/models/noelle_337k.pth"),
    # ("vits_server/models_unused/yunfeimix.json", "vits_server/models_unused/yunfeimix_122k.pth"),
    # ("vits_server/models_unused/yunfeineo.json", "vits_server/models_unused/yunfeineo_25k.pth"),
    # ("vits_server/models/yunfeimix2.json", "vits_server/models/yunfeimix2_47k.pth")
    # ("vits_server/models_unused/zhongli.json", "vits_server/models_unused/zhongli_44k.pth"),
]
for cfg, model in config_combo:
    a = VitsService(cfg, model, 'test', 1)
    p = pyaudio.PyAudio()
    audio = a.read('统一计算设备架构由 NVIDIA 推出的并行计算平台和编程模型。 它通过利用图形处理单元 (GPU) 的强大功能来显着提高计算性能。'
                   '最新发行版本11.6.2，2022年3月发行。目前几乎所有的编程语言，不使用特定框架，只能使用CPU运行所编的程序。'
                   'std::thread也是将线程开在CPU中。使用GPU编程可以使用更多的流处理器和更多的线程')
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=a.hps.data.sampling_rate,
                    output=True
                    )
    # data = audio.astype(np.float32).tostring()
    # stream.write(data)
    # Set the output file name
    output_file = "output.wav"

    # Set the audio properties
    num_channels = 1
    sample_width = 2  # Assuming 16-bit audio
    frame_rate = a.hps.data.sampling_rate

    # Convert audio data to 16-bit integers
    audio_int16 = (audio * np.iinfo(np.int16).max).astype(np.int16)

    # Open the output file in write mode
    with wave.open(output_file, 'wb') as wav_file:
        # Set the audio properties
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)

        # Write audio data to the file
        wav_file.writeframes(audio_int16.tobytes())
