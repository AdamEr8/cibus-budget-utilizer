from abc import ABC, abstractmethod

class AbstractOrderController(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def login(self) -> None:
        pass
    
    @abstractmethod
    def get_budget(self) -> float:
        pass

    @abstractmethod
    def fetch_voucher_options(self) -> None:
        pass

    @abstractmethod
    def get_cart_info(self):
        pass
    
    @abstractmethod
    def add_voucher_to_cart(self, voucher_price: int) -> None:
        pass
    
    @abstractmethod
    def apply_order(self) -> None:
        pass