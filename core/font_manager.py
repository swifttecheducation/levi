#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/font_manager.py — Quản lý & Định tuyến Bộ Font Chữ Việt Hóa Toàn Diện (Font Manager Engine).
Tích hợp toàn bộ 32 tệp font chuẩn điện ảnh (14 họ font) từ Xưởng Dựng Rảnh Tay & Styles Library:
  1. Instrument Serif (Báo chí, tạp chí cao cấp của Sia Trương)
  2. Be Vietnam Pro (Chuẩn quốc dân cho phụ đề tiếng Việt trên di động)
  3. Inter / Inter Tight (Tối giản hiện đại chuẩn Apple)
  4. Playfair Display (Serif cổ điển sang trọng quyền quý)
  5. Poppins (Tròn trịa, năng động, Gen Z)
  6. Coolvetica (Chữ đậm Viral, phong cách Streetwear)
  7. Caveat (Chữ viết tay nghệ thuật phóng khoáng)
  8. SVN-Chicken Noodle Soup (Chữ viết tay tiếng Việt ấm áp)
  9. Pinyon Script (Thư pháp chữ ký quý phái)
  10. DM Sans (Hình học thanh thoát, hiện đại)
  11. Space Grotesk (Futuristic, công nghệ số)
  12. Alegreya (Nhân văn, học thuật, chiều sâu)
  13. Shrikhand (Retro, tiêu đề nổi bật)
  14. Julius Sans One (In hoa thanh lịch tối giản)
"""

import os
from typing import Dict, Any, List, Optional


FONT_FAMILIES: Dict[str, Dict[str, Any]] = {
    "Instrument Serif": {
        "name": "Instrument Serif",
        "category": "Serif Báo Chí & Tạp Chí",
        "description": "Font serif thanh mảnh, sang trọng đặc trưng của Sia Trương và tạp chí cao cấp (Styles H4, H10, C7, C9, X16).",
        "files": {
            "regular": "InstrumentSerif-Regular.ttf",
            "italic": "InstrumentSerif-Italic.ttf"
        },
        "best_for": ["hook", "accent", "magazine"]
    },
    "Be Vietnam Pro": {
        "name": "Be Vietnam Pro",
        "category": "Sans-Serif Chuẩn Phụ Đề Tiếng Việt",
        "description": "Bộ font thiết kế riêng cho tiếng Việt, dấu thanh chuẩn mực 100%, không bao giờ lỗi ô vuông, tối ưu đọc trên màn hình điện thoại.",
        "files": {
            "regular": "BeVietnamPro-Regular.ttf",
            "medium": "BeVietnamPro-Medium.ttf",
            "bold": "BeVietnamPro-Bold.ttf",
            "italic": "BeVietnamPro-SemiBoldItalic.ttf"
        },
        "best_for": ["caption", "body", "ui"]
    },
    "Inter": {
        "name": "Inter",
        "category": "Sans-Serif Tối Giản Công Nghệ",
        "description": "Chuẩn mực thiết kế Apple, dứt khoát, dễ đọc ở mọi kích cỡ nhỏ (Styles H10, C8, L4, V15, G4).",
        "files": {
            "regular": "Inter-Regular.otf",
            "medium": "Inter-Medium.ttf",
            "bold": "Inter-Bold.otf",
            "black": "Inter-Black.otf",
            "variable": "Inter-VF.ttf"
        },
        "best_for": ["hook", "caption", "tech"]
    },
    "Playfair Display": {
        "name": "Playfair Display",
        "category": "Serif Cổ Điển Sang Trọng",
        "description": "Font có độ tương phản nét dày nét thanh cao, tạo cảm giác uy quyền, chuyên nghiệp và đắt giá.",
        "files": {
            "semibold": "PlayfairDisplay-SemiBold.ttf",
            "variable": "PlayfairDisplay-VF.ttf"
        },
        "best_for": ["hook", "title"]
    },
    "Poppins": {
        "name": "Poppins",
        "category": "Geometric Sans Năng Động",
        "description": "Font chữ hình học bo tròn, năng động, đậm chất hiện đại và Gen Z.",
        "files": {
            "regular": "Poppins-Regular.ttf",
            "semibold": "Poppins-SemiBold.ttf",
            "bold": "Poppins-Bold.ttf",
            "black": "Poppins-Black.ttf"
        },
        "best_for": ["hook", "bold_statement"]
    },
    "Coolvetica": {
        "name": "Coolvetica",
        "category": "Display Bold Viral",
        "description": "Font chữ nét cực dày, nén chặt, tạo sự áp đảo thị giác mạnh mẽ cho các video viral, streetwear.",
        "files": {
            "regular": "Coolvetica-Rg.otf",
            "heavy": "Coolvetica-Hv-Comp.otf"
        },
        "best_for": ["hook", "punch_word"]
    },
    "Caveat": {
        "name": "Caveat",
        "category": "Handwriting Phóng Khoáng",
        "description": "Chữ viết tay bút lông tự nhiên, phóng khoáng, dùng cho các ghi chú, mũi tên chú thích.",
        "files": {
            "variable": "Caveat-VF.ttf"
        },
        "best_for": ["accent", "note", "arrow"]
    },
    "SVN-Chicken Noodle Soup": {
        "name": "SVN-Chicken Noodle Soup",
        "category": "Handwriting Tiếng Việt Ấm Áp",
        "description": "Chữ viết tay Việt hóa tròn trịa, ấm áp, gần gũi như trang sổ lưu niệm cá nhân.",
        "files": {
            "regular": "SVN-Chicken Noodle Soup.otf"
        },
        "best_for": ["accent", "scrapbook", "warm"]
    },
    "Pinyon Script": {
        "name": "Pinyon Script",
        "category": "Calligraphy Quý Tộc",
        "description": "Thư pháp chữ ký quý phái, thanh thoát, phù hợp với các video phong cách hoàng gia, trang sức, thời trang cao cấp.",
        "files": {
            "regular": "PinyonScript-Regular.ttf"
        },
        "best_for": ["accent", "signature", "luxe"]
    },
    "DM Sans": {
        "name": "DM Sans",
        "category": "Geometric Sans Thanh Thoát",
        "description": "Font hình học thanh lịch, độ thoáng cao, hỗ trợ đa trọng lượng linh hoạt.",
        "files": {
            "variable": "DMSans-Variable.ttf",
            "italic": "DMSans-Italic-Variable.ttf"
        },
        "best_for": ["body", "caption", "clean"]
    },
    "Space Grotesk": {
        "name": "Space Grotesk",
        "category": "Monospace / Tech AI",
        "description": "Mang hơi thở tương lai, không gian vũ trụ, rất hợp cho các video AI, lập trình và công nghệ cao.",
        "files": {
            "variable": "SpaceGrotesk-VF.ttf"
        },
        "best_for": ["accent", "tech_spec", "hud"]
    },
    "Alegreya": {
        "name": "Alegreya",
        "category": "Serif Nhân Văn & Tri Thức",
        "description": "Font chữ cổ điển giàu nhịp điệu văn học, mang lại cảm giác tri thức, sâu lắng, tin cậy.",
        "files": {
            "variable": "Alegreya-VF.ttf",
            "italic": "Alegreya-Italic-VF.ttf"
        },
        "best_for": ["hook", "quote", "thinker"]
    },
    "Shrikhand": {
        "name": "Shrikhand",
        "category": "Retro Display Nghệ Thuật",
        "description": "Font chữ đậm đà mang phong cách biển hiệu thủ công retro, nổi bật từ cái nhìn đầu tiên.",
        "files": {
            "regular": "Shrikhand-Regular.ttf"
        },
        "best_for": ["hook", "bold_retro"]
    },
    "Julius Sans One": {
        "name": "Julius Sans One",
        "category": "All-Caps Minimal",
        "description": "Font in hoa thanh mảnh, khoảng cách chữ rộng thoáng, tạo nét tối giản tinh tế.",
        "files": {
            "regular": "JuliusSansOne-Regular.ttf"
        },
        "best_for": ["subtitle", "minimal_label"]
    }
}


CURATED_FONT_PACKS: Dict[str, Dict[str, Any]] = {
    "1": {
        "id": "editorial_luxe",
        "name": "Editorial Luxe (Tạp Chí Sang Trọng - Chuẩn Sia Trương)",
        "headline": "Instrument Serif",
        "caption": "Be Vietnam Pro",
        "accent": "Caveat",
        "description": "Tiêu đề serif báo chí thanh lịch, phụ đề Be Vietnam Pro nét căng, điểm nhấn viết tay nghệ thuật."
    },
    "2": {
        "id": "apple_minimal",
        "name": "Apple Minimal (Tối Giản Hiện Đại Chuẩn Apple)",
        "headline": "Inter",
        "caption": "Be Vietnam Pro",
        "accent": "Space Grotesk",
        "description": "Phong cách công nghệ tinh gọn, không rườm rà, nhịp dứt khoát như quảng cáo Apple."
    },
    "3": {
        "id": "gen_z_pop",
        "name": "Gen Z Pop (Năng Động & Bùng Nổ Sáng Tạo)",
        "headline": "Poppins",
        "caption": "Be Vietnam Pro",
        "accent": "SVN-Chicken Noodle Soup",
        "description": "Tròn trịa, vui tươi, viết tay tiếng Việt ấm áp gần gũi, cuốn hút người xem trẻ tuổi."
    },
    "4": {
        "id": "bold_streetwear",
        "name": "Bold Streetwear (Đậm Đà Viral & Cá Tính Mạnh)",
        "headline": "Coolvetica",
        "caption": "Be Vietnam Pro",
        "accent": "Caveat",
        "description": "Chữ cực đậm, tạo sức ép thị giác lớn, dành cho nội dung tài chính, thể thao, streetwear."
    },
    "5": {
        "id": "classic_elegance",
        "name": "Classic Elegance (Cổ Điển Hoàng Gia & Quý Phái)",
        "headline": "Playfair Display",
        "caption": "Be Vietnam Pro",
        "accent": "Pinyon Script",
        "description": "Font quyền lực kết hợp thư pháp chữ ký, chuẩn mực cho khóa học cao cấp, bất động sản, trang sức."
    },
    "6": {
        "id": "deep_thinker",
        "name": "Deep Thinker (Tri Thức Sâu Sắc & Kể Chuyện)",
        "headline": "Alegreya",
        "caption": "DM Sans",
        "accent": "Instrument Serif",
        "description": "Trầm ấm, chiêm nghiệm, rất hợp video tâm sự (Confessional), chia sẻ bài học cuộc sống."
    }
}


class FontManager:
    def __init__(self, fonts_dir: Optional[str] = None):
        if fonts_dir:
            self.fonts_dir = fonts_dir
        else:
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.fonts_dir = os.path.join(root_dir, "assets", "fonts")

    @property
    def total_families(self) -> int:
        return len(FONT_FAMILIES)

    def list_families(self) -> List[Dict[str, Any]]:
        return list(FONT_FAMILIES.values())

    def get_family(self, name: str) -> Optional[Dict[str, Any]]:
        for fam_name, data in FONT_FAMILIES.items():
            if fam_name.lower() == name.lower().strip():
                return data
        return None

    def resolve_font_file(self, family_name: str, weight: str = "regular", italic: bool = False) -> Optional[str]:
        """
        Tìm tệp font (.ttf / .otf) thực tế trong thư mục assets/fonts/.
        """
        fam = self.get_family(family_name)
        if not fam:
            return None

        files = fam["files"]
        target_file = None

        if italic and "italic" in files:
            target_file = files["italic"]
        elif weight in files:
            target_file = files[weight]
        elif "regular" in files:
            target_file = files["regular"]
        elif "variable" in files:
            target_file = files["variable"]
        else:
            target_file = next(iter(files.values()))

        full_path = os.path.join(self.fonts_dir, target_file)
        return full_path if os.path.exists(full_path) else None

    def list_packs(self) -> Dict[str, Dict[str, Any]]:
        return CURATED_FONT_PACKS

    def get_pack(self, key: str) -> Optional[Dict[str, Any]]:
        return CURATED_FONT_PACKS.get(key.strip())
