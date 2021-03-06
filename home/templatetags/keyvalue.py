from django import template
register = template.Library()

@register.filter
def get_item(dict, key):
	if key in dict:
		return dict[key]	
	else:
		return 0


@register.filter
def get_active(dict):
	if not "confirmed" in dict:
		dict["confirmed"] = 0
	if not "recovered" in dict:
		dict["recovered"] = 0
	if not "deceased" in dict:
		dict["deceased"] = 0
	if not "other" in dict:
		dict["other"] = 0
	if "confirmed" in dict and "recovered" in dict and "deceased" in dict and "other" in dict:
		return dict["confirmed"] - (dict["recovered"] + dict["deceased"] + dict["other"])
	if "confirmed" in dict and "recovered" in dict and "deceased" in dict:
		return dict["confirmed"] - (dict["recovered"] + dict["deceased"])
	else:
		return None

@register.filter
def get_shortcut(value):
	if("Lakhs" in value):
		return value.replace(" Lakhs", "L")
	elif("Crores" in value):
		return value.replace(" Crores", "Cr")
	elif("Thousands" in value):
		return value.replace(" Thousands", "K")
	else:
		return value