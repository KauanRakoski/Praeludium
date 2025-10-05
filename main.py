import flet as ft
from pages.index import Index


def main(page: ft.Page):
    page.title = "Praeludium"
    
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(
                Index(page)
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
    ft.app(target=main)