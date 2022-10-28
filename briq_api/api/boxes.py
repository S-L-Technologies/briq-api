from dataclasses import dataclass
from itertools import chain
import logging
from briq_api.storage.file.backends.file_storage import FileStorage
import time

from briq_api.storage.multi_backend_client import StorageClient
from briq_api.stores import genesis_storage, file_storage
from briq_api.indexer.storage import mongo_storage

logger = logging.getLogger(__name__)


@dataclass
class BoxRID:
    chain_id: str  # NB: this is not the same as the 'chain ID', since we'll plan ahead for cross-chain support.
    theme_id: str
    box_id: str


class BoxStorage:
    storage: StorageClient
    cache: FileStorage
    PREFIX = "genesis_themes"

    def __init__(self, storage: StorageClient) -> None:
        self.storage = storage
        self.cache = {}

    def box_path(self, rid: BoxRID):
        return f"{BoxStorage.PREFIX}/{rid.theme_id}/{rid.box_id}"

    def load_metadata_box(self, rid: BoxRID):
        return self.storage.get_backend(rid.chain_id).load_json(f"{self.box_path(rid)}/metadata_box.json")

    def load_metadata_booklet(self, rid: BoxRID):
        return self.storage.get_backend(rid.chain_id).load_json(f"{self.box_path(rid)}/metadata_booklet.json")

    def step_image_path(self, rid: BoxRID, step: int):
        return f"{self.box_path(rid)}/step_{step}.png"

    def load_box_file(self, rid: BoxRID, file: str):
        return self.storage.get_backend(rid.chain_id).load_bytes(f"{self.box_path(rid)}/{file}")

    def load_step_image(self, rid: BoxRID, step: int):
        return self.storage.get_backend(rid.chain_id).load_bytes(self.step_image_path(rid, step))

    def load_cover_item(self, rid: BoxRID):
        return self.storage.get_backend(rid.chain_id).load_bytes(f"{self.box_path(rid)}/cover.png")

    def load_cover_booklet(self, rid: BoxRID):
        return self.storage.get_backend(rid.chain_id).load_bytes(f"{self.box_path(rid)}/booklet_cover.png")

    def load_cover_box(self, rid: BoxRID):
        return self.storage.get_backend(rid.chain_id).load_bytes(f"{self.box_path(rid)}/box_cover.png")

    def load_box_texture(self, rid: BoxRID):
        return self.storage.get_backend(rid.chain_id).load_bytes(f"{self.box_path(rid)}/box_tex.png")

    def load_booklet_texture(self, rid: BoxRID):
        return self.storage.get_backend(rid.chain_id).load_bytes(f"{self.box_path(rid)}/booklet_cover_tex.png")

    # Themes

    def list_themes(self, chain_id: str):
        return self.storage.get_backend(chain_id).list_paths(f"{BoxStorage.PREFIX}/")

    def list_boxes_of_theme(self, chain_id: str, theme_id: str):
        return [x for x in self.storage.get_backend(chain_id).list_paths(f"{BoxStorage.PREFIX}/{theme_id}/") if not ('.' in x)]

    def get_theme_data(self, chain_id: str, theme_id: str):
        return self.storage.get_backend(chain_id).load_json(f"{BoxStorage.PREFIX}/{theme_id}/data.json")

    def theme_cover_prelaunch(self, chain_id: str, theme_id: str):
        try:
            return self.cache[f'{chain_id}_{theme_id}_cover_prelaunch']
        except Exception:
            data = self.storage.get_backend(chain_id).load_bytes(f"{BoxStorage.PREFIX}/{theme_id}/cover_prelaunch.jpg")
            self.cache[f'{chain_id}_{theme_id}_cover_prelaunch'] = data
            return data

    def theme_cover_postlaunch(self, chain_id: str, theme_id: str):
        try:
            return self.cache[f'{chain_id}_{theme_id}_cover_postlaunch']
        except Exception:
            data = self.storage.get_backend(chain_id).load_bytes(f"{BoxStorage.PREFIX}/{theme_id}/cover_postlaunch.jpg")
            self.cache[f'{chain_id}_{theme_id}_cover_postlaunch'] = data
            return data

    def theme_logo(self, chain_id: str, theme_id: str):
        try:
            return self.cache[f'{chain_id}_{theme_id}_logo']
        except Exception:
            data = self.storage.get_backend(chain_id).load_bytes(f"{BoxStorage.PREFIX}/{theme_id}/logo.png")
            self.cache[f'{chain_id}_{theme_id}_logo'] = data
            return data

    def theme_splash(self, chain_id: str, theme_id: str):
        try:
            return self.cache[f'{chain_id}_{theme_id}_splash']
        except Exception:
            data = self.storage.get_backend(chain_id).load_bytes(f"{BoxStorage.PREFIX}/{theme_id}/splash.jpg")
            self.cache[f'{chain_id}_{theme_id}_splash'] = data
            return data


box_storage = BoxStorage(file_storage)


def get_box_metadata(rid: BoxRID):
    metadata = box_storage.load_metadata_box(rid)
    metadata['token_id'] = genesis_storage.get_box_token_id(rid.chain_id, f'{rid.theme_id}/{rid.box_id}')
    metadata['auction_id'] = genesis_storage.get_auction_id(rid.chain_id, f'{rid.theme_id}/{rid.box_id}')
    return metadata


def get_booklet_metadata(rid: BoxRID):
    metadata = box_storage.load_metadata_booklet(rid)
    metadata['token_id'] = genesis_storage.get_booklet_token_id(rid.chain_id, f'{rid.theme_id}/{rid.box_id}')
    # Parse the number because javascript can't
    metadata['serial_number'] = (int(metadata['token_id']) - (int(metadata['token_id']) & (2**192 - 1))) / 2**192
    metadata['auction_id'] = genesis_storage.get_auction_id(rid.chain_id, f'{rid.theme_id}/{rid.box_id}')
    return metadata


def get_box_saledata(rid: BoxRID):
    auction_data = genesis_storage.get_auction_static_data(rid.chain_id, f'{rid.theme_id}/{rid.box_id}')
    box_token_id = genesis_storage.get_box_token_id(rid.chain_id, f'{rid.theme_id}/{rid.box_id}')
    auction_data['quantity_left'] = mongo_storage.get_available_boxes(rid.chain_id, box_token_id)
    # temp hack
    import time
    if 'ongoing' in rid.theme_id:
        if 'base' in rid.box_id:
            auction_data['auction_start'] = time.time() + 60
        else:
            auction_data['auction_start'] = time.time() - 60
    else:
        auction_data['auction_start'] = time.time() + 24 * 60 * 60 * 10
    return auction_data


def get_box_transfer(rid: BoxRID, tx_hash: str):
    box_token_id = genesis_storage.get_box_token_id(rid.chain_id, f'{rid.theme_id}/{rid.box_id}')
    return mongo_storage.get_transfer(rid.chain_id, 'box', tx_hash, box_token_id)


def list_themes(chain_id: str):
    return box_storage.list_themes(chain_id)


def list_boxes_of_theme(chain_id: str, theme_id: str):
    data = get_theme_data(chain_id, theme_id)
    if data['sale_start'] is None or data['sale_start'] > time.time():
        return []
    return [f"{theme_id}/{box}" for box in box_storage.list_boxes_of_theme(chain_id, theme_id)]


def get_theme_data(chain_id: str, theme_id: str):
    data = box_storage.get_theme_data(chain_id, theme_id)
    data['sale_start'] = time.time() - 60 if 'ongoing' in theme_id else None
    return data


def get_box_step_image(rid: BoxRID, step: int):
    return box_storage.load_step_image(rid, step)


def get_box_cover_item(rid: BoxRID):
    return box_storage.load_cover_item(rid)


def get_box_cover_booklet(rid: BoxRID):
    return box_storage.load_cover_booklet(rid)


def get_box_cover_box(rid: BoxRID):
    return box_storage.load_cover_box(rid)


def get_box_texture(rid: BoxRID):
    return box_storage.load_box_texture(rid)


def get_booklet_texture(rid: BoxRID):
    return box_storage.load_booklet_texture(rid)


def get_booklet_step_glb(rid: BoxRID, step: int):
    return [
        box_storage.load_box_file(rid, f'step_{step}.glb'),
        box_storage.load_box_file(rid, f'step_level_{step}.glb')
    ]