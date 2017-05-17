from django.utils.translation import ugettext as _

BASE_ERROR_CODE = 245696

NO_PASSWORD_RESET_FOUND = {
	"code" : BASE_ERROR_CODE | 1,
	"message" : _("No password reset found"),
}