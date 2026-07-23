# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)
"""Test normalized receiving pattern via get_norm_rx_pattern()."""

import PyNEC
import pytest


@pytest.fixture
def rx_antenna():
    """Vertical half-wave over imperfect ground, receiving pattern."""
    nec = PyNEC.nec_context()
    geo = nec.get_geometry()
    geo.wire(0, 9, 0, 0, 2, 0, 0, 7, 0.3, 1, 1)
    nec.geometry_complete(0)
    nec.set_extended_thin_wire_kernel(True)
    nec.fr_card(0, 1, 30.0, 0)
    nec.gn_card(0, 0, 6.0, 0.001, 0, 0, 0, 0)
    nec.ex_card(1, 10, 3, 0, 0, 0, 0, 0, 10, 20, 0)
    nec.pt_card(2, 0, 5, 5)
    nec.xq_card(0)
    return nec


class TestNormRxPattern:
    def test_pattern_not_none(self, rx_antenna):
        """Normalized RX pattern should be retrievable."""
        nrp = rx_antenna.get_norm_rx_pattern(0)
        assert nrp is not None

    def test_frequency(self, rx_antenna):
        nrp = rx_antenna.get_norm_rx_pattern(0)
        # necpp returns the result's frequency as a scalar (Hz).
        freq = nrp.get_frequency()
        assert freq > 0

    def test_theta_phi_counts(self, rx_antenna):
        """N_theta and N_phi should be non-negative."""
        nrp = rx_antenna.get_norm_rx_pattern(0)
        assert nrp.get_n_theta() >= 0
        assert nrp.get_n_phi() >= 0

    def test_angle_ranges(self, rx_antenna):
        """Theta/phi start and delta should be finite."""
        nrp = rx_antenna.get_norm_rx_pattern(0)
        assert nrp.get_theta_start() is not None
        assert nrp.get_phi_start() is not None
        assert nrp.get_delta_theta() is not None
        assert nrp.get_delta_phi() is not None

    def test_eta_and_axial_ratio(self, rx_antenna):
        """Eta and axial ratio should be non-empty."""
        nrp = rx_antenna.get_norm_rx_pattern(0)
        assert nrp.get_eta() is not None
        assert nrp.get_axial_ratio() is not None

    def test_segment_number(self, rx_antenna):
        """Segment number should be set (scalar)."""
        nrp = rx_antenna.get_norm_rx_pattern(0)
        # necpp returns the segment number as a scalar int.
        assert nrp.get_segment_number() > 0

    def test_magnitude(self, rx_antenna):
        """Magnitude should be non-empty."""
        nrp = rx_antenna.get_norm_rx_pattern(0)
        mag = nrp.get_mag()
        assert mag is not None
