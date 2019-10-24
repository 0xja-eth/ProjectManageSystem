
from .views import ProjectManager
from utils.interface_manager import InterfaceManager

Interfaces = {}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)
