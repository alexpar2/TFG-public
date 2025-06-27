# from typing import Optional, Union
# from pydantic import BaseModel, HttpUrl
# from datetime import datetime

# class Emoji(BaseModel):
#     shortcode: str
#     url: HttpUrl
#     static_url: HttpUrl
#     visible_in_picker: bool

# class Field(BaseModel):
#     name: str
#     value: str
#     verified_at: Optional[Union[str, datetime]]

# class Account(BaseModel):
#     id: int
#     username: str
#     acct: str
#     display_name: str
#     locked: bool
#     bot: bool
#     discoverable: bool
#     indexable: bool
#     group: bool
#     created_at: Union[str, datetime]
#     note: str
#     url: HttpUrl
#     uri: HttpUrl
#     avatar: HttpUrl
#     avatar_static: HttpUrl
#     header: HttpUrl
#     header_static: HttpUrl
#     followers_count: int
#     following_count: int
#     statuses_count: int
#     last_status_at: Union[str, datetime]
#     hide_collections: bool
#     emojis: list[Emoji]
#     fields: list[Field]

# class MastodonModel(BaseModel):
#     accounts: list[Account]
