from martini import Martini, DataCube, Source
from martini.beams import GaussianBeam
from martini.noise import GaussianNoise
from martini.spectral_models import GaussianSpectrum
from martini.sph_kernels import WendlandC2
import astropy.units as U
from collections import namedtuple

snap_id = namedtuple('snap_id', ['res', 'phys', 'vol', 'snap'])
mysnap = snap_id(res=3, phys='hydro', vol=1, snap=127)
obj_id = namedtuple('obj_id', ['fof', 'sub'])
myobj = obj_id(fof=1, sub=0)

SO_args = {
    'obj_id': myobj,
    'snap_id': mysnap,
    'mask_type': 'fofsub',
    'mask_args': (myobj, ),
    'mask_kwargs': dict(),
    'configfile': '~/code/simobj/simobj/configs/example.py',
    'simfiles_configfile': '~/code/simfiles/simfiles/configs/example.py',
    'cache_prefix': './',
    'disable_cache': False,
    'ncpu': 0
}

source = Source(
    distance = 3. * U.Mpc,
    rotation = {'L_coords': (60. * U.deg, 0. * U.deg)},
    SO_args = SO_args
)

datacube = DataCube(
    n_px_x = 64,
    n_px_y = 64,
    n_channels = 32,
    px_size = 30. * U.arcsec,
    channel_width = 16. * U.km * U.s ** -1,
    velocity_centre = source.vsys
)

beam = GaussianBeam(
    bmaj = 60. * U.arcsec,
    bmin = 60. * U.arcsec,
    bpa = 0. * U.deg,
    truncate = 4.
)

baselines = None

noise = GaussianNoise(
    rms = 1.E-5 * U.Jy * U.pix ** -2
)

spectral_model = GaussianSpectrum(
    sigma = 7. * U.km * U.s ** -1
)

sph_kernel = WendlandC2()

M = Martini(
    source=source, 
    datacube=datacube, 
    beam=beam,
    baselines=baselines,
    noise=noise,
    spectral_model=spectral_model,
    sph_kernel=sph_kernel
)

M.insert_source_in_cube()
M.add_noise()
M.convolve_beam()
M.write_fits('test')
