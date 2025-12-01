## Create virtual environment
```shell
module purge
module load python/3.10.9
python -m venv /scratch/users/ntu/daniel02/GigaSpeech2/envs/gsp2
source /scratch/users/ntu/daniel02/GigaSpeech2/envs/gsp2/bin/activate
pip install --upgrade pip
pip install faster-whisper tqdm librosa torchaudio
```

## Running ASR Jobs

Submit batch jobs using PBS with the following parameters:
```shell
qsub -J 1-7 -v ASR_LANG=en,COUNTRY=id,CHANNEL=apbshow conv_asr.pbs
```

**Parameters:**
- `ASR_LANG`: Target language code: `en` or `id`
- `COUNTRY`: For `en`: English accent country e.g. `id` or `ph`
- `MODE`: `mono` for monolingual and `cs`for code-switch
- `CHANNEL`: YouTube channel
- `-J 1-7`: Job array range (optional)

## Configuration

**Important:** Modify line 102 in `GigaSpeech2/pipeline/convert_transcribe/convert_and_transcribe.py`:
```python
# Replace with this line:
segments, info = model.transcribe(audio_path, language=args.lang, beam_size=5)
```