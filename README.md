# Hệ thống Phát hiện Sự cố Giao thông & Cảnh báo Lũ lụt

> Đồ án tốt nghiệp đại học — Nhóm 4 người | Deadline: 19/12

Hệ thống phân tích video CCTV, tự động phát hiện sự cố giao thông và cảnh báo đường ngập,
kết quả được hiển thị trên dashboard web real-time.

## Kiến trúc tổng quan

```
Video CCTV/clip
  → YOLO Detector/Tracker        (yolo26m)
  → Stage 1: Rule-based engine   (heuristic, không cần train)
  → Stage 2: Image Classifier    (xác nhận tai nạn)
  → Event Engine                 (threshold / smoothing / dedup / cooldown)
  → SQLite Database
  → FastAPI Backend → React Dashboard

Video CCTV/clip
  → Flood-road Detection (độc lập với pipeline trên)
  → Event Engine (dùng chung)
```

## Cài đặt

```bash
# 1. Tạo virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate    # Linux/macOS

# 2. Cài dependencies
pip install -r requirements.txt

# 3. (Tuỳ chọn) Development mode
pip install -e .
```

## Cấu trúc repo

```
incident_detection/
├── configs/                     # YAML config (threshold, hyperparams, paths)
├── data/                        # Dữ liệu — KHÔNG commit raw lên Git
│   ├── raw/
│   ├── processed/
│   └── splits/
├── src/
│   ├── detection_tracking/      # YOLO wrapper dùng chung
│   ├── incident_detection/
│   │   ├── stage1_rule_engine/  # Heuristic rule-based
│   │   └── event_engine/        # Threshold/smoothing/dedup
│   ├── stage2_classifier/       # Image classifier
│   ├── flood_model/             # Model phụ, độc lập
│   ├── database/                # schema.sql + db_client.py
│   ├── pipeline/                # end_to_end.py + event JSON schema
│   └── utils/                   # Shared utilities
├── dashboard/                   # React frontend
├── evaluation/                  # Shared evaluation harness
├── notebooks/
├── tests/
├── docs/
└── scripts/
```

## Dataset

| Dataset                        | Dùng cho              |
|--------------------------------|-----------------------|
| SO-TAD                         | Stage 2 train         |
| CADP                           | Stage 2 train         |
| TUM Accid3nD                   | Stage 2 train         |
| AI City Challenge 2021 Track 4 | Evaluation + Stage 1 tune |
| FloodNet                       | Flood model           |

> Raw data không được commit. Xem `scripts/download_data.py`.

## Chạy pipeline

```bash
python src/pipeline/end_to_end.py --config configs/pipeline.yaml --source <video_path>
```

## Đánh giá

```bash
python -m evaluation.metrics --help
```
