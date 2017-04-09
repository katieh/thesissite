from django.contrib import admin
from .models import Activity, Tag


class ActivityAdmin(admin.ModelAdmin):

	actions = ['download_csv']
	list_display = ('user', 'start_time', 'tot_dist', 'RPE', 'tot_time', 'comments', 'tags', 'met_expectation')

	def download_csv(self, request, queryset):
		import csv
		from django.http import HttpResponse
		import StringIO

		f = StringIO.StringIO()
		writer = csv.writer(f)
		writer.writerow(['user', 'start_time', 'tot_dist', 'RPE', 'tot_time', 'comments', 'tags', 'met_expectation'])
		for s in queryset:
			writer.writerow([s.user, s.start_time, s.tot_dist, s.RPE, s.tot_time, s.comments, s.tags, s.met_expectation])

		f.seek(0)
		response = HttpResponse(f, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
		return response

	download_csv.short_description = "Download CSV file for selected stats."


class TagAdmin(admin.ModelAdmin):

	actions = ['download_csv']
	list_display = ('user', 'run', 'tag', 'date', 'value', 'comments')

	def download_csv(self, request, queryset):
		import csv
		from django.http import HttpResponse
		import StringIO

		f = StringIO.StringIO()
		writer = csv.writer(f)
		writer.writerow(['user', 'run', 'tag', 'date', 'value', 'comments'])
		for s in queryset:
			writer.writerow([s.user, s.run, s.tag, s.date, s.value, s.comments])

		f.seek(0)
		response = HttpResponse(f, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
		return response

	download_csv.short_description = "Download CSV file for selected stats."

# Register your models here.
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Tag)
