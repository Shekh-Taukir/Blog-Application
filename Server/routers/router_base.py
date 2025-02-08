from typing import Optional
from fastapi import APIRouter


def of_result_message(
    ab_success: bool,
    as_message: Optional[str] = None,
    alt_result=None,
    ab_added: Optional[bool] = False,
):
    ld_return = {}

    ld_return["Success"] = ab_success

    if as_message:
        ld_return["Message"] = as_message

    if alt_result:
        ld_return["result"] = alt_result

        # if function is called from new data addition function,
        # then len() function not works for individual entity,
        # i.e len(new_blog)
        # if not ab_added:
        #     ld_return["no_of_entries"] = len(alt_result)

    return ld_return


def of_init_router(as_prefix: str, alt_tags: list):
    au_router = APIRouter(
        # (Feb 02, 2025 Taukir Python Project) eg, of initialization of a router
        # prefix="/blogs",
        # tags=["Blog"],
        prefix=as_prefix,
        tags=alt_tags,
    )
