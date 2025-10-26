import flet as ft
from pages.index import Index
from pages.documentation import Docs
from pages.answers import Answers
from stateManager import StateManager

from filehandler.fileHandler import FileHandler
from conversor.conversor import Conversor, default_rules
from soundmanager.soundManager import SoundManager

APP_ROUTES = {
    "/": Index,
    "/docs": Docs,
    "/answers": Answers
}

DEFAULT_ROUTE = "/"
DEFAULT_VIEW = Index

def main(page: ft.Page):
    page.title = "Praeludium"
    
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    state = StateManager(page)
    
    state.rules = default_rules()
    state.conversor_service = Conversor(state.rules)
    state.file_service = FileHandler()
    state.sound_service = SoundManager()
    
    def route_change(route):
        page.views.clear()
        
        view_class = APP_ROUTES.get(page.route, DEFAULT_VIEW)
        
        page.views.append(
            view_class(page, state)
        )
        
        page.update()
        
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")