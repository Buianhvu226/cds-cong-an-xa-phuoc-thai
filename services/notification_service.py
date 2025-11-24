from datetime import date, datetime

from database import db
from models import (
    DanhSachPhuongTien,
    DanhSachThietBiKyThuatNghiepVu,
    DanhSachThietBiVanPhongDoanhTrai,
    DanhSachVuKhiCongCuHoTro,
    DanhSachTrangThietBiThuy,
)
from utils.date_utils import get_inspection_status


class NotificationService:
    def __init__(self):
        self.models = [
            ("weapons", DanhSachVuKhiCongCuHoTro, "ten_tai_san"),
            ("vehicles", DanhSachPhuongTien, "ten_phuong_tien"),
            ("water", DanhSachTrangThietBiThuy, "ten_trang_bi"),
            ("technical", DanhSachThietBiKyThuatNghiepVu, "ten_tai_san"),
            ("office", DanhSachThietBiVanPhongDoanhTrai, "ten_tai_san"),
        ]

        # Vehicle specific reminder fields
        self.vehicle_date_fields = [
            ("ngay_dang_kiem", "Ngày đăng kiểm"),
            ("ngay_thay_nhot", "Ngày thay nhớt"),
            ("ngay_thay_vo", "Ngày thay vỏ"),
        ]

    def get_notifications(self, priority=None, limit=None):
        """Get all notifications/alerts"""
        from sqlalchemy import inspect

        all_notifications = []
        today = date.today()

        try:
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
        except Exception:
            return []

        for asset_type, model_class, name_field in self.models:
            table_name = model_class.__tablename__
            if table_name not in existing_tables:
                continue

            try:
                assets = model_class.query.filter_by(is_deleted=False).all()
            except Exception:
                continue

            for asset in assets:
                asset_name = getattr(asset, name_field, "")

                # Always check upcoming inspection date if available
                notifications = []
                notifications.extend(
                    self._build_notification(
                        asset_type,
                        asset,
                        asset_name,
                        getattr(asset, "ngay_kiem_tra_tiep_theo", None),
                        "Ngày kiểm tra tiếp theo",
                        today,
                        priority,
                    )
                )

                # Additional vehicle schedules
                if asset_type == "vehicles":
                    for field_name, label in self.vehicle_date_fields:
                        date_value = getattr(asset, field_name, None)
                        notifications.extend(
                            self._build_notification(
                                asset_type,
                                asset,
                                asset_name,
                                date_value,
                                label,
                                today,
                                priority,
                            )
                        )

                all_notifications.extend(notifications)

        priority_order = {"high": 0, "medium": 1, "low": 2}
        all_notifications.sort(
            key=lambda x: (priority_order.get(x["priority"], 99), x["days_until"])
        )

        if limit:
            all_notifications = all_notifications[:limit]

        return all_notifications

    def _build_notification(
        self,
        asset_type,
        asset,
        asset_name,
        date_value,
        label,
        today,
        priority_filter,
    ):
        if not date_value:
            return []

        # Convert to date object
        if isinstance(date_value, datetime):
            due_date = date_value.date()
        elif isinstance(date_value, str):
            try:
                due_date = datetime.fromisoformat(date_value).date()
            except ValueError:
                return []
        else:
            due_date = date_value

        status = get_inspection_status(due_date, today)
        priority_map = {"overdue": "high", "due_soon": "medium", "normal": "low"}
        notification_priority = priority_map.get(status, "low")

        if priority_filter and notification_priority != priority_filter:
            return []

        days_until = (due_date - today).days

        notification = {
            "asset_type": asset_type,
            "ma_tai_san": asset.ma_tai_san,
            "ten_tai_san": asset_name,
            "target_date": due_date.isoformat(),
            "target_label": label,
            "ngay_kiem_tra_tiep_theo": due_date.isoformat(),
            "status": status,
            "priority": notification_priority,
            "days_until": days_until,
            "asset_id": asset.id,
        }

        return [notification]

    def get_notification_counts(self):
        notifications = self.get_notifications()

        counts = {"high": 0, "medium": 0, "low": 0, "total": len(notifications)}

        for notification in notifications:
            priority = notification["priority"]
            if priority in counts:
                counts[priority] += 1

        return counts
