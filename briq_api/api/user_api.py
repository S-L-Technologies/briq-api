import io
import logging
import base64

from PIL import Image

from briq_api.set_identifier import SetRID
from briq_api.indexer.storage import mongo_storage
from briq_api.stores import genesis_storage, theme_storage

from briq_api.mesh.briq import BriqData

logger = logging.getLogger(__name__)


async def get_user_items(chain_id: str, user_id: str):
    boxes = await mongo_storage.get_user_nfts(chain_id, user_id, 'box')
    booklets = await mongo_storage.get_user_nfts(chain_id, user_id, 'booklet')
    sets = await mongo_storage.get_user_nfts(chain_id, user_id, 'set')
    return {
        "box_token_ids": [genesis_storage.get_box_id(chain_id, box) for box in boxes.nfts],
        "booklets": [theme_storage.get_booklet_id_from_token_id(chain_id, booklet) for booklet in booklets.nfts],
        "sets": sets.nfts,
        "last_block": max(boxes.last_block, booklets.last_block, sets.last_block),
    }


async def get_user_briqs(chain_id: str, user_id: str):
    briqs = await mongo_storage.get_user_briqs(chain_id, user_id)
    ret = {'last_block': 0}
    for briq in briqs:
        # TODO: acknowledge NFTS here
        ret['last_block'] = max(ret['last_block'], briq['updated_block'])
        material = hex(int.from_bytes(briq['token_id'], "big"))
        quantity = int.from_bytes(briq['quantity'], "big")
        ret[material] = {
            'ft_balance': quantity,
            'nft_ids': []
        }
    return ret
