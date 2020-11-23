from .models import HitCounter

def hit(request):

	# obj = HitCounter.objects.first()
	# obj.hit_count += 1
	# obj.save()
	# return {"total_hit": obj.hit_count }

	if(request.session.get("visitor")):
		obj = HitCounter.objects.first()
		return {"total_hit": obj.hit_count }
	else:
		# request.session.set_expiry(300)
		request.session["visitor"] = True
		obj = HitCounter.objects.first()
		obj.hit_count += 1
		obj.save()
		return {"total_hit": obj.hit_count }