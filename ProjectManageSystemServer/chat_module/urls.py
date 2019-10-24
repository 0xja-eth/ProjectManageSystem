
from .views import ChatManager
from utils.interface_manager import InterfaceManager

Interfaces = {}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)
