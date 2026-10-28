# 📚 TRA CỨU CHI TIẾT TỪNG MODULE VÀ HÀM (API REFERENCE)

> Tài liệu kỹ thuật chi tiết dành cho lập trình viên và các kỹ sư AI muốn can thiệp, mở rộng các module trong `levi`.

---

## 1. Nhóm Module `core/` (Phân Tích AI & Media)

### 1.1. `core.brand_engine.BrandEngine`
- `__init__(brand_kit_path: Optional[str] = None)`: Khởi tạo engine và nạp cấu hình từ `brand-kit.md`.
- `load_from_markdown(path: str) -> Dict[str, Any]`: Dùng Regex phân tích các trường thương hiệu, font chữ và bảng màu hex.
- `get_fonts() -> Dict[str, str]`: Trả về font cho `headline`, `caption`, `accent`.
- `get_colors() -> Dict[str, str]`: Trả về mã màu hex cho `primary`, `secondary`, `accent`, `highlight`.
- `get_audio_standards() -> Dict[str, float]`: Trả về ngưỡng `target_lufs`, `true_peak`, `bgm_volume_db`.

### 1.2. `core.whisper_transcriber.WhisperTranscriber`
- `load_transcript_json(json_path: str) -> List[Dict[str, Any]]`: Nạp file JSON transcript và chuẩn hóa mốc thời gian.
- `_chunk_words(words: List[Dict], max_words: int = 4) -> List[Dict]`: Gom các từ đơn lẻ thành cụm 2-4 từ ngắn dễ đọc trên video dọc.
- `create_mock_transcript_from_text(text: str, total_duration: float) -> List[Dict]`: Tạo phụ đề giả lập đều nhịp từ văn bản thuần.

### 1.3. `core.audio_master.AudioMaster`
- `get_loudnorm_filter_string() -> str`: Sinh chuỗi filter FFmpeg loudnorm chuẩn EBU R128 (`I=-14.0`, `TP=-1.5`, `LRA=7.0`).
- `build_ffmpeg_audio_master_command(...) -> List[str]`: Xây dựng mảng lệnh FFmpeg cân bằng giọng nói và hạ âm ngầm BGM (Audio ducking).
- `export_master_audio(...) -> bool`: Gọi thực thi FFmpeg để xuất file âm thanh hoàn thiện.

### 1.4. `core.chin_lock.ChinLock`
- `_init_detector()`: Nạp mô hình mạng nơ-ron OpenCV YuNet (`face_detection_yunet_2023mar.onnx`).
- `analyze_frame(frame_img) -> Optional[Dict]`: Quét 1 frame ảnh, trả về tọa độ hộp mặt, đáy cằm (`chin_y`), tọa độ an toàn cho phụ đề (`safe_sub_top_y`) và góc nghiêng đầu (`head_roll_deg`).
- `get_timeline_chin_anchors(video_path: str, sample_interval_sec: float = 0.5) -> List[Dict]`: Quét toàn bộ video theo chu kỳ mẫu và làm mượt tọa độ neo chữ.

### 1.5. `core.rough_cutter.RoughCutter`
- `compute_cuts_from_speech_segments(speech_segments: List[Dict], ...) -> List[Dict]`: Tính toán các đoạn giữ lại, cắt khoảng lặng và xen kẽ cỡ cảnh Micro-zoom (1.0 vs 1.08).
- `get_timeline_duration(cuts: List[Dict]) -> float`: Tính tổng thời lượng timeline sau khi cắt.

---

## 2. Nhóm Module `engines/` (Bộ Điều Khiển Xuất Bản)

### 2.1. `engines.adobe.pr_xml_builder.PremiereXMLBuilder`
- `generate_xml_timeline(main_video_path, cuts, output_xml_path, ...) -> str`: Sinh file Final Cut Pro XML (`<xmeml version="4">`) tương thích 100% Adobe Premiere Pro, hỗ trợ video tracks, B-Roll và audio tracks riêng biệt.

### 2.2. `engines.adobe.ae_script_generator.AfterEffectsScriptGenerator`
- `generate_jsx_script(...) -> str`: Sinh mã JavaScript ExtendScript (`.jsx`) cho After Effects, tự động áp dụng biểu thức nảy đàn hồi lò xo (*Inertial Bounce Expression*) vào câu Hook và rải subtitles né cằm.

### 2.3. `engines.adobe.aerender_service.AERenderService`
- `_find_aerender_executable() -> Optional[str]`: Tự động tìm đường dẫn `aerender.exe` trên máy tính.
- `render_project(...) -> bool`: Gọi render ngầm một Composition trong file `.aep` qua GPU bằng dòng lệnh.

### 2.4. `engines.capcut.draft_builder.CapCutDraftBuilder`
- `add_main_video(video_path, duration_sec)`: Thêm video chính vào track 0.
- `add_hook(headline, eyebrow, duration_sec, font_name, font_color)`: Thêm cụm chữ Hook lớn ở 1/3 trên màn hình.
- `add_subtitles(subtitles, font_name, font_color, transform_y)`: Thêm phụ đề chạy từng câu né cằm.
- `finalize() -> str`: Ghi và hoàn tất cấu trúc thư mục dự án CapCut Desktop.

### 2.5. `engines.remotion.render_alpha.RemotionAlphaRenderer`
- `build_render_command(composition_id, output_path, codec) -> List[str]`: Xây dựng lệnh render Remotion với kênh Alpha (ProRes 4444 hoặc WebM VP9).
- `render_alpha_overlay(...) -> bool`: Thực thi render đồ họa 60fps trong suốt.

---

## 3. Nhóm Module `workflows/` (Quy Trình Tự Động Hóa)

### 3.1. `workflows.autopilot.AutopilotEngine`
- `run_autopilot(video_path, project_name, headline, ...) -> Dict[str, Any]`: Điều phối toàn bộ quy trình 7 bước tự động từ A-Z.

### 3.2. `workflows.beat_sheet.BeatSheetGenerator`
- `generate_contact_sheet(keyframe_images, beat_labels, output_path) -> str`: Ghép các ảnh keyframe thành lưới storyboard `beat_sheet.jpg`.
- `extract_and_generate_from_video(video_path, cuts, output_path) -> Optional[str]`: Tự động trích xuất các khung hình then chốt từ video và tạo Beat Sheet.

### 3.3. `workflows.trial_reels.TrialReelsGenerator`
- `generate_three_variants(base_headline, base_cuts) -> List[Dict]`: Sinh 3 biến thể A/B/C với phong cách Hook và nhịp điệu khác nhau để thử nghiệm Instagram Trial Reels.

### 3.4. `workflows.carousel_story.carousel.CarouselStoryGenerator`
- `generate_carousel_slides(slides_data, output_dir) -> List[str]`: Sinh trọn bộ slide 1080x1350 (4:5) cho bài đăng vuốt ngang Instagram Carousel.
- `generate_story_slide(headline, sticker_type, output_path) -> str`: Sinh frame Story 9:16 chừa sẵn vị trí dán Sticker tương tác.
