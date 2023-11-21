class SaveGroup:
    def __init__(self, nameGroup, balanceGroup, usersGroup, idGroup, investments):
        self.nameGroup = nameGroup
        self.idGroup = idGroup
        self.balanceGroup = balanceGroup
        self.usersGroup = usersGroup
        self.investments = {user.userID: 0 for user in usersGroup}

    def getTopContributor(self):
        sorted_users = sorted(self.usersGroup, key=lambda user: self.investments.get(user.userID, 0), reverse=True)
        top_contributor = sorted_users[0] if sorted_users else None
        return top_contributor
