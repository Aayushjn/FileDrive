from django.db import models

class Model(models.Model):
    def __repr__(self) -> str:
        values = [self.__class__.__name__, "("]
        for field in self._meta.get_fields():
            values.append(f"{field.name}={getattr(self, field.name)}, ")
        values.append(")")
        return "".join(values)

    class Meta:
        abstract = True

models.Model = Model
