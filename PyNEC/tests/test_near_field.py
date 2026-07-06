# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)
"""Test near-field patterns via ne_card(), nh_card(), get_near_field_pattern()."""

import PyNEC
import pytest


@pytest.fixture
def dipole_near_field():
    """Simple dipole with near electric and magnetic field cards."""
    nec = PyNEC.nec_context()
    geo = nec.get_geometry()
    geo.wire(1, 21, 0, -0.25, 0.0, 0, 0.25, 0.0, 0.001, 1, 1)
    nec.geometry_complete(0)
    nec.ex_card(0, 1, 11, 0, 0, 1, 0, 0, 0, 0, 0)
    nec.pq_card(0, 0, 0, 0)
    nec.ne_card(0, 1, 20, 20, 0, 0.05, 0.05, 0, 0.05, 0.05)
    nec.nh_card(0, 1, 20, 20, 0, 0.05, 0.05, 0, 0.05, 0.05)
    nec.rp_card(0, 19, 36, 1, 0, 0, 0, 0, 0, 10, 10, 0, 0)
    return nec


class TestNearField:
    def test_electric_field_not_none(self, dipole_near_field):
        """Near electric field should be retrievable at index 0."""
        ne = dipole_near_field.get_near_field_pattern(0)
        assert ne is not None

    def test_magnetic_field_not_none(self, dipole_near_field):
        """Near magnetic field should be retrievable at index 1."""
        nh = dipole_near_field.get_near_field_pattern(1)
        assert nh is not None

    def test_electric_field_frequency(self, dipole_near_field):
        """Frequency should be non-empty."""
        ne = dipole_near_field.get_near_field_pattern(0)
        freqs = ne.get_frequency()
        assert len(freqs) > 0

    def test_electric_field_coordinates(self, dipole_near_field):
        """X, Y, Z coordinate arrays should be non-empty."""
        ne = dipole_near_field.get_near_field_pattern(0)
        assert len(ne.get_x()) > 0
        assert len(ne.get_y()) > 0
        assert len(ne.get_z()) > 0

    def test_electric_field_components(self, dipole_near_field):
        """Field X, Y, Z components should be non-empty complex arrays."""
        ne = dipole_near_field.get_near_field_pattern(0)
        fx = ne.get_field_x()
        fy = ne.get_field_y()
        fz = ne.get_field_z()
        assert len(fx) > 0
        assert len(fy) > 0
        assert len(fz) > 0

    def test_nfeh_flag(self, dipole_near_field):
        """NFEH flag should indicate electric or magnetic."""
        ne = dipole_near_field.get_near_field_pattern(0)
        nh = dipole_near_field.get_near_field_pattern(1)
        # nfeh=0 or 1 (0=electric, 1=magnetic) for the whole pattern
        assert ne.get_nfeh() in (0, 1)
        assert nh.get_nfeh() in (0, 1)

    def test_both_field_types_different_flags(self, dipole_near_field):
        """Electric and magnetic should have different NFEH flags."""
        ne = dipole_near_field.get_near_field_pattern(0)
        nh = dipole_near_field.get_near_field_pattern(1)
        assert ne.get_nfeh() != nh.get_nfeh()
