# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)
"""Test structure currents via get_structure_currents()."""

import PyNEC
import pytest


@pytest.fixture
def dipole_with_currents():
    """Half-wavelength vertical dipole over ground with structure currents."""
    nec = PyNEC.nec_context()
    geo = nec.get_geometry()
    geo.wire(0, 9, 0, 0, 2, 0, 0, 7, 0.3, 1, 1)
    nec.geometry_complete(0)
    nec.set_extended_thin_wire_kernel(True)
    nec.pt_card(0, 0, 3, 4)
    nec.ld_card(0, 0, 0, 0, 1000, 1, 1)
    nec.fr_card(0, 1, 30e6, 0)
    nec.ex_card(0, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0)
    nec.gn_card(1, 0, 0, 0, 0, 0, 0, 0)
    nec.rp_card(0, 10, 2, 1, 3, 0, 1, 0, 0, 10.0, 90.0, 0.0, 0.0)
    return nec


class TestStructureCurrents:
    def test_currents_not_none(self, dipole_with_currents):
        """Structure currents should be retrievable."""
        sc = dipole_with_currents.get_structure_currents(0)
        assert sc is not None

    def test_frequency(self, dipole_with_currents):
        """Frequency should be non-empty."""
        sc = dipole_with_currents.get_structure_currents(0)
        freqs = sc.get_frequency()
        assert len(freqs) > 0

    def test_segment_info(self, dipole_with_currents):
        """Segment number, tag, center, length should be non-empty."""
        sc = dipole_with_currents.get_structure_currents(0)

        assert len(sc.get_current_segment_number()) > 0
        assert len(sc.get_current_segment_tag()) > 0
        assert len(sc.get_current_segment_center_x()) > 0
        assert len(sc.get_current_segment_length()) > 0

    def test_current_complex(self, dipole_with_currents):
        """Current should be a complex array."""
        sc = dipole_with_currents.get_structure_currents(0)
        curr = sc.get_current()
        assert len(curr) > 0

    def test_current_theta_phi(self, dipole_with_currents):
        """Theta and phi components should be non-empty."""
        sc = dipole_with_currents.get_structure_currents(0)
        assert len(sc.get_current_theta()) > 0
        assert len(sc.get_current_phi()) > 0

    def test_n_m_counts(self, dipole_with_currents):
        """N and M counts should be non-negative."""
        sc = dipole_with_currents.get_structure_currents(0)
        assert sc.get_n() >= 0
        assert sc.get_m() >= 0

    def test_ipt_flags(self, dipole_with_currents):
        """IPT flags should be valid."""
        sc = dipole_with_currents.get_structure_currents(0)
        # iptflg and iptflq are print flags, should be >= 0
        assert sc.get_iptflg() >= 0
        assert sc.get_iptflq() >= 0
