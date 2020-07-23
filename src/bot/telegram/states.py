from aiogram.dispatcher.filters.state import State, StatesGroup


# States
class User(StatesGroup):
    ChooseLanguage = State()
    MainMenu = State()
    Category = State()
    Product = State()
    ProductMenu = State()
    Quantity = State()
    Cart = State()
    Edit = State()
    EditQuantity = State()
    Phone = State()
    RealName = State()
    Delivery = State()
    Location = State()
    Time = State()
    TimeSet = State()
    OrderAccept = State()
    PaymentType = State()
    PaySystemChoose = State()
    OrderEdit = State()
    TimeEdit = State()
    TimeSetEdit = State()
    DeliveryEdit = State()
    LocationEdit = State()
    PaymentTypeEdit = State()
    PaySystemChooseEdit = State()
    OrderCartEdit = State()
    OrderEditQuantity = State()
    PreCheckout = State()
    SuccessfulPayment = State()
    SetBranch = State()
    EditBranch = State()
    NewsShow = State()
    Events = State()
    EventsShow = State()
