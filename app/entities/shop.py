from app.common.shop_status import ShopStatusEnum


class Shop:
    def __init__(
        self,
        shop_id: str,
        name: str,
        email: str,
        password: str,
        status: str = ShopStatusEnum.ACTIVE,
        verify: bool = False,
        roles: list = [],
    ):
        self.shop_id = shop_id
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.verify = verify
        self.roles = roles
