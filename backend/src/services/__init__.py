from .services import (
    MakersService,
    BrandsService,
    TypeDecorsService,
    TypePlatesService,

    FormatsService,

    DecorsService,
    PlatesService,

    MaterialsService,

    PricesService
)

from .auth import (
    AuthService,
    get_current_user
)

from .permissions import (
    allow_create_new_user,
    allow_create_items,
    allow_get_items,
    allow_update_items,
    allow_delete_items
)

from .reports import (
    ReportsService
)