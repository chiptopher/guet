class Committer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __eq__(self, o):
        return self.name == o.name and self.email == o.email
