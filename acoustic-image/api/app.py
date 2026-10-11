"""API local (FastAPI) para simular el envío/recepción de paquetes acústicos."""
from __future__ import annotations

import base64
import io

from fastapi import FastAPI, HTTPException
from PIL import Image
from pydantic import BaseModel

from audio_protocol import bursts as B
from database.models import Layer, Transmission, open_db, pair_of_color
from decoder.reconstruct import reconstruct
from encoder.peeling import compress


class SendIn(BaseModel):
    image_b64: str            # PNG/JPEG en base64
    name: str = ""
    max_layers: int = 64
    tol: int = 1


def create_app(db_url: str = "sqlite://") -> FastAPI:
    app, Session = FastAPI(title="acoustic-image"), open_db(db_url)

    @app.post("/send")
    def send(req: SendIn):
        try:
            img = Image.open(io.BytesIO(base64.b64decode(req.image_b64)))
            stream, info = compress(img, tol=req.tol, max_layers=req.max_layers)
            bursts = B.encode(stream)
        except Exception as e:
            raise HTTPException(400, str(e))
        with Session.begin() as db:
            t = Transmission(name=req.name, width=img.width, height=img.height, bursts=bursts, stream=stream)
            for i, l in enumerate(info["layers"]):
                rgb = int.from_bytes(bytes(l["rgb"]), "big")
                a, b = pair_of_color(rgb)
                t.layers.append(Layer(idx=i, rgb=rgb, pair_a=a, pair_b=b, pixels=l["pixels"]))
            db.add(t)
            db.flush()
            tid = t.id
        return {"id": tid, "bursts": len(bursts), "stream_bytes": len(stream), "raw_bytes": info["raw_bytes"],
                "gradient_blocks": info["gradient_blocks"], "layers": len(info["layers"])}

    @app.get("/packets/{tid}")
    def packets(tid: int):
        with Session() as db:
            t = db.get(Transmission, tid)
            if not t:
                raise HTTPException(404, "transmisión no encontrada")
            return {"id": tid, "bursts": t.bursts}

    @app.post("/receive")
    def receive(body: dict):
        try:
            img = reconstruct(B.decode(body["bursts"]))
        except Exception as e:
            raise HTTPException(422, str(e))
        buf = io.BytesIO()
        img.save(buf, "PNG")
        return {"width": img.width, "height": img.height, "image_b64": base64.b64encode(buf.getvalue()).decode()}

    return app


app = create_app()
