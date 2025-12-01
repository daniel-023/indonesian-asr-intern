## Create Virtual Environment
```shell
python -m venv /scratch/users/ntu/daniel02/GigaSpeech2/envs/gsp2_post
source /scratch/users/ntu/daniel02/GigaSpeech2/envs/gsp2_post/bin/activate

pip install --upgrade pip
pip install "numpy==1.26.4" fasttext tqdm soundfile
```

### Download Language ID Model
```shell
mkdir -p /scratch/users/ntu/daniel02/GigaSpeech2/models
wget -O /scratch/users/ntu/daniel02/GigaSpeech2/models/lid.176.bin \
  https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
```

## Configuration

### Modify Filtering Rules

Edit `filter_manifest.py` to customise language filtering:
```shell
cd /scratch/users/ntu/daniel02/GigaSpeech2/GigaSpeech2/pipeline/segmentation
vim filter_manifest.py
```

#### 1. Update `LanguageConfidenceFilter` class
```python
class LanguageConfidenceFilter(FilterStrategy):
    def __init__(self, model_path, required_langs=None, confidence_threshold=0.75):
        self.model = fasttext.load_model(model_path)
        self.required_langs = {f"__label__{lang.strip()}" for lang in required_langs}
        self.confidence_threshold = confidence_threshold

    def apply(self, line):
        labels, probabilities = self.model.predict(line["text"], k=1)
        return (labels[0] in self.required_langs and 
                probabilities[0] >= self.confidence_threshold)
```

**Changes:**
- Added `required_langs` parameter for flexible language selection
- Reduced `confidence_threshold` from 0.95 to 0.75 (handles ms/id confusion)
- Updated return condition to check language membership

#### 2. Add `--langs` argument to argument parser
```python
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--lid-model-path", type=str, required=True)
    parser.add_argument("--langs", type=str, required=True)
    return parser.parse_args()
```

#### 3. Update `main()` function
```python
def main():
    args = parse_args()
    required_langs = args.langs.split(",")
    strategies = [
        # CharsetFilter(),  # Optional: enable if needed
        LanguageConfidenceFilter(args.lid_model_path, required_langs, 0.75),
        AudioDurationFilter(2, 30),
    ]
    content_filter = ContentFilter(strategies)
    filter_manifests(args.input_dir, args.output_dir, content_filter)
```

## Usage

### Step 1: Filter Manifests
```shell
qsub -v ASR_LANG=en,COUNTRY=id,CHANNEL=GESTEofficial filter.pbs
```

### Step 2: Segment Audio
```shell
qsub -v ASR_LANG=en,COUNTRY=id,CHANNEL=GESTEofficial segment.pbs
```