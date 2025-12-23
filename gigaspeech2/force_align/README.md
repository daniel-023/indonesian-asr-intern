## Create Virtual Environment
```shell
module purge
module load python/3.10.9
python -m venv /scratch/users/ntu/daniel02/GigaSpeech2/envs/gsp2_align
source /scratch/users/ntu/daniel02/GigaSpeech2/envs/gsp2_align/bin/activate

pip install --upgrade pip
pip install "numpy==1.26.4"
pip install --extra-index-url https://download.pytorch.org/whl/cu121 "torch==2.1.0+cu121" "torchaudio==2.1.0+cu121"
pip install soundfile sox tqdm dataclasses
```

## Set Up Micromamba for Sox
```shell
# Install micromamba binary
cd /scratch/users/ntu/daniel02/GigaSpeech2
mkdir -p bin
wget -O bin/micromamba https://micro.mamba.pm/api/micromamba/linux-64/latest
chmod +x /path/to/your/bin/micromamba

# Set micromamba root directory
export MAMBA_ROOT_PREFIX=/scratch/users/ntu/daniel02/GigaSpeech2/mamba

# Create environment with sox
/scratch/users/ntu/daniel02/GigaSpeech2/bin/micromamba create -y \
  -n soxbin \
  -c conda-forge \
  sox
```

## Install Uroman (Unicode Romanization)
```shell
cd /scratch/users/ntu/daniel02/GigaSpeech2/GigaSpeech2
git submodule update --init --recursive
```

## Running Alignment Jobs

Submit batch jobs using PBS:
```shell
qsub -v COUNTRY=id,CHANNEL=MarinaTasha align.pbs
```

## Update Punctuation Handling
In `GigaSpeech2/pipeline/utils/force_alignment/text_normalization.py`
Replace:
```shell
punct_pattern = r"[" + config["punc_set"]
```
With:
```shell
# Allow apostrophes (') and hyphens (-) to survive punctuation filtering
safe_punc_set = config["punc_set"].replace("'", "").replace("-", "")
punct_pattern = r"[" + safe_punc_set
```