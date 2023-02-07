import pytest
import numpy as np
from astropy import units as U
from martini.martini import Martini
from martini.datacube import DataCube
from martini.beams import GaussianBeam
from martini.noise import GaussianNoise
from martini.sources import _SingleParticleSource, SPHSource
from martini.spectral_models import GaussianSpectrum
from martini.sph_kernels import GaussianKernel

GaussianKernel.noFWHMwarn = True


@pytest.fixture(scope="function")
def m():

    source = _SingleParticleSource()
    datacube = DataCube(
        n_px_x=16,
        n_px_y=16,
        n_channels=16,
        velocity_centre=source.distance * 70 * U.km / U.s / U.Mpc,
    )
    beam = GaussianBeam()
    noise = GaussianNoise(rms=1.0e-9 * U.Jy * U.arcsec**-2)
    sph_kernel = GaussianKernel()
    spectral_model = GaussianSpectrum()

    M = Martini(
        source=source,
        datacube=datacube,
        beam=beam,
        noise=noise,
        sph_kernel=sph_kernel,
        spectral_model=spectral_model,
    )
    M.insert_source_in_cube()
    M.add_noise()
    M.convolve_beam()
    yield M


@pytest.fixture(scope="function")
def m_nn():

    source = _SingleParticleSource()
    datacube = DataCube(
        n_px_x=16,
        n_px_y=16,
        n_channels=16,
        velocity_centre=source.distance * 70 * U.km / U.s / U.Mpc,
    )
    beam = GaussianBeam()
    noise = None
    sph_kernel = GaussianKernel()
    spectral_model = GaussianSpectrum()

    M = Martini(
        source=source,
        datacube=datacube,
        beam=beam,
        noise=noise,
        sph_kernel=sph_kernel,
        spectral_model=spectral_model,
    )
    M.insert_source_in_cube()
    M.convolve_beam()
    yield M


@pytest.fixture(scope="function")
def dc():

    dc = DataCube(
        n_px_x=16,
        n_px_y=16,
        n_channels=32,
    )

    dc._array[...] = (
        np.random.rand(dc._array.size).reshape(dc._array.shape) * dc._array.unit
    )

    yield dc


@pytest.fixture(scope="function")
def s():

    n_g = 1000
    phi = np.random.rand(n_g, 1) * 2 * np.pi
    R = np.random.rand(n_g, 1)
    xyz_g = np.hstack(
        (
            R * np.cos(phi) * 0.01,
            R * np.sin(phi) * 0.01,
            (np.random.rand(n_g, 1) * 2 - 1) * 0.001,  # 1 kpc height
        )
    )
    vxyz_g = (
        np.hstack(
            (
                # solid body, 100 km/s at edge
                R * np.sin(phi) * 100,
                R * np.cos(phi) * 100,
                np.random.rand(n_g, 1) * 20 - 10,  # 10 km/s vertical
            )
        )
        * U.km
        / U.s
    )
    T_g = np.ones(n_g) * 1e4 * U.K
    mHI_g = np.ones(n_g) * 1e9 * U.Msun / n_g
    hsm_g = 0.5 * U.kpc
    particles = dict(
        xyz_g=xyz_g,
        vxyz_g=vxyz_g,
        mHI_g=mHI_g,
        T_g=T_g,
        hsm_g=hsm_g,
    )
    s = SPHSource(**particles)

    yield s
