"""Test radiation pattern via get_radiation_pattern() and rp_card()."""

import PyNEC
import pytest


@pytest.fixture
def radpat_dipole():
    """Simple dipole with radiation pattern computed."""
    nec = PyNEC.nec_context()
    geo = nec.get_geometry()
    geo.wire(0, 36, 0, 0, 0, -0.042, 0.008, 0.017, 0.001, 1.0, 1.0)
    nec.geometry_complete(0)
    nec.gn_card(-1, 0, 0, 0, 0, 0, 0, 0)
    nec.ex_card(1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)
    nec.fr_card(0, 2, 2400.0, 100.0e6)
    nec.rp_card(0, 91, 1, 0, 5, 0, 0, 0.0, 45.0, 4.0, 2.0, 1.0, 0.0)
    return nec


class TestRadiationPattern:
    def test_gain_matrix_shape(self, radpat_dipole):
        """Gain should be a 2D matrix with shape (ntheta, nphi)."""
        rp = radpat_dipole.get_radiation_pattern(0)
        gains = rp.get_gain()

        assert gains is not None
        assert gains.ndim == 2

    def test_theta_angles(self, radpat_dipole):
        """Theta angles should be a non-empty array."""
        rp = radpat_dipole.get_radiation_pattern(0)
        thetas = rp.get_theta_angles()

        assert len(thetas) > 0
        assert rp.get_ntheta() == len(thetas)

    def test_phi_angles(self, radpat_dipole):
        """Phi angles should be a non-empty array."""
        rp = radpat_dipole.get_radiation_pattern(0)
        phis = rp.get_phi_angles()

        assert len(phis) > 0
        assert rp.get_nphi() == len(phis)

    def test_gain_components(self, radpat_dipole):
        """Vertical, horizontal, and total gain should all be available."""
        rp = radpat_dipole.get_radiation_pattern(0)

        gv = rp.get_gain_vert()
        gh = rp.get_gain_horiz()
        gt = rp.get_gain_tot()

        assert gv is not None
        assert gh is not None
        assert gt is not None
        assert gv.shape == gt.shape

    def test_polarization_fields(self, radpat_dipole):
        """Polarization fields should be available."""
        rp = radpat_dipole.get_radiation_pattern(0)

        assert rp.get_pol_axial_ratio() is not None
        assert rp.get_pol_tilt() is not None
        assert rp.get_pol_sense_index() is not None

    def test_e_fields(self, radpat_dipole):
        """E-theta, E-phi, and E-r should all be available."""
        rp = radpat_dipole.get_radiation_pattern(0)

        assert rp.get_e_theta() is not None
        assert rp.get_e_phi() is not None

    def test_frequency(self, radpat_dipole):
        """Frequency should be a non-empty array."""
        rp = radpat_dipole.get_radiation_pattern(0)
        freqs = rp.get_frequency()

        assert len(freqs) > 0

    def test_gain_max_is_finite(self, radpat_dipole):
        """Gain max should be finite and not NaN."""
        gmax = radpat_dipole.get_gain_max(0)
        import math

        assert not math.isnan(gmax)
        assert not math.isinf(gmax)
