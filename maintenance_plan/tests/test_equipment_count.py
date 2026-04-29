# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from .common import TestMaintenanceBase


class TestEquipmentCount(TestMaintenanceBase):
    """Test _compute_search_maintenance_plan_count in maintenance.equipment"""

    def test_search_maintenance_plan_count_zero(self):
        """Test search_maintenance_plan_count when no plans exist"""
        # Create a new equipment with no maintenance plans
        equipment = self.MaintenanceEquipment.create(
            {
                "name": "Equipment No Plans",
            }
        )
        equipment._compute_search_maintenance_plan_count()
        self.assertEqual(
            equipment.search_maintenance_plan_count,
            0,
            "search_maintenance_plan_count should be 0 when no plans exist",
        )

    def test_search_maintenance_plan_count_one(self):
        """Test search_maintenance_plan_count with one active plan"""
        # Create a maintenance plan for the equipment
        self.MaintenancePlan.create(
            {
                "equipment_id": self.equipment.id,
                "maintenance_kind_id": self.maintenance_kind.id,
            }
        )
        self.equipment._compute_search_maintenance_plan_count()
        self.assertGreaterEqual(
            self.equipment.search_maintenance_plan_count,
            1,
            "search_maintenance_plan_count should be at least 1 when plan exists",
        )

    def test_search_maintenance_plan_count_multiple(self):
        """Test search_maintenance_plan_count with multiple plans"""
        # Create a second maintenance kind
        kind2 = self.MaintenanceKind.create(
            {
                "name": "Second Kind",
                "code": "SECOND_KIND",
                "priority": "optional",
            }
        )
        # Create multiple maintenance plans for the equipment with different kinds
        self.MaintenancePlan.create(
            [
                {
                    "equipment_id": self.equipment.id,
                    "maintenance_kind_id": self.maintenance_kind.id,
                },
                {
                    "equipment_id": self.equipment.id,
                    "maintenance_kind_id": kind2.id,
                },
            ]
        )

        self.equipment._compute_search_maintenance_plan_count()
        self.assertGreaterEqual(
            self.equipment.search_maintenance_plan_count,
            2,
            "search_maintenance_plan_count should be at least 2 when multiple plans exist",
        )

    def test_search_maintenance_plan_count_with_inactive(self):
        """Test search_maintenance_plan_count includes inactive plans"""
        # Create an inactive plan
        self.MaintenancePlan.create(
            {
                "equipment_id": self.equipment.id,
                "maintenance_kind_id": self.maintenance_kind.id,
                "active": False,
            }
        )
        self.equipment._compute_search_maintenance_plan_count()
        self.assertGreaterEqual(
            self.equipment.search_maintenance_plan_count,
            1,
            "search_maintenance_plan_count should include inactive plans",
        )
