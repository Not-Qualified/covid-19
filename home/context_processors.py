from .models import HitCounter

def hit(request):
	obj = HitCounter.objects.first()
	obj.hit_count += 1
	obj.save()
	return {"total_hit": obj.hit_count }