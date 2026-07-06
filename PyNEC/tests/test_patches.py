# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)
"""Test surface patch geometry and results."""

import PyNEC
import pytest


@pytest.fixture
def cylinder_with_patches():
    """Cylinder with attached wires, multiple surface patches."""
    nec = PyNEC.nec_context()
    geo = nec.get_geometry()
    geo.arbitrary_shaped_patch(10, 0, 7.3333, 0.0, 0.0, 38.4)
    geo.arbitrary_shaped_patch(10, 0, 0, 0.0, 0.0, 38.4)
    geo.arbitrary_shaped_patch(10, 0, -7.3333, 0.0, 0.0, 38.4)
    geo.move(0, 0, 30, 0, 0, 0, 0, 1, 0)
    geo.arbitrary_shaped_patch(6.89, 0.0, 11.0, 90.0, 0.0, 44.88)
    geo.arbitrary_shaped_patch(6.89, 0.0, -11.0, -90.0, 0.0, 44.88)
    geo.generate_cylindrical_structure(0, 6)
    geo.arbitrary_shaped_patch(0, 0, 11, 90, 0, 44.89)
    geo.arbitrary_shaped_patch(0, 0, -11, -90, 0, 44.89)
    geo.wire(1, 4, 0, 0, 11, 0, 0, 23, 0.1, 1, 1)
    geo.wire(2, 5, 10, 0, 0, 27.6, 0, 0, 0.2, 1, 1)
    geo.scale(0.01)
    nec.geometry_complete(0)
    nec.fr_card(0, 1, 465.84e6, 0)
    nec.ex_card(0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0)
    nec.rp_card(0, 73, 1, 1, 0, 0, 0, 0, 0, 5, 0, 0, 0)
    nec.ex_card(0, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0)
    nec.xq_card(0)
    return nec


class TestPatches:
    def test_structure_currents_not_none(self, cylinder_with_patches):
        """Structure currents should be retrievable for patch model."""
        sc = cylinder_with_patches.get_structure_currents(0)
        assert sc is not None

    def test_patch_info(self, cylinder_with_patches):
        """Patch number, center, and tangent vectors should be available."""
        sc = cylinder_with_patches.get_structure_currents(0)
        # Patches produce patch-specific current data
        assert len(sc.get_patch_number()) > 0
        assert len(sc.get_patch_center_x()) > 0

    def test_patch_tangent_vectors(self, cylinder_with_patches):
        """Patch tangent vectors should be complex arrays."""
        sc = cylinder_with_patches.get_structure_currents(0)
        tv1 = sc.get_patch_tangent_vector1()
        tv2 = sc.get_patch_tangent_vector2()
        assert len(tv1) > 0
        assert len(tv2) > 0

    def test_patch_e_fields(self, cylinder_with_patches):
        """Patch E-field components should be available."""
        sc = cylinder_with_patches.get_structure_currents(0)
        assert len(sc.get_patch_e_x()) > 0
        assert len(sc.get_patch_e_y()) > 0
        assert len(sc.get_patch_e_z()) > 0

    def test_impedance_finite(self, cylinder_with_patches):
        """Impedance should be finite."""
        ipt = cylinder_with_patches.get_input_parameters(0)
        z = ipt.get_impedance()
        assert len(z) > 0
        for val in z:
            assert abs(val.real) < 1e6
            assert abs(val.imag) < 1e6
