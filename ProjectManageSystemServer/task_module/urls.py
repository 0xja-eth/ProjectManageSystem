
from .views import TaskManager
from utils.interface_manager import InterfaceManager

Interfaces = {}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)
