from braneworld.engine import BraneworldEngine
from ai.embeddings import hash_embedding
from ai.lora import lora_shapes

def test_engine_pipeline():
    result = BraneworldEngine().run("hello voltron")
    assert result["plan"] and result["result"]

def test_embedding_is_normalized():
    vector = hash_embedding("voltron", 16)
    assert len(vector) == 16
    assert abs(sum(x*x for x in vector) - 1.0) < 1e-5

def test_lora_shapes():
    assert lora_shapes(32, 24, 8) == ((32, 8), (8, 24))
    assert lora_shapes(16, 8, 4, (3, 3)) == ((16, 4, 1, 1), (4, 8, 3, 3))
