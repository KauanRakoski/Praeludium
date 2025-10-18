import flet as ft
from pages.index import Index
from pages.documentation import Docs
from pages.answers import Answers
from stateManager import StateManager

def main(page: ft.Page):
    page.title = "Praeludium"
    
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    state = StateManager()
    
    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(
                Index(page, state)
            )
        elif page.route == '/docs':
            page.views.append(
                Docs(page, state)
            )
        
        else:
            page.views.append(
                Answers(page, state)
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