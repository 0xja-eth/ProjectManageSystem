
from .views import ChatView
from utils.interface_manager import InterfaceManager

Interfaces = {}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)
