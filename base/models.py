from django.db import models
from django.utils import timezone
from users.models import CustomUser
from django.core.exceptions import ValidationError


class TimeBased(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    edited_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Page(TimeBased):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey("Page", related_name='children', null=True, blank=True, on_delete=models.CASCADE)
    creator = models.ManyToManyField(CustomUser)
    photo = models.CharField(max_length=100, null=True, blank=True, default='📄')
    closed = models.BooleanField(default=True)
    favourite = models.BooleanField(default=False)
    full_width = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name}" 


class Page_element(TimeBased):
    page = models.ForeignKey("Page", related_name="page_elements", on_delete=models.CASCADE)
    element_type = models.CharField(max_length=85)
    order_on_page = models.FloatField()
    color = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class Heading_1(models.Model):
    heading_text = models.CharField(max_length=85, null=True, blank=True)
    page_element = models.ForeignKey("Page_element", related_name="heading_1", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.heading_text}"


class Heading_2(models.Model):
    heading_text = models.CharField(max_length=85, null=True, blank=True)
    page_element = models.ForeignKey("Page_element", related_name="heading_2", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.heading_text}"


class Text(models.Model):
    text = models.CharField(max_length=5000, null=True, blank=True)
    page_element = models.ForeignKey("Page_element", related_name="text", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"
    

class Code(models.Model):
    code = models.CharField(max_length=20000, null=True, blank=True)
    language = models.CharField(max_length=64, null=True, blank=True)
    page_element = models.ForeignKey("Page_element", related_name="code", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code}"
    

def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB in bytes
        raise ValidationError("The file size should not exceed 5MB.")


class File(models.Model):
    file = models.FileField(upload_to='files/', validators=[validate_file_size])
    page_element = models.ForeignKey("Page_element", related_name="file", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.file.name}"


class Kanban(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    page_element = models.ForeignKey("Page_element", related_name="kanban", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Kanban_Group(models.Model):
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=100)
    kanban = models.ForeignKey("Kanban", related_name="kanban_group", on_delete=models.CASCADE)
    order = models.FloatField()

    def __str__(self):
        return f"{self.name}"


class Kanban_Card(models.Model):
    description = models.CharField(max_length=100, null=True, blank=True)
    kanban_group = models.ForeignKey("Kanban_Group", related_name="kanban_card", on_delete=models.CASCADE)
    order_on_group = models.FloatField()

    def __str__(self):
        return f"{self.description}"


class PageLink(models.Model):
    page = models.ForeignKey("Page", on_delete=models.CASCADE)
    page_element = models.ForeignKey("Page_element", related_name="page_link", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.page}"


class To_do(models.Model):
    description = models.CharField(max_length=500, null=True, blank=True)
    completed = models.BooleanField(default=False)
    page_element = models.ForeignKey("Page_element", related_name="to_do", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description}"


class Table(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    page_element = models.ForeignKey("Page_element", related_name="table", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"


class Table_row(models.Model):
    order = models.FloatField()
    table = models.ForeignKey("Table", related_name="rows", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"


class Table_data(models.Model):
    text = models.CharField(max_length=1000, null=True, blank=True)
    number = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    checkbox = models.BooleanField(null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    property_type = models.CharField(max_length=100)
    header = models.BooleanField()
    width = models.IntegerField()
    order = models.FloatField()
    table_row = models.ForeignKey("Table_row", related_name="data", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    table_data = models.ManyToManyField("Table_data", related_name="tags", blank=True)
    table_head = models.ForeignKey("Table_data", related_name="tag_heads", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

