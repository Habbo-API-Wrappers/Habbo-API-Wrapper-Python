from __future__ import annotations


def sanitise_furni_id(furni_id: int) -> int:
    if furni_id < 0:
        furni_id *= -1
    if furni_id >= 2147418112:
        furni_id -= 2147418112
    return furni_id
