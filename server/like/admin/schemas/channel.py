from pydantic import BaseModel, Field
from typing_extensions import Literal


class ChannelOaIn(BaseModel):
    """
    公众号渠道参数
    """
    name: str = Field(default='', max_length=100)  # 小程序名称
    primary_id: str = Field(default='', alias='primaryId', max_length=100)  # 原始ID
    app_id: str = Field(default='', alias='appId', max_length=100)  # appId
    app_secret: str = Field(default='', alias='appSecret', max_length=200)  # appSecret
    qr_code: str = Field(default='', alias='qrCode', max_length=300)  # 小程序码
    url: str = Field(default='', max_length=300)  # URL
    token: str = Field(default='', max_length=200)  # Token
    encoding_aes_key: str = Field(default='', alias='encodingAesKey', max_length=43)  # EncodingAESKey
    encryption_type: Literal[1, 2, 3] = Field(default=1, alias='encryptionType')  # EncryptionType
