from Login import Login


class Menu:
    def __init__(self):
        self.login_instance = Login()
        self.logged_user = None

    def display_initial_menu(self):
        while True:
            print("----- Menú Principal -----")
            print("1. Registrarse")
            print("2. Iniciar Sesión")
            print("3. Salir")

            choice = input("Ingrese su elección: ")

            if choice == '1':
                self.login_instance.registerNewUser()
            elif choice == '2':
                self.logged_user = self.login_instance.loginUser()
                if self.logged_user:
                    self.display_logged_in_menu()
            elif choice == '3':
                print("¡Hasta luego!")
                break
            else:
                print("Elección no válida. Inténtelo nuevamente.")

    def display_logged_in_menu(self):
        while True:
            print("----- Menú Después de Iniciar Sesión -----")
            print("1. Ver historial de transacciones")
            print("2. Crear grupo de ahorro")
            print("3. Depositar dinero en grupo de ahorro")
            print("4. Agregar usuarios al grupo de ahorro")
            print("5. Solicitar préstamo del grupo de ahorro")
            print("6. Solicitar préstamo a un grupo de ahorro externo")
            print("7. Pagar deudas")
            print("8. Mostrar lista de grupos")
            print("9. Disolver grupo de ahorro")
            print("10. Cerrar sesión")

            choice = input("Ingrese su elección: ")

            if choice == '1':
                self.logged_user.printMoneyMovements()
            elif choice == '2':
                self.logged_user.createSaveGroup(self.login_instance)
            elif choice == '3':
                self.logged_user.depositMoneyInGroup(self.login_instance)
            elif choice == '4':
                self.logged_user.addUsersToSaveGroup(self.login_instance)
            elif choice == '5':
                self.logged_user.askGroupLoan(self.login_instance)
            elif choice == '6':
                self.logged_user.externalGroupLoan(self.login_instance)
            elif choice == '7':
                self.logged_user.payDebts()
            elif choice == '8':
                self.logged_user.printUserGroups(self.logged_user.saveGroups)
            elif choice == '9':
                self.logged_user.dissolveSaveGroup(self.login_instance)
            elif choice == '10':
                print(f"Hasta luego, {self.logged_user.name}!")
                self.logged_user = None
                break
            else:
                print("Elección no válida. Inténtelo nuevamente.")

