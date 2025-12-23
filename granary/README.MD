## Write input manifest using `input_manifest.sh`

## Clone NeMo SDP
```shell
cd /scratch/users/ntu/daniel02/Granary/
module load git
git clone https://github.com/NVIDIA/NeMo-speech-data-processor.git
```

## Modify Config File
```shell
vim /NeMo-speech-data-processor/dataset_configs/multilingual/granary/config.yaml
```

## Install Dependencies
```shell
pip install -r requirements/main.txt
```

## Create Commonn Phrases File
```shell
PHRASE_DIR="NeMo-speech-data-processor/dataset_configs/multilingual/granary/partials/common_phrases"
mkdir -p "$PHRASE_DIR"
: > "$PHRASE_DIR/id.txt"   # create empty file for Indonesian language
```

## Running Granary
```shell
qsub ~/granary_run.pbs
```

## GigaSpeech2 post-processing to reduce segment length
1. Split Manifests by Punctuation
```shell
python split_txt.py --corpus-dir ./scratch/Granary/gsp2_prep/clips
```

2. Slice Granary Clips
```shell
module load python/3.10.9
module load ffmpeg
python slice_granary.py \
  --manifest /scratch/users/ntu/daniel02/Granary/id/work/granary_test/output/id/manifest_20.json \
  --out-dir /scratch/users/ntu/daniel02/Granary/gsp2_prep/clips
```

3. Follow GigaSpeech2 Pipeline:
    - Force Alignment
    - Filtering
    - Segmentation