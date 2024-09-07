import sys
import ui
import menu

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'ui':
            app = ui.App()
            app.mainloop()
    menu.iniciar()