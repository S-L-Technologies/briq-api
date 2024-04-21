import io
import json
import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.responses import StreamingResponse, JSONResponse

from briq_api.set_identifier import SetRID
from briq_api.storage.file.backends.cloud_storage import NotFoundException
from briq_api.indexer.storage import mongo_storage

from .common import ExceptionWrapperRoute

from .. import api

logger = logging.getLogger(__name__)

router = APIRouter(route_class=ExceptionWrapperRoute(logger))

hidden_sets = {
    hex(3237257010082882961400056035578317339222271916371075326396818103833724977152),
    hex(2489739008863561988083186495972912854981196782375410526076829889144545083392),
    hex(842526709234298077544294311480747113148708646056843575885085464101969199104),
    hex(2224665168682032383546486112244211137116359398460551383628278093314451832832)
}


@router.head("/metadata/{chain_id}/{token_id}")
@router.head("/metadata/{chain_id}/{token_id}.json")
@router.get("/metadata/{chain_id}/{token_id}")
@router.get("/metadata/{chain_id}/{token_id}.json")
async def metadata(chain_id: str, token_id: str):
    if token_id in hidden_sets:
        raise HTTPException(status_code=404, detail="Not found")

    rid = SetRID(chain_id=chain_id, token_id=token_id)

    output = await api.get_metadata(rid)
    # Don't cache data if the set has no creation date, which means we haven't indexed it yet.
    cache_time = (24 * 3600) if output['created_at'] != -1 else 10

    # Stream the data because files can get fairly hefty.
    out = io.StringIO()
    json.dump(output, out)
    out.seek(0)
    return StreamingResponse(out, media_type="application/json", headers={
        "Cache-Control": f"public,max-age={cache_time}"
    })


@router.head("/preview/{chain_id}/{token_id}")
@router.head("/preview/{chain_id}/{token_id}.png")
@router.get("/preview/{chain_id}/{token_id}")
@router.get("/preview/{chain_id}/{token_id}.png")
async def preview(chain_id: str, token_id: str):
    if token_id in hidden_sets:
        raise HTTPException(status_code=404, detail="Not found")

    rid = SetRID(chain_id=chain_id, token_id=token_id)

    preview = api.get_preview(rid)

    return StreamingResponse(io.BytesIO(preview), media_type="image/png", headers={
        "Cache-Control": f"public,max-age={3600 * 24}"
    })


@router.head("/set/{chain_id}/{token_id}/small_preview.jpg")
@router.get("/set/{chain_id}/{token_id}/small_preview.jpg")
async def get_small_preview(chain_id: str, token_id: str):
    if token_id in hidden_sets:
        raise HTTPException(status_code=404, detail="Not found")

    rid = SetRID(chain_id=chain_id, token_id=token_id)

    preview = api.get_small_preview(rid)

    return StreamingResponse(io.BytesIO(preview), media_type="image/png", headers={
        "Cache-Control": f"public,max-age={3600 * 24}"
    })


@router.head("/model/{chain_id}/{token_id}.{kind}")
@router.get("/model/{chain_id}/{token_id}.{kind}")
async def model(chain_id: str, token_id: str, kind: str):
    if token_id in hidden_sets:
        raise HTTPException(status_code=404, detail="Not found")

    mime_type = {
        "gltf": "model/gltf-binary",
        "glb": "model/gltf-binary",
        "vox": "application/octet-stream",
    }
    if kind not in mime_type:
        raise HTTPException(status_code=400, detail=f"Model kind {kind} is not supported")

    rid = SetRID(chain_id=chain_id, token_id=token_id)
    try:
        data = api.get_model(rid, kind)
    except (NotFoundException, OSError):
        metadata = await api.get_metadata(rid)
        data = api.create_model(metadata, kind)
        api.store_model(rid, kind, data)
        logger.info("Created %(type)s model for %(rid)s on the fly.", {"type": kind, "rid": rid.json()})

    return StreamingResponse(io.BytesIO(data), media_type=mime_type[kind], headers={
        "Cache-Control": f"public,max-age={3600 * 24}"
    })

@router.head("/{chain_id}/gallery/static_data")
@router.get("/{chain_id}/gallery/static_data")
async def get_gallery_data(chain_id: str):
    sets = mongo_storage.get_backend(chain_id).async_db['set_tokens'].find({}).sort("_timestamp", -1).limit(25)
    
    result = {}
    for token_id in sets:
        rid = SetRID(chain_id=chain_id, token_id=token_id)
        set_data = await api.get_metadata(rid)
        result[token_id] = {
            x: set_data[x] for x in ['id', 'name', 'description', 'image', 'created_at', 'booklet_id', 'background_color'] if x in set_data
        }
        
    return JSONResponse(result, headers={
        "Cache-Control": f"public,max-age={24 * 3600}"
    })
    

class StoreSetRequest(BaseModel):
    chain_id: str
    token_id: str
    data: dict[str, Any]
    image_base64: bytes
    owner: str


@router.post("/store_set")
async def store_set(set: StoreSetRequest):
    # Ensure compliance of the metadata with ERC 721
    set.data["image"] = f"https://api.briq.construction/v1/preview/{set.chain_id}/{set.token_id}.png"
    # Default to showing the GLB version of the mesh.
    set.data["animation_url"] = f"https://api.briq.construction/v1/model/{set.chain_id}/{set.token_id}.glb"

    # Point to the builder.
    set.data["external_url"] = f"https://briq.construction/set/{set.chain_id}/{set.token_id}"

    rid = SetRID(chain_id=set.chain_id, token_id=set.token_id)

    await api.store_set(rid, set.data, set.image_base64)

    logger.info("Stored new set %(rid)s for %(owner)s", {
        "rid": rid.json(),
        "owner": set.owner
    })
