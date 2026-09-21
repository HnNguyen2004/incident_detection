# AGENTS.md

File ngữ cảnh dành cho các AI coding agent (Claude Code, Cursor, Copilot, v.v.) khi làm việc trong repository này.

## Dự án

**Tên đề tài (chính thức):** Xây dựng và tích hợp hệ thống học sâu phát hiện sự cố giao thông và cảnh báo lũ lụt vào nền tảng hỗ trợ quản lý đô thị
**Loại:** Đồ án/khóa luận tốt nghiệp đại học (nhóm 4 người)
**Deadline:** 19/12

## Mục tiêu & phạm vi

Xây dựng một hệ thống phân tích video nhận luồng CCTV/video, tự động phát hiện sự cố, tạo sự kiện có cấu trúc và hiển thị trên dashboard. Đề tài chủ đích tập trung vào **một bài toán ML lõi** (phát hiện sự cố giao thông) kèm **một model phụ đơn giản** (nhận diện đường ngập), thay vì phát triển nhiều model song song.

**Trong phạm vi:**
- Phát hiện sự cố giao thông từ CCTV cố định (không phải dashcam)
- Nhận diện đường ngập (chỉ ở mức cảnh báo, không đo độ sâu nước)
- Pipeline end-to-end: video → inference → event engine → database → dashboard/notification
- Đánh giá không chỉ bằng accuracy: precision, recall, F1, false alarms/hour, detection delay, throughput/latency

**Ngoài phạm vi — không đề xuất hoặc thêm vào:**
- Một nền tảng smart-city đầy đủ
- Các domain phát hiện khác (fire/smoke/crime/vi phạm giao thông)
- Kubernetes hay hạ tầng phân tán — đây là đồ án, không phải hạ tầng production
- Mục tiêu độ trễ real-time/cảnh báo sớm — hệ thống này là **xác nhận sau sự cố (post-hoc)**, chấp nhận trễ 1-2 giây

## Kiến trúc hệ thống

```
Video CCTV/clip
  -> YOLO Detector/Tracker (module dùng chung)
  -> Stage 1: rule-based candidate detection (không cần train; dùng output
     của detector/tracker qua nhiều frame liên tiếp để gắn cờ thay đổi trạng thái
     đột ngột — dừng đột ngột, lệch làn, lệch nhịp so với xe xung quanh)
  -> Stage 2: image classifier (xác nhận candidate được gắn cờ có phải tai nạn thật không)
  -> Event Engine (threshold, temporal smoothing, deduplication, cooldown)
  -> Database (structured event + evidence)
  -> Dashboard / Notification

Video CCTV/clip
  -> Flooded-road Detection (classification/segmentation, độc lập với phần trên)
  -> Normal / Possible Flood / Severe Flood
  -> đổ vào cùng Event Engine
```

Lưu ý: bản đề xuất ban đầu dùng fusion đầy đủ appearance + trajectory qua temporal
model (TCN/LSTM/Transformer) cho model chính. **Hướng hiện tại (thực tế đang triển khai)
là pipeline 2 giai đoạn đơn giản hơn ở trên (Stage 1 rule-based + Stage 2 classifier).**
Không tự ý quay lại hướng fusion/temporal model trừ khi được yêu cầu rõ ràng.

## Cấu trúc repo

```
incident_detection/
├── configs/                          # yaml config — threshold, hyperparam, path
├── data/
│   ├── raw/{ai_city_2021_track4, so_tad, cadp, tum_accid3nd, floodnet}/
│   ├── processed/
│   └── splits/
├── src/
│   ├── detection_tracking/           # wrapper YOLO detector/tracker dùng chung
│   ├── incident_detection/
│   │   ├── stage1_rule_engine/       # rule-based, không cần train
│   │   └── event_engine/             # threshold/smoothing/dedup/cooldown
│   ├── stage2_classifier/            # classifier ảnh tai nạn
│   ├── flood_model/                  # model phụ, độc lập
│   ├── database/                     # schema.sql, db_client.py
│   ├── pipeline/                     # end_to_end.py ghép nối toàn bộ
│   └── utils/
├── dashboard/                        # frontend + notification
├── evaluation/                       # harness đo metric dùng chung — tái sử dụng, không viết lại
├── notebooks/
├── tests/
├── docs/
└── scripts/
```

## Phân công module (chỉ để tham khảo — không tự ý đổi nếu chưa được yêu cầu)

| Khu vực | Người phụ trách | Ghi chú |
|---|---|---|
| `detection_tracking/`, `incident_detection/` (Stage 1 + phần ranh giới với Event Engine), `stage2_classifier/` | Nguyên | Core AI. Phần *implementation* của Event Engine do Lãnh phụ trách — Nguyên chỉ định nghĩa format output "incident score". |
| `flood_model/` | Son | Độc lập với pipeline traffic. |
| `database/`, wiring `pipeline/`, `src/incident_detection/event_engine/`, backend/API | Lãnh | Đồng thời lead kiến trúc repo và harness `evaluation/` dùng chung. |
| `dashboard/` | Khang | UI/frontend/testing/documentation. Giữ công việc của thành viên này ở UI, testing, docs — không giao logic backend, thiết kế DB schema, hay code model. |

## Ràng buộc kỹ thuật quan trọng

- **Domain gap là có thật và đã được xác định:** các dataset tai nạn tốt nhất (DoTA) là dashcam-based; đề tài này dùng CCTV cố định. Dữ liệu train (SO-TAD, CADP, TUM Accid3nD) chỉ dùng cho Stage 2; AI City Challenge 2021 Track 4 (camera cố định, video liên tục ~15 phút) dùng cho **evaluation** và làm nguồn ảnh negative/normal để tune Stage 1 — không nhầm lẫn giữa nguồn dữ liệu train và evaluation.
- Tai nạn là sự kiện hiếm → dữ liệu mất cân bằng. Không mặc định dùng accuracy thuần; ưu tiên PR/F1, event-level recall, false-alarms/hour.
- Stage 1 phải giữ nhẹ, không phụ thuộc framework training (đây là heuristic/rule-based trên output của tracker, không phải model).
- Mọi threshold hay hằng số có thể tune phải để trong `configs/`, không hardcode trong source code.

## Đánh giá

- **Model chính:** Precision, Recall, F1/PR-AUC, event-level recall, false alarms/hour, detection delay
- **Model phụ:** F1/IoU hoặc accuracy
- **Hệ thống:** FPS/throughput, end-to-end latency, độ ổn định khi stream liên tục
- Dùng chung harness `evaluation/metrics.py` cho cả 2 model — không viết 2 script chấm điểm riêng biệt.

## Quy ước dành cho agent

- Codebase chủ yếu bằng Python. Giữ mỗi module trong `src/<module>/` độc lập; logic dùng chung đặt ở `src/utils/` hoặc `detection_tracking/`.
- Không tự ý tái cấu trúc layout thư mục gốc nếu chưa xác nhận với người dùng.
- Khi thêm detector/model mới, phải thêm test tương ứng trong `tests/`.
- Đối tượng event truyền giữa các stage phải theo đúng 1 JSON schema (định nghĩa trong `src/pipeline/` — kiểm tra ở đó trước khi tự tạo schema mới).
- Giữ Stage 1 và Stage 2 tách rời nhau: Stage 2 phải gọi/train được độc lập với tracking live (nó train trên clip/ảnh đã cắt sẵn từ trước).

## Trạng thái hiện tại

Đang ở Phase 1 (Foundation) trong kế hoạch 5 phase, ~13 tuần, kết thúc 19/12. Kiểm tra task tracker của nhóm (Google Sheet / GitHub Issues) để biết trạng thái task hiện tại thay vì tự suy đoán — file này mô tả kiến trúc và quy ước ổn định, không phải trạng thái task theo ngày.
