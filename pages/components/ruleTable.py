import flet as ft

class RuleTable(ft.DataTable):
    def __init__(self, rules):
        
        columns = [
                ft.DataColumn(ft.Text("Texto", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Informação Musical ou Ação", weight=ft.FontWeight.BOLD)),
        ]
        
        rows = []
        for text, action in rules.items():
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(text)),
                        ft.DataCell(ft.Text(action)),
                    ]
                )
            )
            
        super().__init__(
            columns=columns, 
            rows=rows,
            heading_row_color=ft.Colors.WHITE24,
            data_row_color={"hover": ft.Colors.WHITE10},
            border=ft.border.all(1, ft.Colors.WHITE30),
            border_radius=ft.border_radius.all(10),
            width=700,
        )
        
              