import random
import datetime
from Debt import Debt
from SaveGroups import SaveGroup


class User:

    def __init__(self, name, surname, userID, password, saveGroups=None, balance=random.randint(0, 1000000)):
        self.name = name
        self.surname = surname
        self.userID = userID
        self.password = password
        self.saveGroups = saveGroups if saveGroups is not None else []
        self.balance = balance
        self.debtsList = []
        self.moneyMovements = []

    def registerUser(self):
        print("Para ser registrado ingrese los siguientes datos:")
        self.name = input("Ingrese su nombre: ")
        self.surname = input("Ingrese su apellido: ")
        self.userID = input("Ingrese su numero de identificacion: ")
        self.password = input("Ingrese una contraseña segura: ")
        print("Usuario registrado con exito")

    def printMoneyMovements(self):
        print("-" * 20)
        print("Historial de transacciones")
        for transaction in self.moneyMovements:
            print("Fecha: ", transaction["date"])
            print("Hora: ", transaction["hour"])
            print("Tipo de movimiento: ", transaction["type"])
            print("Monto: ", transaction["amount"])
            print("Saldo antes de la transacción: ", transaction["balanceBefore"])
            print("Saldo despues de la transacción: ", transaction["balanceAfter"])
            print("-" * 20)
            print("\n")

    def printUserGroups(self, list_groups):
        print("-" * 20)
        print("Grupos de ahorro:")
        for group in list_groups:
            print(f"-- {group.nameGroup} (ID: {group.idGroup})")
            for user in group.usersGroup:
                print(f"  - {user.name} {user.surname} (ID: {user.userID})")
            print("-" * 20)

    def createSaveGroup(self, login_instance):
        if len(self.saveGroups) < 2:
            group_id = random.randint(100000, 999999)
            group_balance = 0
            group_name = input("Ingrese el nombre del grupo: ")
            new_group = SaveGroup(nameGroup=group_name, balanceGroup=group_balance, usersGroup=[self], idGroup=group_id,
                                  investments=None)
            self.saveGroups.append(new_group)
            login_instance.listGroups.append(new_group)

            print(f"Se ha creado el grupo de ahorro {group_id} con éxito.")

            add_users = input("¿Desea agregar otros usuarios al grupo? (s/n): ").lower()
            if add_users == 's':
                self.addUsersToSaveGroup(login_instance)

        else:
            print("Ya has alcanzado el límite de grupos de ahorro.")

    def depositMoneyInGroup(self, login_instance):
        print("Depositar dinero en grupo de ahorro:")
        self.printUserGroups(self.saveGroups)
        group_id = int(input("Ingrese el ID del grupo en el que desea depositar (o '0' para salir): "))

        if group_id == 0:
            return

        selected_group = login_instance.findGroupById(group_id, self.saveGroups)

        if selected_group:
            amount = int(input("Ingrese la cantidad a depositar: "))
            if amount > self.balance:
                print("No tienes suficiente dinero para realizar el depósito.")
            else:
                amountWcomission = amount - amount * 0.001
                self.balance -= amountWcomission
                selected_group.balanceGroup += amountWcomission
                selected_group.investments[self.userID] += amountWcomission
                print(f"Se han depositado {amount}  al grupo de ahorro {selected_group.idGroup}.")
                print(f"Nuevo saldo personal: {self.balance}")
                print(
                    f"Se ha invertido en el grupo por el usuario {self.userID}: {selected_group.investments[self.userID]}")
                movementRegister = {
                    'date': datetime.datetime.now().strftime("%d/%m/%Y"),
                    'hour': datetime.datetime.now().strftime("%H:%M:%S"),
                    'type': f"Transferencia a grupo de ahorro {selected_group.idGroup} por {amountWcomission}",
                    "amount": amountWcomission,
                    "balanceBefore": self.balance,
                    "balanceAfter": self.balance - amountWcomission
                }
                self.moneyMovements.append(movementRegister)
        else:
            print(f"Grupo de ahorro {group_id} no encontrado. Inténtelo nuevamente.")

    def addUsersToSaveGroup(self, login_instance):
        print("Agregar usuarios al grupo de ahorro:")
        group_id = int(input("Ingrese el ID del grupo al que desea agregar usuarios (o '0' para salir): "))

        if group_id == 0:
            return

        selected_group = login_instance.findGroupById(group_id, self.saveGroups)

        if selected_group:
            while True:
                user_id = input("Ingrese el ID del usuario a agregar (o 'q' para salir): ")
                if user_id.lower() == 'q':
                    break
                found_user = login_instance.findUserById(user_id, login_instance.listUsers)
                if found_user:
                    selected_group.usersGroup.append(found_user)
                    print(f"Usuario {user_id} agregado al grupo de ahorro {selected_group.idGroup}.")
                else:
                    print(f"Usuario {user_id} no encontrado. Inténtelo nuevamente.")
        else:
            print(f"Grupo de ahorro {group_id} no encontrado. Inténtelo nuevamente.")

    def askGroupLoan(self, login_instance):
        print("Solicitar prestamo del grupo de ahorro: ")
        self.printUserGroups(self.saveGroups)
        group_id = int(input("Ingrese el ID del grupo al que desea solicitar el prestamo (o q para salir): "))
        if group_id == 0:
            return
        selected_group = login_instance.findGroupById(group_id, self.saveGroups)

        if selected_group:
            # obtiene la inversion que lleva el usuario
            inversion_usuario = selected_group.investments.get(self.userID, 0)
            amountD = int(input("Ingrese la cantidad a solicitar el prestamo: "))
            if amountD > inversion_usuario or amountD > selected_group.balanceGroup:
                print("El monto del depósito no puede superar la inversión total del usuario en este grupo.")
                print("O el prestamo solicitado ha superado el monto que guarda el grupo")
                return
            amountWComission = amountD - amountD * 0.001
            debt_name = input("Ingrese como quiere nombrar esta deuda")
            term_to_pay = int(input("Ingrese en cuantos meses desea pagar (max: 2)"))
            if term_to_pay > 2:
                print("El plazo de pago no puede ser superior a 2 meses. Se establecerá en 2 meses.")
                term_to_pay = 2
            top_contributor = selected_group.getTopContributor()
            if self == top_contributor:
                interest_rate = 0.02
                print(f"Eres premiado por ser el mayor contribuidor a tu grupo de ahorro")
                print(f"Tu interes sera del 2% en vez del 3%")
            else:
                interest_rate = 0.03
            debt_instance = Debt(name=debt_name, amount=amountWComission, interest=interest_rate, termToPay=term_to_pay)
            self.debtsList.append(debt_instance)
            self.balance += amountWComission
            selected_group.balanceGroup -= amountWComission
            movementRegister = {
                'date': datetime.datetime.now().strftime("%d/%m/%Y"),
                'hour': datetime.datetime.now().strftime("%H:%M:%S"),
                'type': f"Solicitud de préstamo al grupo {selected_group.idGroup} por {amountWComission}",
                "amount": amountWComission,
                "balanceBefore": self.balance,
                "balanceAfter": self.balance + amountWComission
            }
            self.moneyMovements.append(movementRegister)
        else:
            print(f"Grupo de ahorro {group_id} no encontrado. Inténtelo nuevamente.")

    def externalGroupLoan(self, login_instance):
        print("Solicitar prestamo a un grupo de ahorro externo: ")
        IDcurrentGroup = int(input("Ingrese el id del grupo desde el cual quiere pedir el prestamo: "))
        print("Estos son los grupos que estan disponibles en el sistema")
        self.printUserGroups(login_instance.listGroups)
        IDtargetGroup = int(input("Elige a cual quieres pedirle el prestamo: "))

        current_group = login_instance.findGroupById(IDcurrentGroup, self.saveGroups)
        target_group = login_instance.findGroupById(IDtargetGroup, login_instance.listGroups)
        if current_group and target_group:
            if any(user in target_group.usersGroup for user in current_group.usersGroup):
                print("Perfecto! uno de tus compañeros de grupo se encuentra en este grupo.")
                print("Puedes continuar el proceso para pedir tu prestamo.")
                # ED= External Debt
                EDname = input("Ingrese como quiere nombrar esta deuda")
                EDamount = int(input("Ingrese el monto que quiere pedir como prestamo"))
                if EDamount > target_group.balanceGroup:
                    print("El monto del depósito no puede superar la inversión total del usuario en este grupo.")
                    print("O el prestamo solicitado ha superado el monto que guarda el grupo")
                    return
                EDamountWComission = EDamount - EDamount * 0.001
                EDtermToPay = int(input("Ingrese en cuantos meses desea pagar (max:2)"))
                if EDtermToPay > 2:
                    print("El plazo de pago no puede ser superior a 2 meses. Se establecerá en 2 meses.")
                    EDtermToPay = 2
                top_contributor = current_group.getTopContributor()
                if self == top_contributor:
                    EDinterestRate = 0.04
                    print(f"Eres premiado por ser el mayor contribuidor a tu grupo de ahorro")
                    print(f"Tu interes sera del 4% en vez del 5%")
                else:
                    EDinterestRate = 0.05

                debt_instance = Debt(name=EDname, amount=EDamountWComission, interest=EDinterestRate,
                                     termToPay=EDtermToPay)
                self.debtsList.append(debt_instance)
                self.balance += EDamountWComission
                target_group.balanceGroup -= EDamountWComission

                movementRegister = {
                    'date': datetime.datetime.now().strftime("%d/%m/%Y"),
                    'hour': datetime.datetime.now().strftime("%H:%M:%S"),
                    'type': f"Solicitud de préstamo externo al grupo {target_group.idGroup} por {EDamountWComission}",
                    "amount": EDamountWComission,
                    "balanceBefore": self.balance,
                    "balanceAfter": self.balance + EDamountWComission
                }
                self.moneyMovements.append(movementRegister)
            else:
                print("Ninguno de tus compañeros de grupo está en este grupo. No puedes solicitar el préstamo.")
        else:
            print("Al menos uno de los grupos no existe. Intenta nuevamente.")

    def payDebts(self):
        print("Esta es la lista de las deudas que tienes pendientes")
        for i, debt in enumerate(self.debtsList):
            print(f"{i + 1}. {debt.name} - Monto: {debt.amount} - Cuotas restantes: {debt.termToPay}")

        if not self.debtsList:
            print("Felicitaciones! Estás al día con tus deudas...")
            return

        try:
            selected_index = int(input("Seleccione el número de la deuda que desea pagar (o 0 para salir): ")) - 1

            if selected_index == -1:
                return

            selected_debt = self.debtsList[selected_index]
            monthly_installment = selected_debt.calculate_monthly_installment() + selected_debt.interest
            MIwComission = monthly_installment - monthly_installment * 0.001
            print(f"La cuota mensual para la deuda {selected_debt.name} es de {MIwComission}.")

            confirm_payment = input("¿Desea realizar el pago de esta cuota? (s/n): ").lower()

            if confirm_payment == 's':
                if self.balance >= MIwComission:
                    self.balance -= MIwComission
                    selected_debt.termToPay -= 1
                    print(f"Se ha realizado el pago de la cuota para la deuda {selected_debt.name}.")
                    print(f"Saldo actual: {self.balance}")

                    if selected_debt.termToPay == 0:
                        print(f"Has pagado la deuda {selected_debt.name} en su totalidad.")
                        self.debtsList.remove(selected_debt)
                    else:
                        # Actualiza la cantidad total de la deuda después de realizar el pago
                        selected_debt.amount -= selected_debt.calculate_monthly_installment()

                    movementRegister = {
                        'date': datetime.datetime.now().strftime("%d/%m/%Y"),
                        'hour': datetime.datetime.now().strftime("%H:%M:%S"),
                        'type': f"Pago de cuota de la deuda {selected_debt.name}",
                        "amount": MIwComission,
                        "balanceBefore": self.balance + MIwComission,
                        "balanceAfter": self.balance
                    }
                    self.moneyMovements.append(movementRegister)
                else:
                    print("Saldo insuficiente para realizar el pago.")
            else:
                print("Pago cancelado.")

        except (ValueError, IndexError):
            print("Selección no válida. Inténtelo nuevamente.")

    def dissolveSaveGroup(self, login_instance):
        group_id = int(input("Ingrese el ID del grupo que desea disolver: "))
        selected_group = login_instance.findGroupById(group_id, login_instance.listGroups)

        if selected_group and selected_group.balanceGroup > 0:
            total_balance = selected_group.balanceGroup
            commission = 0.05 * total_balance
            final_balance = total_balance - commission

            for user in selected_group.usersGroup:
                user_percentage = selected_group.investments.get(user.userID, 0) / total_balance
                user_amount = user_percentage * final_balance
                user.balance += user_amount

            print(f"El grupo de ahorro {selected_group.nameGroup} se ha disuelto.")
            print(f"Comisión del banco: {commission}")
            print(f"Saldo total distribuido a los usuarios: {final_balance}")
            print("Saldo individual de los usuarios después de la disolución:")
            for user in selected_group.usersGroup:
                print(f"{user.name}")

            login_instance.listGroups.remove(selected_group)
        elif selected_group:
            print(f"El saldo del grupo de ahorro {selected_group.nameGroup} es cero. No se puede disolver.")
        else:
            print(f"Grupo de ahorro {group_id} no encontrado. Inténtelo nuevamente.")
