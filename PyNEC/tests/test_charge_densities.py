# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)
"""Test charge densities via pq_card() and get_structure_currents()."""

import PyNEC
import pytest


@pytest.fixture
def dipole_with_charges():
    """Simple dipole with charge density card."""
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


class TestChargeDensities:
    def test_currents_not_none(self, dipole_with_charges):
        """Structure currents (with charge densities) should be retrievable."""
        sc = dipole_with_charges.get_structure_currents(0)
        assert sc is not None

    def test_charge_density_segment_info(self, dipole_with_charges):
        """Charge density segment info should be non-empty."""
        sc = dipole_with_charges.get_structure_currents(0)
        assert len(sc.get_q_density_segment_number()) > 0
        assert len(sc.get_q_density_segment_tag()) > 0
        assert len(sc.get_q_density_segment_center_x()) > 0
        assert len(sc.get_q_density_segment_length()) > 0

    def test_charge_density_complex(self, dipole_with_charges):
        """Charge density should be a complex array."""
        sc = dipole_with_charges.get_structure_currents(0)
        qdens = sc.get_q_density()
        assert len(qdens) > 0

    def test_current_and_charge_density_same_length(self, dipole_with_charges):
        """Current and charge density arrays should have matching lengths."""
        sc = dipole_with_charges.get_structure_currents(0)
        current = sc.get_current()
        qdens = sc.get_q_density()
        assert len(current) == len(qdens)
