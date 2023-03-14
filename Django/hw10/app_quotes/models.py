from django.db.models import Model, ForeignKey, CharField, TextField, CASCADE, ManyToManyField


class Tag(Model):
    name = CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f'{self.name}'


class Author(Model):
    fullname = CharField(max_length=50, unique=True)
    born_date = CharField(max_length=10, null=False)
    born_location = CharField(max_length=100, null=False)
    bio = TextField(null=False)

    def __str__(self):
        return f'{self.fullname}'


class Quote(Model):
    author = ForeignKey(Author, on_delete=CASCADE)
    text = TextField(unique=True, null=False)
    tags = ManyToManyField(Tag)

    def __str__(self):
        return f'{self.author.fullname}: "{self.text[:50]}..." {self.tags}'

    def show_author(self):
        return self.author

    def show_text(self):
        return self.text

    def show_tags(self):
        tag = self.tags.all()
        return tag
