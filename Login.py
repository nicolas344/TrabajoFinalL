from User import User


class Login:
    def __init__(self):
        self.listUsers = []
        self.listGroups = []

    def findUserById(self, user_id, list_users):
        return next((user for user in list_users if user.userID == user_id), None)

    def findGroupById(self, group_id, list_groups):
        for group in list_groups:
            if group.idGroup == group_id:
                return group
        return None

    def registerNewUser(self):
        newUser = User("", "", "", "")
        newUser.registerUser()

        user_instance = User(name=newUser.name,
                             surname=newUser.surname,
                             userID=newUser.userID,
                             password=newUser.password,
                             saveGroups=newUser.saveGroups,
                             balance=newUser.balance)
        self.listUsers.append(user_instance)

    def loginUser(self):
        while True:
            user_id = input("Ingrese su ID de usuario: ")
            password = input("Ingrese su contraseña: ")

            for user_instance in self.listUsers:
                if user_instance.userID == user_id and user_instance.password == password:
                    print("Has iniciado sesión correctamente, bienvenido!")
                    return user_instance  # Devuelve una instancia de User
            else:
                print("ID o contraseña incorrectos. Inténtalo de nuevo.")
                try_again = input("¿Desea intentar nuevamente? (s/n): ")
                if try_again.lower() != 's':
                    return None
