from django import template

register = template.Library()

@register.filter
def picUrlSize(photo, size):
	" Return url with size argument fed in"
	return photo.get_pic_url(size)
