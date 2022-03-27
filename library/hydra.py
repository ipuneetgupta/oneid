from hydra import Hydra
from decouple import config


def create_hydra():
    return Hydra(
        publichost=config('PUBLIC_HYDRA_URL'),
        adminhost=config('ADMIN_HYDRA_URL'),
        client=config('AUTH_CLIENT_ID'),
        secret=config('AUTH_CLIENT_SECRET')
    )
