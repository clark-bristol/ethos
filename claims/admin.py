from django.contrib import admin
from claims.models import Claim
from claims.forms import ClaimForm

# Register your models here.
class ClaimAdmin(admin.ModelAdmin):
	list_display = ["title", "source", "timestamp", "updated", "id", "user", "user_id", "votes"]
	form = ClaimForm
	class Meta:
		model = Claim

admin.site.register(Claim, ClaimAdmin)