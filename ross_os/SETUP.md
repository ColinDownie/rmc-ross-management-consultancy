# Ross OS Infrastructure Setup

## Quick Start

### Step 1: Clone and Navigate
```bash
git clone https://github.com/ColinDownie/rmc-ross-management-consultancy.git
cd rmc-ross-management-consultancy
```

### Step 2: Install Dependencies
```bash
pip install -r ross_os/requirements.txt
```

### Step 3: Run Pipeline Validation
```bash
python ross_os/pipeline/video_engine/render_matrix.py
```

## Directory Structure

```
ross_os/
├── core/
│   └── kernels/
│       └── microkernel.py
├── data/
│   └── tenders/
│       └── master_registry.csv
├── pipeline/
│   └── video_engine/
│       └── render_matrix.py
├── requirements.txt
└── SETUP.md
```

## Configuration

Add your data to `ross_os/data/tenders/master_registry.csv` with the following columns:
- `date` - Entry date
- `sector` - Business sector
- `title` - Tender/project title
- `video_style` - Video rendering style
- `video_voiceover_prompt` - AI voiceover prompt

The pipeline will validate all entries against this schema before processing.
