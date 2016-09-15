from django.contrib import admin
from claims.models import Claim
from claims.forms import ClaimForm


# Register your models here.
class ClaimAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created", "updated", "user"]
    form = ClaimForm

    class Meta:
        model = Claim

admin.site.register(Claim, ClaimAdmin)
